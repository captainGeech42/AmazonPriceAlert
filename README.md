# Amazon Price Alert script

This script will send you an email when the price for a specific item on Amazon drops beneath a certain threshold

Dependencies:
 * Python 2
 * `BeautifulSoup4` (the `pip` package is called `bs4`)
 * `requests`
 * `smtplib`
 * `MIMEText`
 * `ConfigParser`

Usage:
 1. Duplicate `config_example.ini` and rename it to `config.ini`
 2. Add correct Amazon product settings to `config.ini`
 3. Add correct email server settings to `config.ini`
 4. Run the script via `python amazon_price.py`
 5. You may wish to add this to `crontab` (*nix) or configure a `Scheduled Task` (Windows)
