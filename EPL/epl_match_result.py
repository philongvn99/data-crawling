import datetime


class Ground:
    def __init__(self, data):
        self.name = data["name"]
        self.city = data["city"]


class TeamInfo:
    name: str
    short_name: str
    id: int

    def __init__(self, data):
        self.id = data["team"]["id"]
        self.name = data["team"]["name"]
        self.short_name = data["team"]["shortName"]


class MatchInfo:
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
    ftg: int  # fulltime goal
    htg: int  # halftime goal
    sh: int  # shot
    sot: int  # shot on target
    co: int  # corner
    fo: int  # foul
    yc: int  # yellow carde
    rc: int  # red card

    def __init__(self):
        self.ftg = 0
        self.htg = 0
        self.sh = 0
        self.sot = 0
        self.co = 0
        self.fo = 0
        self.yc = 0
        self.rc = 0


class TeamStat:
    info: TeamInfo
    stats: Statistic

    def __init__(self, data: dict):
        self.info = TeamInfo(data)
        self.stats = Statistic()


class MatchStatistic:
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
