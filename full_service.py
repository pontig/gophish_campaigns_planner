"""
Script that creates and launches multiple Gophish campaigns based on the list of emails provided in a CSV file.
Each campaign targets subsets of recipients and uses a specified email template, landing page, and SMTP profile.
"""

import random
import urllib3
from gophish.models import Campaign, Group, Page, Template, SMTP, User

# Disable SSL warnings for localhost connections
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from utils import *

# Config
CSV_FILE_PATH  = "mock_emails_2.csv"
CLIENT_NAME    = "Test Client 3"
START_LAUNCH   = '2026/01/10'  # YYYY/MM/DD, that will be converted to ISO8601
DURATION       = 365  # days, all emails will be sent within this duration
PAGE_NAME      = "Awareness"
URL            = "https://phish.hackforce.ai"
SMTP_NAME      = "Codin Marche"

# Auto-convert dates
MIN_LAUNCH_DATE = yyyymmdd_to_iso8601(START_LAUNCH)
DEADLINE_DATE = dateFromDuration(MIN_LAUNCH_DATE, DURATION)

api = connect_gophish()

# Step 1: Import email addresses and create groups
emails = import_emails_from_csv(CSV_FILE_PATH)
existing_templates = {t.name: t for t in api.templates.get()}

groups = []
# For each template, create a subset group (sample 80% of emails)
for template_name, template in existing_templates.items():
    subset_size = max(1, len(emails) // 5) * 4
    subset_emails = random.sample(emails, min(subset_size, len(emails)))

    targets = [User(first_name=email[0], last_name=email[1], email=email[2], position=email[3]) for email in subset_emails]
    # Shuffle targets to ensure randomness
    random.shuffle(targets)
    group = Group(name=f"Group for {CLIENT_NAME} - {template_name}", targets=targets)
    
    # Sample a launch date between MIN_LAUNCH_DATE and DEADLINE_DATE
    launch_date = sample_date_between(MIN_LAUNCH_DATE, dateFromDuration(MIN_LAUNCH_DATE, DURATION/2)) # All campaigns launch in the first half of the duration
    
    print(f"Prepared group '{group.name}' with {len(group.targets)} targets it should start on {launch_date}.")
    groups.append((group, template, launch_date))

# Step 2: Create and launch campaigns for each group-template pair
page = find_by_name(api.pages.get, PAGE_NAME, "Page")
smtp = find_by_name(api.smtp.get, SMTP_NAME, "SMTP profile")

print(f'Ready to launch {len(groups)} campaigns for client "{CLIENT_NAME}". Are you sure? (y/N)')
confirm = input().strip().lower()
if confirm != "y":
    print("Campaign creation aborted.")
    exit(0)

# Create groups only after confirmation
for i, (group, template, launch_date) in enumerate(groups):
    try: 
        created_group = api.groups.post(group)
        groups[i] = (created_group, template, launch_date)
        print(f"Created group '{created_group.name}' with {len(created_group.targets)} targets.")
    except Exception as e:
        print(f"Error creating group '{group.name}': {str(e)}")

for group, template, launch_date in groups:
    campaign_name = f"Campaign for {CLIENT_NAME} - {template.name}"
    campaign = Campaign(
        name=campaign_name,
        groups=[Group(name=group.name)],
        template=Template(name=template.name),
        page=Page(name=page.name),
        smtp=SMTP(name=smtp.name),
        url=URL,
        launch_date=launch_date,
        send_by_date=DEADLINE_DATE
    )
    
    created_campaign = api.campaigns.post(campaign)
    print(f"Launched campaign '{created_campaign.name}' with ID: {created_campaign.id}, status: {created_campaign.status}.")