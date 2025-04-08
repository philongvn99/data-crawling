"""This module provides classes to represent and process data related to English Premier League 
(EPL) matches, including match information, team details, and match statistics.

Classes:
    Ground:

    TeamInfo:
        Represents information about a football team, including its name, short name, and unique 
        identifier.

    MatchInfo:
        Represents match information for an EPL game, including details such as game week, season, 
        league, kickoff time, ground, and attendance.

    Statistic:
        Represents statistical data for a football match, including goals, shots, corners, fouls, 
        and cards.

    TeamStat:
        Represents a team's information and statistics for a match, combining team details and 
        match statistics.

    MatchStatistic:
        Represents and processes match statistics for two teams in a football match, including 
        methods to extract and assign detailed statistics.

Usage:
    These classes are designed to parse and represent data from a structured dictionary format, 
    typically obtained from an external data source. They provide a structured way to access and 
    manipulate match-related data for analysis or further processing."""
import datetime


class Ground:
    """
    Represents a football ground with its name and city.
    Attributes:
        name (str): The name of the ground.
        city (str): The city where the ground is located.
    Methods:
        __init__(data):
            Initializes a Ground instance with the provided data dictionary.
    """

    def __init__(self, data):
        self.name = data["name"]
        self.city = data["city"]


class TeamInfo:
    """
    A class to represent information about a football team.
    Attributes:
        name (str): The full name of the team.
        short_name (str): The short name or abbreviation of the team.
        id (int): The unique identifier for the team.
    Methods:
        __init__(data):
            Initializes the TeamInfo object with data from a dictionary.
    """
    name: str
    short_name: str
    id: int

    def __init__(self, data):
        self.id = data["team"]["id"]
        self.name = data["team"]["name"]
        self.short_name = data["team"]["shortName"]


class MatchInfo:
    """
    A class to represent match information for an English Premier League (EPL) game.
    Attributes:
        game_week_id (int): The unique identifier for the game week.
        match_id (int): The unique identifier for the match.
        season (str): The season label (e.g., "2022/23").
        round (int): The round number of the match within the season.
        league (str): The league description (e.g., "Premier League").
        kickoff (str): The kickoff date and time in the format "dd/mm/yyyy".
        ground_name (Ground): The ground where the match is played.
        attendance (int): The number of attendees at the match.
    Methods:
        __init__(data):
            Initializes a MatchInfo object using the provided match data.
    """

    game_week_id: int
    match_id: int
    season: str
    round: int
    league: str
    kickoff: str
    ground_name: Ground
    attendance: int

    def __init__(self, data):
        gameweek = data["gameweek"]
        self.game_week_id = gameweek["id"]
        self.match_id = data["id"]
        self.season = gameweek["compSeason"]["label"]
        self.round = gameweek["gameweek"]
        self.league = gameweek["compSeason"]["competition"]["description"]
        self.kickoff = datetime.datetime.strptime(
            data["kickoff"]["label"][:-4], "%a %d %b %Y, %H:%M"
        ).strftime("%d/%m/%Y")
        self.ground_name = Ground(data["ground"])
        self.attendance = data.get("attendance", 0)


class Statistic:
    """
    A class to represent statistical data for a football match.
    Attributes:
        ftg (int): Full-time goals scored. Default is 0.
        htg (int): Half-time goals scored. Default is 0.
        sh (int): Total number of shots. Default is 0.
        sot (int): Total number of shots on target. Default is 0.
        co (int): Total number of corners. Default is 0.
        fo (int): Total number of fouls committed. Default is 0.
        yc (int): Total number of yellow cards received. Default is 0.
        rc (int): Total number of red cards received. Default is 0.
    Methods:
        __init__(ftg=0, htg=0, sh=0, sot=0, co=0, fo=0, yc=0, rc=0):
            Initializes a Statistic object with the given values or defaults.
    """
    ftg: int  # fulltime goal
    htg: int  # halftime goal
    sh: int  # shot
    sot: int  # shot on target
    co: int  # corner
    fo: int  # foul
    yc: int  # yellow carde
    rc: int  # red card

    def __init__(self, ftg=0, htg=0, sh=0, sot=0, co=0, fo=0, yc=0, rc=0):
        self.ftg = ftg
        self.htg = htg
        self.sh = sh
        self.sot = sot
        self.co = co
        self.fo = fo
        self.yc = yc
        self.rc = rc


