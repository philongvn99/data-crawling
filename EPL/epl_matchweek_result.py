import argparse
import csv
import json
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from EPL.epl_match_result import MatchStatistic

# Initialize User Agent
ua = UserAgent()

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-mw", "--match_week", help="match_week")

# Read arguments from command line
args = parser.parse_args()


def manipulate_stats(data: MatchStatistic, ref: str):
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

        filename = f"crawling/data/match_stats_{match_week}.csv"
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
                        ).findAll(class_="mc-summary__info")
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
