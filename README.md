# Gophish Campaigns Planner

This project is designed to help users plan and manage phishing simulation campaigns using Gophish. It allows users to create, schedule, and monitor email campaigns effectively.

Since the GoPhish campaigns provide only the sending of a single email for campaigns, this tool extends its functionality by allowing users to plan multiple emails to multiple groups over a specified duration.

## Usage

1. Place your email data in a CSV, following the structure `First Name, Last Name, Email, Group`, as the GoPhish import requires.
1. To launch a **full scale** phishing campaign, configure the first lines of `full_service.py` with your desired parameters, including the CSV file path, name of the client (identifying the set of GoPhish campaigns), start date, duration (in days), page name, URL, SMTP server name. __WIP: allow to use only a subset of the email list for each campaign__
1. Run `full_service.py`. It will generate a many-to-many mapping of emails to email addresses over the specified duration, creating multiple GoPhish campaigns and groups as needed. Every campaign will be named according a specific pattern: `"Campaign for {client_name} - {email template}"`.

## Monitoring

To see the status of your campaigns, you can use the `campaigns_summary.py` script, which will provide a summary of all the progresses made already grouped by client name.

## Removing clients

To remove all campaigns and groups associated with a specific client, use the `cancel_client_campaigns.py` script, providing the client name as configured in the `full_service.py` file.

## Acknowledgements

This project leverages the [GoPhish](https://github.com/gophish/gophish) API and is inspired by the need for more flexible phishing simulation campaigns in cybersecurity training.