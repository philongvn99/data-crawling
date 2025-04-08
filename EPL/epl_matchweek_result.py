""" 
from the Premier League website and processes the data into a structured format.
This script fetches and processes match statistics for a specified Premier League match week
and writes the data to a CSV file. It utilizes web scraping techniques to extract match data

Modules:
- argparse: For parsing command-line arguments.
- csv: For writing match statistics to a CSV file.
- urllib.request: For sending HTTP requests and handling responses.
- bs4(BeautifulSoup): For parsing HTML content.
- fake_useragent: For generating random user agents for HTTP requests.

Classes:
- MatchStatistic: A class (imported from EPL.epl_match_result) used to process and store
    match statistics.

Functions:
- manipulate_stats(data: MatchStatistic, ref: str): Processes match statistics data and
    extracts relevant information into a list format.
- main(match_week: int): Fetches match statistics for a given match week, processes the
    data, and writes it to a CSV file.

Command-line Arguments:
- -mw, --match_week: Specifies the match week number for which statistics are to be fetched.

CSV Output:
- The script generates a CSV file named `match_stats_ < match_week > .csv` in the `crawling/data/`
    directory. The CSV contains the following fields:
    - Season, Date, HomeTeam, AwayTeam, FTHG, FTAG, HTHG, HTAG, Referee, HS, AS, HST, AST, HC,
        AC, HF, AF, HY, AY, HR, AR.

- The script requires the `fake_useragent` and `bs4` libraries to be installed.
- It assumes the existence of the `MatchStatistic` class and its `get_stats` method for
    processing match data.

Usage:
- Run the script from the command line and provide the match week number as an argument:
    `python epl_matchweek_result.py - mw < match_week_number >`

Notes:
- The script uses BeautifulSoup to parse HTML content and extract match fixtures and referee
    information.
- It sends HTTP requests to the Premier League website and an API endpoint to fetch match
    data.
- The match week number is adjusted by adding 18389 to align with the Premier League's
    internal match week numbering system."""

import argparse
import csv
import json
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from epl_match_result import MatchStatistic
from fake_useragent import UserAgent

# Initialize User Agent
ua = UserAgent()

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-mw", "--match_week", help="match_week")

# Read arguments from command line
args = parser.parse_args()


def manipulate_stats(data: MatchStatistic, ref: str):
    """Manipulates the match statistics data to extract relevant information.
    Args:
        data(MatchStatistic): An instance of MatchStatistic containing match data.
        ref(str): The referee's name."""
    return [
        data.match.season,
        data.match.kickoff,
        data.team1.info.short_name,
        data.team2.info.short_name,
        data.team1.stats.ftg,
        data.team2.stats.ftg,
        data.team1.stats.htg,
        data.team2.stats.htg,
        ref,
        data.team1.stats.sh,
        data.team2.stats.sh,
        data.team1.stats.sot,
        data.team2.stats.sot,
        data.team1.stats.co,
        data.team2.stats.co,
        data.team1.stats.fo,
        data.team2.stats.fo,
        data.team1.stats.yc,
        data.team2.stats.yc,
        data.team1.stats.rc,
        data.team2.stats.rc,
    ]


def main(match_week):
    """
    Fetches and processes match statistics for a given Premier League match week.

    This function retrieves match statistics from the Premier League website for a
    specified match week and writes the data to a CSV file. It uses BeautifulSoup to
    parse HTML content and extract relevant data, and urllib to handle HTTP requests
    and responses. Additionally, it employs fake_useragent to generate random user
    agents for the requests.

    Args:
        match_week(int): The match week number for which statistics are to be fetched.

    Functionality:
    - Constructs the URL for the specified match week and fetches the match fixtures.
    - Extracts match IDs from the fixtures and iterates through each match to fetch
      detailed statistics.
    - Retrieves various match statistics such as season, date, teams, goals, referee,
      shots, cards, etc.
    - Writes the extracted statistics to a CSV file named `match_stats_ < match_week > .csv`
      in the `crawling/data /` directory.

    CSV File Fields:
    - Season, Date, HomeTeam, AwayTeam, FTHG, FTAG, HTHG, HTAG, Referee, HS, AS, HST,
      AST, HC, AC, HF, AF, HY, AY, HR, AR.

    Dependencies:
    - urllib: For sending HTTP requests and handling responses.
    - BeautifulSoup: For parsing HTML content.
    - fake_useragent: For generating random user agents.
    - json: For processing JSON responses.

    Note:
    - The function assumes the existence of helper functions `MatchStatistic.get_stats`
      and `manipulate_stats` to process and format the match statistics.
    - The function is intended to be called from the main block with the match week as
      an argument.
    """
    match_week_req = Request(
        f"https://www.premierleague.com/matchweek/{match_week}/blog?match=true"
    )
    match_week_req.add_header("User-Agent", ua.random)
    with urlopen(match_week_req) as match_week_doc:
        match_id_list = list(
            m.attrs["href"]
            for m in BeautifulSoup(
                match_week_doc.read().decode("utf8"), "html.parser"
            ).select("a.match-fixture--abridged")
        )

        filename = f"EPL/data/match_stats_{match_week}.csv"
        fields = [
            "Season",
            "Date",
            "HomeTeam",
            "AwayTeam",
            "FTHG",
            "FTAG",
            "HTHG",
            "HTAG",
            "Referee",
            "HS",
            "AS",
            "HST",
            "AST",
            "HC",
            "AC",
            "HF",
            "AF",
            "HY",
            "AY",
            "HR",
            "AR",
        ]

        # writing to csv file
        with open(filename, "w", encoding="utf-8") as csvfile:
            # creating a csv dict writer object
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(fields)

            # writing data rows

            for i in match_id_list:
                match_stat_req = Request(f"https://www.premierleague.com{i}")
                match_stat_req.add_header("User-Agent", ua.random)
                with urlopen(match_stat_req) as uo:
                    ref = list(
                        t.text.strip()
                        for t in BeautifulSoup(
                            uo.read().decode("utf8"), "html.parser"
                        ).find_all(class_="mc-summary__info")
                    )[-1].split(": ")[-1]

                    match_stat_req = Request(
                        f"https://footballapi.pulselive.com/football/stats{i}"
                    )
                    match_stat_req.add_header(
                        "User-Agent",
                        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
                    )
                    match_stat_req.add_header(
                        "Origin", "https://www.premierleague.com")
                    match_stat_req.add_header(
                        "Content-Type",
                        "application/x-www-form-urlencoded; charset=UTF-8",
                    )
                    match_stat_req.add_header(
                        "Referer",
                        "https://www.premierleague.com//clubs/1/Arsenal/squad?se=79",
                    )
                    with urlopen(match_stat_req) as sub_uo:
                        match_info = json.loads(sub_uo.read().decode("utf8"))

                        match_stats = MatchStatistic(match_info)
                        match_stats.get_stats(match_info)

                        writer.writerow(manipulate_stats(match_stats, ref))


if __name__ == "__main__":
    matchWeek = int(args.match_week)
    main(matchWeek + 18389)
    print("Finish!")
