import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_person_info(person_name):
    # Convert names without underscores to match Wikipedia naming convention
    wikipedia_name = person_name.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{wikipedia_name}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the HTTP request fails
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the HTTP request for {person_name}:", e)
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    birthdate_element = soup.find("span", class_="bday")
    
    if birthdate_element is None:
        print(f"Birthdate element not found for {person_name}")
        return None
    
    try:
        birthdate = birthdate_element.text
        print(f"The raw birthdate of {person_name} is: {birthdate}")
        zodiac_sign, date_range = get_zodiac_sign(birthdate)
        print(f"The zodiac sign of {person_name} is: {zodiac_sign} ({date_range})")
        return {'Person Name': person_name, 'Birthdate': birthdate, 'Zodiac Sign': zodiac_sign, 'Date Range': date_range}
    except AttributeError:
        print(f"Error occurred while accessing the birthdate element for {person_name}")
        return None

def get_zodiac_sign(birthdate):
    print(f"Processing birthdate: {birthdate}")
    day, month, _ = map(int, birthdate.split('-'))
    
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries", "March 21 - April 19"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus", "April 20 - May 20"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini", "May 21 - June 20"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer", "June 21 - July 22"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo", "July 23 - August 22"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo", "August 23 - September 22"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra", "September 23 - October 22"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio", "October 23 - November 21"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius", "November 22 - December 21"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn", "December 22 - January 19"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius", "January 20 - February 18"
    else:
        return "Pisces", "February 19 - March 20"

# File name
file_name = "people_info_with_zodiac.xlsx"

# List of names
names = [
    "Napoleon Bonaparte",
    "Rosa Parks",
    "Winston Churchill",
    "Mao Zedong",
    "Fidel Castro",
    "Indira Gandhi",
    "Mother Teresa",
    "Michael Jackson",
    "Oprah Winfrey",
    "Pele",
    "Bill Gates",
    "Malala Yousafzai",
    "Stephen Hawking",
    "Albert Camus",
    "Billie Holiday",
    "Freddie Mercury",
    "Ruth Bader Ginsburg",
    "Diego Maradona",
    "J.K. Rowling",
    "Vincent Price"
]



# Check if the file exists
if os.path.exists(file_name):
    # Read existing data into a DataFrame
    existing_df = pd.read_excel(file_name)
    data_list = existing_df.to_dict(orient='records')
else:
    # Create an empty list to store data
    data_list = []

# Loop through each name
for name in names:
    person_info = get_person_info(name)
    if person_info:
        data_list.append(person_info)

# Create a DataFrame from the list of data
df = pd.DataFrame(data_list)

# Save the DataFrame to the file
df.to_excel(file_name, index=False)
print(f"Data saved to {file_name}")