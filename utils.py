from datetime import datetime, timezone, timedelta
import random
import urllib3
from gophish import Gophish
import os
import csv

# Disable SSL warnings for localhost connections
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

def render_client_html(client):
    parts = []
    parts.append(f"<div class=\"client\">\n  <h2>{client.client}</h2>")

    parts.append(f"""  <p>Il seguente documento spiega l'andamento delle simulazioni di campagne phishing per il cliente {client.client}.</p>
                        <p>La prima tabella elenca le email che sono state oggetto delle campagne simulate, con il numero di volte in cui ciascuna email è stata utilizzata.</p>
                        <p>La seconda tabella raggruppa le campagne per template email, elencando per ciascuna il titolo, lo stato attuale, il numero di email inviate, aperte e cliccate, nonché le date di inizio e fine della campagna.</p>
                        <br>
                 """)

    # Emails table
    if client.emails:
        parts.append("  <h3>Emails interessate nelle campagne</h3>")
        parts.append("  <table>\n    <tr><th>Email</th><th>#</th></tr>")
        for e in client.emails:
            parts.append(f"    <tr><td>{e.email}</td><td>{e.count}</td></tr>")
        parts.append("  </table>")

    # Campaigns
    if client.campaigns:
        parts.append("  <h3 class=\"breakbefore\">Campagne</h3>")
        parts.append("  <table>\n    <tr><th>Tipo email</th><th>Stato</th><th>Inviate</th><th>Aperte</th><th>Cliccate</th><th>Inizio</th><th>Fine</th></tr>")
        for c in client.campaigns:
            status_class = 'status-completed' if c.status == 'Completed' else 'status-active'
            parts.append(
                "    <tr>" +
                f"<td>{c.title}</td><td class=\"{status_class}\">{c.status}</td>" +
                f"<td>{c.sent}</td><td>{c.opened}</td><td>{c.clicked}</td><td>{c.launch_date[:10]}</td><td>{c.send_by_date[:10]}</td>" +
                "</tr>"
            )
        parts.append("  </table>")

    # Global stats
    if client.global_stats:
        gs = client.global_stats
        parts.append(f"  <div class=\"stats\"> <div class=\"global-stats\"><b>Totale</b>📤 Inviate: {gs.get('sent',0)} &nbsp; 👁️ Aperte: {gs.get('opened',0)} &nbsp; 🖱️ Cliccate: {gs.get('clicked',0)}</div></div>")

    parts.append("  <img src=\"https://www.getecom.it/wp-content/uploads/2024/02/LOGO.png\" alt=\"Getecom Logo\">")
    parts.append("  <p>Generato automaticamente in data " + datetime.now(timezone.utc).isoformat()[:10] + "</p>")

    parts.append("</div>")
    return "\n".join(parts)