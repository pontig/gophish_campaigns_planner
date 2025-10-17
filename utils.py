from datetime import datetime, timezone, timedelta
from gophish import Gophish
import os

def connect_gophish():
    HOST = "https://127.0.0.1:3333"
    
    API_KEY = os.environ.get("GOPHISH_API_KEY")
    if not API_KEY:
        raise ValueError("GOPHISH_API_KEY not set in environment, set it and retry.")
    
    # Connect
    try:
        api = Gophish(API_KEY, host=HOST, verify=False)
        print(f"Successfully connected to Gophish at {HOST}")
        
        # Test the connection by getting campaigns
        campaigns = api.campaigns.get()
        print(f"Connection established. Found {len(campaigns)} campaigns:")
            
    except Exception as e:
        print(f"Error connecting to Gophish server at {HOST}")
        print(f"Error details: {str(e)}")
        raise e
    
    return api

def dateFromDuration(start_date, days):
    """Helper: return ISO8601 string for start_date + days. If start_date is None, use now."""
    if start_date is None:
        start_date = datetime.now(timezone.utc)
    if days is None:
        return None
    elif isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date)
    return (start_date + timedelta(days=days)).isoformat()

def find_by_name(collection_getter, name, resource_type):
    """Helper: call collection_getter() to get list, return first matching name."""
    items = collection_getter()
    for it in items:
        if getattr(it, "name", None) == name:
            return it
    raise ValueError(f"{resource_type} named '{name}' not found. Available: {[i.name for i in items]}")