class TeamStat:
    """Represents a team's information and statistics for a match."""
    info: TeamInfo
    stats: Statistic

    def __init__(self, data: dict):
        self.info = TeamInfo(data)
        self.stats = Statistic()


class MatchStatistic:
    """
    A class to represent and process match statistics for two teams in a football match.
    Attributes:
        match (MatchInfo): Information about the match.
        team1 (TeamStat): Statistics for the first team.
        team2 (TeamStat): Statistics for the second team.
    Methods:
        __init__(data: dict):
            Initializes the MatchStatistic object with match and team data.
        get_stats(data: dict):
            Extracts and assigns detailed statistics for both teams from the provided data.
    """

    match: MatchInfo
    team1: TeamStat
    team2: TeamStat

    def __init__(self, data: dict):
        self.match = MatchInfo(data["entity"])

        self.team1 = TeamStat(data["entity"]["teams"][0])
        self.team2 = TeamStat(data["entity"]["teams"][1])

        self.team1.stats.ftg = data["entity"]["teams"][0]["score"]
        self.team2.stats.ftg = data["entity"]["teams"][1]["score"]

    def get_stats(self, data):
        """
        Extracts and assigns statistical data for two teams from the provided data.
        This method processes the input data to retrieve specific statistics for 
        `team1` and `team2` and assigns the values to their respective attributes.
        Args:
            data (dict): A dictionary containing match statistics. The structure 
                         is expected to have a "data" key, which maps to another 
                         dictionary where team IDs are keys, and their values 
                         contain a list of statistics under the "M" key.
        Expected Statistics:
            - "first_half_goals": Number of goals scored in the first half.
            - "total_scoring_att": Total scoring attempts.
            - "ontarget_scoring_att": Scoring attempts on target.
            - "total_corners_intobox": Total corners into the box.
            - "fk_foul_lost": Fouls lost.
            - "total_yel_card": Total yellow cards.
            - "total_red_card": Total red cards.
        Attributes Updated:
            - `self.team1.stats` and `self.team2.stats` are updated with the 
              corresponding values for each statistic.
        Raises:
            KeyError: If the expected keys are not found in the input data.
        """

        for stat in data["data"][str(self.team1.info.id)]["M"]:
            if stat["name"] == "first_half_goals":
                self.team1.stats.htg = stat["value"]
            elif stat["name"] == "total_scoring_att":
                self.team1.stats.sh = stat["value"]
            elif stat["name"] == "ontarget_scoring_att":
                self.team1.stats.sot = stat["value"]
            elif stat["name"] == "total_corners_intobox":
                self.team1.stats.co = stat["value"]
            elif stat["name"] == "fk_foul_lost":
                self.team1.stats.fo = stat["value"]
            elif stat["name"] == "total_yel_card":
                self.team1.stats.yc = stat["value"]
            elif stat["name"] == "total_red_card":
                self.team1.stats.rc = stat["value"]

        for stat in data["data"][str(self.team2.info.id)]["M"]:
            if stat["name"] == "first_half_goals":
                self.team2.stats.htg = stat["value"]
            elif stat["name"] == "total_scoring_att":
                self.team2.stats.sh = stat["value"]
            elif stat["name"] == "ontarget_scoring_att":
                self.team2.stats.sot = stat["value"]
            elif stat["name"] == "total_corners_intobox":
                self.team2.stats.co = stat["value"]
            elif stat["name"] == "fk_foul_lost":
                self.team2.stats.fo = stat["value"]
            elif stat["name"] == "total_yel_card":
                self.team2.stats.yc = stat["value"]
            elif stat["name"] == "total_red_card":
                self.team2.stats.rc = stat["value"]
