from gophish.models import Campaign, Group, Page, Template, SMTP

from utils import *

# CONFIG
GROUP_NAME     = "Test Group"
TEMPLATE_NAME  = "aruba"
PAGE_NAME      = "Awareness"
SMTP_NAME      = "Codin Marche"
CAMPAIGN_NAME  = "Test Campaign from API"
URL            = "https://phish.hackforce.ai"
LAUNCH         = None
durationInDays = 1
DEADLINE       = dateFromDuration(LAUNCH, durationInDays)

api = connect_gophish()
    
# 1) locate resources (by name)
group = find_by_name(api.groups.get, GROUP_NAME, "Group")
template = find_by_name(api.templates.get, TEMPLATE_NAME, "Template")
page = find_by_name(api.pages.get, PAGE_NAME, "Page")
smtp = find_by_name(api.smtp.get, SMTP_NAME, "SMTP profile")

print("Using:")
print(" Group:", group.id, group.name)
print(" Template:", template.id, template.name)
print(" Page:", page.id, page.name)
print(" SMTP:", smtp.id, smtp.name)

# 2) Build campaign
# Optional: schedule launch in 2 minutes. If you omit launch_date, it launches immediately.

campaign = Campaign(
    name=CAMPAIGN_NAME,
    groups=[Group(name=group.name)],       # can pass name only (client will resolve)
    template=Template(name=template.name),
    page=Page(name=page.name),
    smtp=SMTP(name=smtp.name),
    url=URL,  # optional: base URL used in link construction
    launch_date=LAUNCH,                 # ISO8601 string, or None
    send_by_date=DEADLINE                      # optional: ISO8601 by which to finish sends
)

# 3) ask confirmation and then create / post the campaign
print("Are you sure you want to create the campaign with the above settings? (y/N)")
confirm = input().strip().lower()
if confirm == "y":
    created = api.campaigns.post(campaign)
    print("Created campaign id:", created.id, "status:", created.status)
else:
    print("Campaign creation aborted.")

# # 4) Optional: fetch summary / results
# summary = api.campaigns.summary(created.id)
# print("Campaign summary:", summary.stats.as_dict())
