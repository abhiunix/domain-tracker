# domain-tracker

## Description
This script is used to track the internal domains of an organization (in AWS Cloud).

## Features
- It fetch domains & subdomains from the route53 directly.
- Keep track of existing domains by creating a database of initialy founded domains.
- If anything changes in any domains, from status code to content length, you get notification on your slack.
- Slack Notifications for each new route entry in your DNS.
- Health check mechanism.

## Prerequisite:
- Python 3.x is required.
- [go](https://go.dev/doc/install)
- [httpx](https://github.com/projectdiscovery/httpx). 
- [anew](https://github.com/tomnomnom/anew)
- [notify](https://github.com/projectdiscovery/notify)

## Setup:
1. Clone the repository:
```
git clone https://github.com/abhiunixx/domain-tracker
cd domain-tracker
```

2. Install the required dependencies:
```
- Python 3.x is required.
- go
- [httpx](https://github.com/projectdiscovery/httpx). 
- [anew](https://github.com/tomnomnom/anew)
- [notify](https://github.com/projectdiscovery/notify)
```

3. Set up environment variables:
- Create a `.env` file in the project directory(ignore if already present).
- Define the following variables in the `.env` file:
  ```
  health_check_webhook=<your_health_check_webhook_url>
  ```

## Usage
Run the script manually for the initial setup:
```
python3 domain-tracker.py
```
### Configure the cronjob:
- Open the crontab file:
  ```
  crontab -e
  ```

- Add the following line to run the script every 5 minutes:
  ```
  0 * * * * /usr/bin/python3 /root/domain-tracker/attack_surface.py >> /root/domain-tracker/cron.log 2>&1
  ```

- Save and exit the crontab file.
## Contributions
Contributions to domain-tracker are welcome! Please fork the repository, make your enhancements, and submit a pull request.


## To do:
- [ ] Fix sorting of domains(currently it is not parsing domains with special characters).
- [ ] Add more detailing 