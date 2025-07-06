"""
Optimized LangChain Agent with Google Calendar Tools
"""

from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_FILE = 'credentials/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Get Google Calendar service with cached credentials"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('calendar', 'v3', credentials=credentials)

def get_calendar_id(service):
    """Get the appropriate calendar ID to use for operations"""
    try:
        calendar_list = service.calendarList().list().execute()
        for cal in calendar_list.get('items', []):
            if cal.get('accessRole') == 'owner':
                return cal['id']
        return 'primary'
    except:
        return 'primary'

calendar_service = get_calendar_service()
CALENDAR_ID = get_calendar_id(calendar_service)

def format_datetime(datetime_str: str) -> str:
    """Format datetime string for display with improved error handling"""
    try:
        if 'T' in datetime_str:
            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            return dt.strftime('%B %d, %Y at %I:%M %p')
        return datetime_str
    except (ValueError, AttributeError):
        return datetime_str

def get_time_status(event_start: str, current_time: datetime) -> str:
    """Get time status for an event (past, present, future)"""
    try:
        if 'T' not in event_start:
            return ""
        
        event_dt = datetime.fromisoformat(event_start.replace('Z', '+00:00')).replace(tzinfo=None)
        event_end_dt = event_dt + timedelta(hours=1)
        
        if event_end_dt < current_time:
            return " (already finished)"
        elif event_dt <= current_time <= event_end_dt:
            return " (happening now!)"
        elif event_dt > current_time:
            return " (upcoming)"
        return ""
    except (ValueError, AttributeError):
        return ""

# Define LangChain tools using the @tool decorator
@tool
def check_calendar_availability(date_str: str = None) -> str:
    """
    Check calendar events. Use date (YYYY-MM-DD) for specific day, "all" for all meetings, or empty for upcoming.
    """
    try:
        if date_str and date_str.lower() in ["all", "all meetings", "meetings"]:
            time_min = datetime.utcnow().isoformat() + 'Z'
            time_max = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
            query_description = "all upcoming meetings (next 30 days)"
        elif date_str:
            target_date = datetime.strptime(date_str, '%Y-%m-%d')
            time_min = target_date.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
            time_max = target_date.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
            query_description = f"events on {date_str}"
        else:
            time_min = datetime.utcnow().isoformat() + 'Z'
            time_max = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
            query_description = "upcoming events (next 7 days)"
        
        events_result = calendar_service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            if "all" in query_description:
                return "📅 Great news! You have no meetings or events scheduled. Your calendar is completely free!"
            elif date_str and date_str != "all":
                return f"📅 Your calendar is completely free on {date_str}! No events scheduled."
            else:
                return "📅 Your calendar looks clear for the next week. No upcoming events found."
        
        current_time = datetime.now()
        response = f"Found {len(events)} event(s):\n"
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'No Title')
            formatted_time = format_datetime(start)
            time_status = get_time_status(start, current_time)
            response += f"• {summary} on {formatted_time}{time_status}\n"
        
        return response.strip()
    
    except Exception as e:
        return f"Error checking calendar: {str(e)}"

@tool
def suggest_available_time_slots(date_str: str) -> str:
    """
    Suggest available 1-hour slots for date (YYYY-MM-DD) during business hours.
    """
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        suggestions = []
        
        business_hours = [9, 11, 13, 15]
        
        for hour in business_hours:
            slot_start = target_date.replace(hour=hour, minute=0, second=0, microsecond=0)
            slot_end = slot_start + timedelta(hours=1)
            
            events_result = calendar_service.events().list(
                calendarId=CALENDAR_ID,
                timeMin=slot_start.isoformat() + 'Z',
                timeMax=slot_end.isoformat() + 'Z',
                singleEvents=True
            ).execute()
            
            if not events_result.get('items', []):
                suggestions.append({
                    'start_time': slot_start.strftime('%I:%M %p'),
                    'end_time': slot_end.strftime('%I:%M %p')
                })
                
            if len(suggestions) >= 3:
                break
        
        if not suggestions:
            return f"No available slots found for {date_str} during business hours (9 AM - 5 PM). Try a different date?"
        
        response = f"Available time slots for {target_date.strftime('%B %d, %Y')}:\n"
        for i, slot in enumerate(suggestions, 1):
            response += f"{i}. {slot['start_time']} - {slot['end_time']}\n"
        
        return response
    
    except Exception as e:
        return f"Error suggesting time slots: {str(e)}"

