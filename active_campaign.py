import requests
import json
import csv

# Replace with your actual API URL and API key
url = "https://[yoursubdomain].api-us1.com/api/3/"
api_key = "[yourAPIkey]"

headers = {
    "accept": "application/json",
    "Api-Token": api_key
}

# Function to retrieve notes for a subscriber
def get_notes_for_subscriber(subscriber_id):
    url_subscriber = f"{url}notes?contact={subscriber_id}"
    response = requests.get(url_subscriber, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data['notes']  # Return only the notes part of the response
    else:
        print(f"Error fetching notes for subscriber {subscriber_id}: {response.status_code}")
        return []  # Return an empty list if there's an error

# Main function to retrieve notes and create CSV

def main():
    # Create CSV file first
    with open("activecampaign_notes.csv", "w", newline="") as csvfile:
        fieldnames = ["subscriber_id", "subscriber_email", "note_id", "note_body"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    total_subscribers = 0
    offset = 0

    while True:
        url_subscribers = f"{url}contacts?limit=100&offset={offset}"
        response_subscribers = requests.get(url_subscribers, headers=headers)

        if response_subscribers.status_code == 200:
            subscribers_data = json.loads(response_subscribers.text)
            total_subscribers += len(subscribers_data["contacts"])

            for subscriber in subscribers_data["contacts"]:
                print(f"Fetching notes for subscriber {subscriber['id']}...")
                subscriber_notes = get_notes_for_subscriber(subscriber["id"])

                # Write notes to CSV immediately, checking for duplicates
                with open("activecampaign_notes.csv", "a", newline="") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    with open("activecampaign_notes.csv", "r", newline="") as csvfile_read:  # Open for reading only
                        existing_rows = set(tuple(row.values()) for row in csv.DictReader(csvfile_read))
                    for note in subscriber_notes:
                        note_id = note["id"]
                        existing_row = (subscriber["id"], note_id)
                        if existing_row not in existing_rows:
                            writer.writerow({
                                "subscriber_id": subscriber["id"],
                                "subscriber_email": subscriber.get("email", "No email provided"),
                                "note_id": note["id"],
                                "note_body": note["note"]
                            })
                            existing_rows.add(existing_row)  # Update existing rows

            offset += 100
        else:
            print(f"Error fetching subscribers: {response_subscribers.status_code}")
            break

    print(f"Total subscribers processed: {total_subscribers}")

if __name__ == "__main__":
    main()
