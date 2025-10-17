"""
Cancel all campaigns and groups for a specific client in GoPhish.
The clients are identified in the campaigns and groups by a substring in their names.
"""

import random
import urllib3
from gophish.models import Campaign, Group, Page, Template, SMTP, User

# Disable SSL warnings for localhost connections
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from utils import *

# Config
CLIENT_NAME    = "Test Client"

api = connect_gophish()

print(f'About to cancel all campaigns and groups for client "{CLIENT_NAME}". Are you sure? (y/N)')
confirm = input().strip().lower()
if confirm != "y":
    print("Cancellation aborted.")
    exit(0)

# Step 1: Find the client's campaigns
all_campaigns = api.campaigns.get()
client_campaigns = [c for c in all_campaigns if CLIENT_NAME in c.name]
print(f"Found {len(client_campaigns)} campaigns for client '{CLIENT_NAME}'.")

for campaign in client_campaigns:
    try:
        api.campaigns.delete(campaign.id)
        print(f"Cancelled campaign '{campaign.name}' (ID: {campaign.id}).")
    except Exception as e:
        print(f"Error cancelling campaign '{campaign.name}' (ID: {campaign.id}): {str(e)}")
        
# Step 2: Find and delete groups associated with the client
all_groups = api.groups.get()
client_groups = [g for g in all_groups if CLIENT_NAME in g.name]
print(f"Found {len(client_groups)} groups for client '{CLIENT_NAME}'.")

for group in client_groups:
    try:
        api.groups.delete(group.id)
        print(f"Cancelled group '{group.name}' (ID: {group.id}).")
    except Exception as e:
        print(f"Error cancelling group '{group.name}' (ID: {group.id}): {str(e)}")