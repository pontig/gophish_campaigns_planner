from datetime import datetime, timezone, timedelta
import random
from gophish import Gophish
import os
import csv

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

def import_emails_from_csv(file_path):
    emails = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the first line (header)
        for row in reader:
            if row:  # Avoid empty rows
                emails.append(row)
        return emails

def yyyymmdd_to_iso8601(date_str):
    """Convert YYYY/MM/DD string to ISO8601 format."""
    dt = datetime.strptime(date_str, "%Y/%m/%d")
    return dt.replace(tzinfo=timezone.utc).isoformat()

def sample_date_between(start_iso, end_iso):
    """Sample a random date between two ISO8601 dates."""
    start_dt = datetime.fromisoformat(start_iso)
    end_dt = datetime.fromisoformat(end_iso)
    delta = end_dt - start_dt
    random_days = random.randint(0, delta.days)
    sampled_date = start_dt + timedelta(days=random_days)
    return sampled_date.isoformat()