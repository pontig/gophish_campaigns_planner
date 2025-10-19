import random
import urllib3
from gophish.models import Campaign, Group, Page, Template, SMTP, User, CampaignSummaries

# Disable SSL warnings for localhost connections
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from utils import *
from functools import reduce
from client_model import ClientSummary, CampaignInfo, EmailTarget
import json

api = connect_gophish()

summaries = api.campaigns.summary()
groups = api.groups.get()

# Group campaigns and groups by client
client_campaigns = {}
for summary in summaries.campaigns:
    # Extract client name from campaign name format "Campaign for {client} - {template}"
    if " - " in summary.name and summary.name.startswith("Campaign for "):
        client = summary.name.split(" - ")[0].replace("Campaign for ", "")
        
        if client not in client_campaigns:
            client_campaigns[client] = []
        client_campaigns[client].append(summary)
    else:
        print(f"⚠️  \033[93mWarning: Campaign name '{summary.name}' does not match expected format.\033[0m")

grouped_groups = {}
for group in groups:
    if " - " in group.name and group.name.startswith("Group for "):
        client = group.name.split(" - ")[0].replace("Group for ", "")

        if client not in grouped_groups:
            grouped_groups[client] = []
        grouped_groups[client].append(group)
    else:
        print(f"⚠️  \033[93mWarning: Group name '{group.name}' does not match expected format.\033[0m")
        
# Calculate email frequency across groups by client using functional programming
client_objects = {}
for client, groups in grouped_groups.items():
    # Extract all emails from all groups for this client
    all_emails = reduce(lambda acc, group: acc + [target.email for target in group.targets], groups, [])

    # Count occurrences of each email
    email_group_count = {}
    for email in all_emails:
        email_group_count[email] = email_group_count.get(email, 0) + 1

    # Create ClientSummary if not exists
    cs = client_objects.get(client, ClientSummary(client=client))
    cs.emails = [EmailTarget(email=e, count=c) for e, c in email_group_count.items()]
    client_objects[client] = cs

    print(f"👤 \033[96mClient {client}:\033[0m")
    for email, count in email_group_count.items():
        print(f"  📮 {email}: this mail is targeted by \033[93m{count}\033[0m campaign(s)")

print("\n\n")

# Print grouped campaigns with global stats
for client, campaigns in client_campaigns.items():
    print(f"👤 \033[96mClient: {client}\033[0m")
    cs = client_objects.get(client, ClientSummary(client=client))

    for summary in campaigns:
        status_emoji = "✅" if summary.status == "Completed" else "🔄"
        campaign_title = summary.name.split(" - ", 1)[1] if " - " in summary.name else summary.name
        print(f"  📧 \033[92mMail '{campaign_title}'\033[0m {status_emoji} \033[94m({summary.status})\033[0m:")
        print(f"    📤 Sent: \033[93m{summary.stats.sent}\033[0m, 👁️  Opened: \033[95m{summary.stats.opened}\033[0m, 🖱️  Clicked: \033[91m{summary.stats.clicked}\033[0m")
        print(f"    🚀 Start Date: \033[90m{summary.launch_date}\033[0m, ⏰ End Date: \033[90m{summary.send_by_date}\033[0m")

        # Append campaign info to client object
        ci = CampaignInfo(
            id=getattr(summary, 'id', None),
            title=campaign_title,
            status=summary.status,
            sent=getattr(summary.stats, 'sent', 0),
            opened=getattr(summary.stats, 'opened', 0),
            clicked=getattr(summary.stats, 'clicked', 0),
            launch_date=getattr(summary, 'launch_date', None),
            send_by_date=getattr(summary, 'send_by_date', None),
        )
        cs.campaigns.append(ci)

    print("\033[35m" + "─" * 100 + "\033[0m")

    # Calculate global stats using functional programming
    total_sent = reduce(lambda acc, campaign: acc + campaign.stats.sent, campaigns, 0)
    total_opened = reduce(lambda acc, campaign: acc + campaign.stats.opened, campaigns, 0)
    total_clicked = reduce(lambda acc, campaign: acc + campaign.stats.clicked, campaigns, 0)

    cs.global_stats = {"sent": total_sent, "opened": total_opened, "clicked": total_clicked}
    client_objects[client] = cs

    print(f"  📊 \033[1;97mGlobal Stats for client '{client}'\033[0m - 📤 Sent: \033[93m{total_sent}\033[0m, 👁️  Opened: \033[95m{total_opened}\033[0m, 🖱️  Clicked: \033[91m{total_clicked}\033[0m")
    print()

# Render HTML from template and client_objects
template_path = 'campaigns_template.html'
output_path = 'campaigns_summary.html'

# Read template
with open(template_path, 'r') as t:
    tpl = t.read()

body_parts = []
for c in client_objects.values():
    body_parts.append(render_client_html(c))

html = tpl.replace('{{title}}', 'Campaigns summary').replace('{{body}}', '\n'.join(body_parts))

with open(output_path, 'w') as out_f:
    out_f.write(html)

print(f"\nSaved structured HTML summary for {len(client_objects)} client(s) to {output_path}\n")
    
    
