# import libraries
from bs4 import BeautifulSoup
import requests
import csv

# input date from user
date = input("Please enter the date in the following of this format MM/DD/YYYY :")
# url of the page to script
url = f"https://www.yallakora.com/match-center?date={date}"

# send a get requests to the url
page = requests.get(url)
def main(page):
    # get the page content
    src = page.content
    # parse the page using BeautifulSoup
    soup = BeautifulSoup(src, "lxml")
    # create info list to store the data
    matches_details = []
    # get the championships blocks
    championships = soup.find_all("div", {"class": "matchCard"})

    def get_match_info(championships):
        # get championship name
        championship_name = championships.contents[1].find("h2").text.strip()
        # get info all matches
        all_matches = championships.contents[3].find_all(
            "div", {"class": "item finish liItem"}
        )
        number_of_matches = len(all_matches)
        for index in range(number_of_matches):
            # get round number
            round_number = (
                all_matches[index].find("div", {"class": "date"}).text.strip()
                if all_matches[index].find("div", {"class": "date"})
                else "N/A"
            )
            # get match status
            match_status = (
                all_matches[index].find("div", {"class": "matchStatus"}).text.strip()
                if all_matches[index].find("div", {"class": "matchStatus"})
                else "N/A"
            )

            # get channel
            channel = (
                all_matches[index].find("div", {"class": "channel"}).text.strip()
                if all_matches[index].find("div", {"class": "channel"})
                else "N/A"
            )

            # get teamA
            teamA = (
                all_matches[index].find("div", {"class": "teamA"}).text.strip()
                if all_matches[index].find("div", {"class": "teamA"})
                else "N/A"
            )
            # get teamA
            teamB = (
                all_matches[index].find("div", {"class": "teamB"}).text.strip()
                if all_matches[index].find("div", {"class": "teamB"})
                else "N/A"
            )
            # get result
            scores = (
                all_matches[index]
                .find("div", {"class": "MResult"})
                .find_all("span", {"class": "score"})
            )
            if scores:
                match_result = f"{scores[0].text.strip()} - {scores[1].text.strip() }"
            else:
                match_result = "N/A"

            # get match time
            match_time = (
                all_matches[index].find("span", {"class": "time"}).text.strip()
                if all_matches[index].find("span", {"class": "time"})
                else "N/A"
            )

            # add match info in matches_details list
            matches_details.append(
                {
                    "نوع البطولة": championship_name,
                    "الجولة": round_number,
                    "حالة المبارة": match_status,
                    "القناة": channel,
                    "الفريق الاول": teamA,
                    "الفريق الثاني": teamB,
                    "الوقت": match_time,
                    "النتيجة": match_result,
                }
            )

    for index in range(len(championships)):
        get_match_info(championships[index])

    keys = matches_details[0].keys()

    with open("matches_details.csv", "w", encoding="utf-8-sig", newline="") as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("file created")


main(page)