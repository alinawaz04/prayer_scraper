import requests
from bs4 import BeautifulSoup
import time

url = "https://isnok.org/"
timeout = 15  # Maximum time to wait in seconds
check_interval = 5  # Time to wait between checks in seconds
elapsed_time = 0

while elapsed_time < timeout:
    response = requests.get(url)
    print(f"Status code: {response.status_code}, Elapsed time: {elapsed_time} seconds")
    
    if response.status_code == 200:
        # Process the data as before
        soup = BeautifulSoup(response.text, "html.parser")
        prayer_times_table = soup.find("table")
        if prayer_times_table:  # Ensure the table exists
            prayer_rows = prayer_times_table.find_all("tr")[3:]
            for row in prayer_rows:
                columns = row.find_all("td")
                if columns:
                    prayer_name = columns[0].text.strip()
                    prayer_time = columns[1].text.strip()
                    jamah_time = columns[2].text.strip()
                    print(f"{prayer_name}: {prayer_time} {jamah_time}")
        break  # Exit the loop since data was processed
    elif response.status_code == 202:
        # Wait before trying again if the status code is 202 (Accepted)
        time.sleep(check_interval)
        elapsed_time += check_interval
    else:
        # Handle other HTTP status codes as needed
        print(f"Unexpected status code: {response.status_code}")
        break  # Exit the loop for unexpected status codes

if elapsed_time >= timeout:
    print("Timeout reached without receiving a 200 OK response.")
