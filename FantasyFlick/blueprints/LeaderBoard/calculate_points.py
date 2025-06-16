import requests
from FantasyFlick.blueprints.UserDashboard.models import FantasyTeam
from FantasyFlick.blueprints.UserDashboard.models import FantasyTeamPlayer
import os
API_KEY = os.environ.get("API_KEY")
def fetch_match_data(match_id):
    url = "https://livescore6.p.rapidapi.com/matches/v2/get-innings"

    querystring = {"Category":"cricket","Eid":f"{match_id}"}

    headers = {
	    "x-rapidapi-key": API_KEY,
	    "x-rapidapi-host": "livescore6.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    return data

def get_player_stats(data,player_id):
    batting_stats = {}
    bowling_stats = {}

    for innings in data["SDInn"]:
        for player in innings["Bat"]:
            if player["Pid"] == player_id:
                for key,value in player.items():
                    if key == "Pid":
                        continue
                    if key in batting_stats and isinstance(value,(int,float)):
                        batting_stats[key] +=value
                    else:
                        batting_stats[key] = value
        for player in innings["Bow"]:
            if player["Pid"] == player_id:
                for key,value in player.items():
                    if key == "Pid":
                        continue
                    if key in bowling_stats and isinstance(value,(int,float)):
                        bowling_stats[key] +=value
                    else:
                        bowling_stats[key] = value
    
    result = {}
    if batting_stats:
        batting_stats["Pid"] = player_id
        result["Batting"] = batting_stats

    if bowling_stats:
        bowling_stats["Pid"] = player_id
        result["Bowling"] = bowling_stats
    
    return result

def calculate_fantasy_points(player_stats):

    points = 0
    batting = player_stats.get("Batting")
    if batting:
        r = batting.get("R",0)
        fours = batting.get("$4",0)
        sixes = batting.get("$6",0)
        balls = batting.get("B",0)
        sr = batting.get("Sr",0)
        
        points += r*1
        points += fours*2
        points += sixes*3

        if r>100:
            points+=20
        if r>50:
            points+=10
        if r ==0 :
            points-=2

        if balls > 10:
            if sr >130:
                points +=4
            elif sr >=100:
                points +=2

    bowling = player_stats.get("Bowling")
    if bowling:
        wkts = bowling.get("Wk",0)
        maidens = bowling.get("Md",0)
        economy = bowling.get("Er",0)

        points += wkts*25
        points += maidens*8

        if economy<4:
            points+=6
        elif economy<5:
            points+=4
        elif economy<6:
            points+=2
        elif economy>10:
            points-=4
        elif economy>9:
            points-=2

    return points

def generate_leaderboard(match_id):
    match_data = fetch_match_data(match_id)
    fantasy_teams = FantasyTeam.query.filter(FantasyTeam.match_id == match_id).all()
    player_stats_map = {}

    for team in fantasy_teams:
        players = FantasyTeamPlayer.query.filter(FantasyTeamPlayer.fantasy_team_id == team.id).all()
        for p in players:
            if p.player_id not in player_stats_map:
                player_stats_map[p.player_id] = get_player_stats(match_data,p.player_id)

    leaderboard_data = []

    for team in fantasy_teams:
        players = FantasyTeamPlayer.query.filter(FantasyTeamPlayer.fantasy_team_id == team.id).all()
        total_points = 0

        for p in players:
            stats = player_stats_map[p.player_id]
            points = calculate_fantasy_points(stats)

            if p.player_id == team.captain_id:
                points*=2
            if p.player_id == team.vice_captain_id:
                points*=1.5

            total_points +=points

        leaderboard_data.append({
            "team_name" : team.team_name,
            "user_name" : team.user.username,
            "total_points": round(total_points,2)
        })

    leaderboard_data.sort(key=lambda x:x["total_points"],reverse=True)    
    return leaderboard_data

