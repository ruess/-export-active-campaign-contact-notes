This python script will run through all of your Active Campaign contacts and export all existing contact notes to a CSV file in the same directory as the script file. You must first install python or python 3 (which is what I used) onto your local machine first before running the script in your Terminal or Command prompt.

Before running, make sure to replace the following variables in the file with your actual API URL and API key:

url = "https://[yoursubdomain].api-us1.com/api/3/notes"

api_key = "[yourAPIkey]"

=========

To run the script:

python3 active_campaign.py