@tool
def book_appointment(appointment_details: str) -> str:
    """
    Book appointment. Format: "title|YYYY-MM-DD|HH:MM|hours|description"
    Example: "Meeting|2025-07-07|10:00|1|Team sync"
    """
    try:
        parts = appointment_details.split('|')
        if len(parts) < 3:
            return "❌ Invalid format. Please provide: title|YYYY-MM-DD|HH:MM|duration_hours|description (last two are optional)"
        
        summary = parts[0].strip()
        date_str = parts[1].strip()
        start_time = parts[2].strip()
        duration_hours = int(parts[3].strip()) if len(parts) > 3 and parts[3].strip() else 1
        description = parts[4].strip() if len(parts) > 4 else ""
        
        appointment_date = datetime.strptime(f"{date_str} {start_time}", '%Y-%m-%d %H:%M')
        end_time = appointment_date + timedelta(hours=duration_hours)
        
        events_result = calendar_service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=appointment_date.isoformat() + 'Z',
            timeMax=end_time.isoformat() + 'Z',
            singleEvents=True
        ).execute()
        
        existing_events = events_result.get('items', [])
        
        if existing_events:
            return f"⚠️ Time slot conflicts with existing event: {existing_events[0].get('summary', 'Unnamed event')}. Please choose a different time."
        
        event = {
            'summary': summary,
            'description': description or f'Appointment booked via AI Assistant: {summary}',
            'start': {
                'dateTime': appointment_date.isoformat() + 'Z',
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat() + 'Z',
                'timeZone': 'UTC',
            },
        }
        
        created_event = calendar_service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        
        formatted_date = appointment_date.strftime('%B %d, %Y at %I:%M %p')
        return f"✅ Successfully booked '{summary}' for {formatted_date} (Duration: {duration_hours} hour{'s' if duration_hours != 1 else ''})\n\nEvent ID: {created_event.get('id')}\nCalendar Link: {created_event.get('htmlLink', 'N/A')}"
    
    except Exception as e:
        return f"❌ Error booking appointment: {str(e)}"

@tool
def remove_event(event_identifier: str) -> str:
    """
    Cancel event by title or partial title.
    """
    try:
        now = datetime.utcnow().isoformat() + 'Z'
        future_date = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
        
        events_result = calendar_service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=now,
            timeMax=future_date,
            maxResults=50,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        matching_events = [
            event for event in events_result.get('items', [])
            if event_identifier.lower() in event.get('summary', '').lower()
        ]
        
        if not matching_events:
            return f"❌ No events found matching '{event_identifier}'. Please check the event name and try again."
        
        if len(matching_events) == 1:
            event_to_delete = matching_events[0]
            calendar_service.events().delete(calendarId=CALENDAR_ID, eventId=event_to_delete['id']).execute()
            
            event_summary = event_to_delete.get('summary', 'Unnamed Event')
            start_time = event_to_delete['start'].get('dateTime', event_to_delete['start'].get('date'))
            formatted_time = format_datetime(start_time)
                
            return f"✅ Successfully cancelled '{event_summary}' scheduled for {formatted_time}"
        
        else:
            response = f"Found {len(matching_events)} events matching '{event_identifier}':\n"
            for i, event in enumerate(matching_events, 1):
                summary = event.get('summary', 'Unnamed Event')
                start_time = event['start'].get('dateTime', event['start'].get('date'))
                formatted_time = format_datetime(start_time)
                response += f"{i}. {summary} on {formatted_time}\n"
            
            response += "\nPlease be more specific about which event you want to cancel."
            return response
            
    except Exception as e:
        return f"❌ Error removing event: {str(e)}"

def create_booking_agent():
    """Create an optimized LangChain agent with calendar tools and memory"""
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.3
        )
        print("✅ Using Gemini 2.0 Flash-Lite")
    except Exception as e:
        print(f"⚠️ Gemini 2.0 Flash-Lite unavailable, falling back to 1.5 Flash: {e}")
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.3
            )
            print("✅ Using Gemini 1.5 Flash (fallback)")
        except Exception as e2:
            raise Exception(f"No Gemini models available: {e2}")
    
    tools = [check_calendar_availability, suggest_available_time_slots, book_appointment, remove_event]
    
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=conversation_memory,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=3,
        early_stopping_method="generate"
    )

booking_agent = None
conversation_memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True,
    input_key="input",
    output_key="output"
)

def get_agent():
    global booking_agent
    if booking_agent is None:
        booking_agent = create_booking_agent()
    return booking_agent

def chat_with_agent(message: str) -> str:
    """Chat with the booking agent with conversation memory"""
    try:
        agent = get_agent()
        current_datetime = datetime.now()
        current_date = current_datetime.strftime('%Y-%m-%d')
        current_time_12h = current_datetime.strftime('%I:%M %p')
        
        enhanced_message = f"""Current: {current_date} {current_time_12h}

{message}

Tools: check_calendar_availability(date_or_"all"), suggest_available_time_slots(date), book_appointment("title|date|time|hours|desc"), remove_event(title)
Format dates as YYYY-MM-DD, times as HH:MM (24h). Be concise."""
        
        response = agent.run(enhanced_message)
        
        return response
    
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}. Please try again or rephrase your request."

def get_conversation_history() -> list:
    """Get the current conversation history"""
    return getattr(conversation_memory.chat_memory, 'messages', [])

def clear_conversation_history():
    """Clear the conversation history"""
    try:
        conversation_memory.clear()
        print("✅ Conversation history cleared")
    except Exception as e:
        print(f"❌ Error clearing conversation history: {e}")

def get_conversation_summary() -> str:
    """Get a summary of the conversation"""
    try:
        messages = get_conversation_history()
        if not messages:
            return "No conversation history"
        
        summary = f"Conversation History ({len(messages)} messages):\n"
        for i, msg in enumerate(messages[-6:], 1):
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            summary += f"{i}. {role}: {content}\n"
        
        return summary
    except Exception as e:
        return f"Error getting conversation summary: {e}"
