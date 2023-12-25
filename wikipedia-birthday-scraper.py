import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_celebrity_info(celebrity_name):
    # Convert names without underscores to match Wikipedia naming convention
    wikipedia_name = celebrity_name.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{wikipedia_name}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the HTTP request fails
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the HTTP request for {celebrity_name}:", e)
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    birthdate_element = soup.find("span", class_="bday")
    
    if birthdate_element is None:
        print(f"Birthdate element not found for {celebrity_name}")
        return None
    
    try:
        birthdate = birthdate_element.text
        print(f"The raw birthdate of {celebrity_name} is: {birthdate}")
        zodiac_sign, date_range = get_zodiac_sign(birthdate)
        print(f"The zodiac sign of {celebrity_name} is: {zodiac_sign} ({date_range})")
        return {'Celebrity Name': celebrity_name, 'Birthdate': birthdate, 'Zodiac Sign': zodiac_sign, 'Date Range': date_range}
    except AttributeError:
        print(f"Error occurred while accessing the birthdate element for {celebrity_name}")
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

# List of celebrities
celebrities = [
    "Emma Watson",
    "Chris Hemsworth",
    "Zendaya",
    "Ryan Reynolds",
    "Scarlett Johansson",
    "Keanu Reeves",
    "Priyanka Chopra",
    "Dwayne Johnson",
    "Gal Gadot",
    "Leonardo DiCaprio",
    "Margot Robbie",
    "Robert Downey Jr.",
    "Natalie Portman",
    "Tom Holland",
    "Charlize Theron",
    "Jason Momoa",
    "Taylor Swift",
    "Johnny Depp",
    "Angelina Jolie",
    "Elon Musk"
]

# List to store data for all celebrities
data_list = []

# Loop through each celebrity
for celebrity in celebrities:
    celebrity_info = get_celebrity_info(celebrity)
    if celebrity_info:
        data_list.append(celebrity_info)

# Create a DataFrame from the list of data
df = pd.DataFrame(data_list)

# Save the DataFrame to an Excel file
df.to_excel("celebrities_info_with_zodiac.xlsx", index=False)
print("Data saved to celebrities_info_with_zodiac.xlsx")
