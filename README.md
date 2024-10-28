# EE Auto-Gift
This script uses selenium to automate the process of gifting data from one number to another in an EE family.
## Setup
### Prerequisites
You will need the geckodriver for the script to run. Install it with `apt install firefox-geckodriver`, and make sure its located at `/usr/bin/geckodriver`. To use a different browser, you can change this at the top of the main() function in the script.  
You will also need to install the required python packages with `pip install -r requirements.txt`.  
### Steps
1. Rename `.env.example` to `.env` and edit the values:
   * `EMAIL` - put your account email that you can login to https://id.ee.co.uk/login with.  
   * `PASSWORD` - put your account password. 
   * `FROM_NUMBER` - put the phone number of the person whose data you want to gift elsewhere. 
   * `TO_NUMBER` - put the phone number of the person you're **sending** the data to.
   * `AMOUNT` - put the amount, in **GB** that you wish to send. e.g. for `512`MB put `0.5`. 
2. Set up the script to run whenever your contract renews each month (or whenever). The script provides multiple ways (crontab or pm2) of automatically setting methods of this up, see below if you want (see below).
3. Then, hopefully you will receive a text every month that you have been gifted data!  

## Running the Script Automatically
The script provides a command line argument (CLI) to help you setup the script to run automatically.  
Run `ee.py` with the `--setup-cron` argument and the script will run you through the steps.  
If you already have experience with automating scripts, you can setup this yourself, obviously

## Other CLI Arguments
The CLI arguments take priority over the `.env` file settings. 
```commandline
options:
  --help                       Shows this.
  --username USERNAME          Your username.
  --password PASSWORD          Your password.
  --from-number FROM_NUMBER    The number you're gifting data from.  
  --to-number TO_NUMBER        The number you're gifting data to.
  --amount AMOUNT              The amount of data you're gifting. In GB.
  --setup-cron                 Helper to add a crontab to run the script every month on the day your contract renews.
```