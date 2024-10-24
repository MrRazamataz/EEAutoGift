# EE Auto-Gift
This script uses selenium to automate the process of gifting data from one number to another in an EE family.  
## Setup
1. Rename `.env.example` to `.env` and edit the values:
   * `EMAIL` - put your account email that you can login to https://id.ee.co.uk/login with.  
   * `PASSWORD` - put your account password. 
   * `FROM_NUMBER` - put the phone number of the person whose data you want to gift elsewhere. 
   * `TO_NUMBER` - put the phone number of the person you're **sending** the data to.
   * `AMOUNT` - put the amount, in **GB** that you wish to send. e.g. for `512`MB put `0.5`. 
2. Set up the script to run whenever your contract renews each month (or whenever). The script provides multiple ways of automatically setting methods of this up, see below if you want.
3. Then, hopefully you will receive a text every month that you have been gifted data!  

