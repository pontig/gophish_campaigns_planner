import random
import urllib3
from gophish.models import Campaign, Group, Page, Template, SMTP, User, CampaignSummaries

# Disable SSL warnings for localhost connections
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from utils import *
from functools import reduce

api = connect_gophish()

summaries = api.campaigns.summary()

# Group campaigns by client
client_campaigns = {}
for summary in summaries.campaigns:
    # Extract client name from campaign name format "Campaign for {client} - {template}"
    if " - " in summary.name and summary.name.startswith("Campaign for "):
        client = summary.name.split(" - ")[0].replace("Campaign for ", "")
        
        if client not in client_campaigns:
            client_campaigns[client] = []
        client_campaigns[client].append(summary)
    else:
        print(f"Warning: Campaign name '{summary.name}' does not match expected format.")

# Print grouped campaigns with global stats
for client, campaigns in client_campaigns.items():
    print(f"Client: {client}")
    
    for summary in campaigns:
        print(f"  Campaign '{summary.name}' ({summary.status}):")
        print(f"    Sent: {summary.stats.sent}, Opened: {summary.stats.opened}, Clicked: {summary.stats.clicked}")
        print(f"    Start Date: {summary.launch_date}, End Date: {summary.send_by_date}")
    print("--------------------------------------------------")
    
    # Calculate global stats using functional programming
    total_sent = reduce(lambda acc, campaign: acc + campaign.stats.sent, campaigns, 0)
    total_opened = reduce(lambda acc, campaign: acc + campaign.stats.opened, campaigns, 0)
    total_clicked = reduce(lambda acc, campaign: acc + campaign.stats.clicked, campaigns, 0)
    
    print(f"  Global Stats - Sent: {total_sent}, Opened: {total_opened}, Clicked: {total_clicked}")
    print()
    
