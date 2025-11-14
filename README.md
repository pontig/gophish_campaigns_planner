# Gophish Campaigns Planner

This project is designed to help users plan and manage phishing simulation campaigns using Gophish. It allows users to create, schedule, and monitor email campaigns effectively.

Since the GoPhish campaigns provide only the sending of a single email for campaigns, this tool extends its functionality by allowing users to plan multiple emails to multiple groups over a specified duration.

## Fundamental step

Before using this tool, ensure you have a working GoPhish server set up and accessible. You will need to configure the [GoPhish API key](https://docs.getgophish.com/user-guide/documentation/changing-user-settings) as an environment variable named `GOPHISH_API_KEY`:

```bash
export GOPHISH_API_KEY="your_api_key_here"
```

being careful that the API key has a scope limited to the particular instance of terminal where you runned the command.

## Usage

1. Place your email data in a CSV, following the structure `First Name, Last Name, Email, Group`, as the GoPhish import requires.
1. To launch a **full scale** phishing campaign, configure the first lines of `full_service.py` with your desired parameters, including the CSV file path, name of the client (identifying the set of GoPhish campaigns), start date, duration (in days), page name, URL, SMTP server name. *WIP: allow to use only a subset of the email list for each campaign*
1. Run `full_service.py`. It will generate a many-to-many mapping of emails to email addresses over the specified duration, creating multiple GoPhish campaigns and groups as needed. Every campaign will be named according a specific pattern: `"Campaign for {client_name} - {email template}"`.

## Monitoring

To see the status of your campaigns, you can use the `campaigns_summary.py` script, which will provide a summary of all the progresses made already grouped by client name.

By running this script, in the same directory will be generated a report file named `campaigns_report.html`, which is a comprehensive HTML report summarizing the status of all campaigns and all users involved. This HTML file is meant to be printed in order to be used as a PDF file.

## Removing clients

To remove all campaigns and groups associated with a specific client, use the `cancel_client_campaigns.py` script, providing the client name as configured in the `full_service.py` file.

## Acknowledgements

This project leverages the [GoPhish](https://github.com/gophish/gophish) API and is inspired by the need for more flexible phishing simulation campaigns in cybersecurity training.

## Future Work (that I unlikely will do)

- Implement an incremental reporting system to track progress over time.
- Actually utilize the _Role_ field in the CSV for more targeted campaigns.
- Implement a web interface for easier campaign management.
- Add support for more complex scheduling options.