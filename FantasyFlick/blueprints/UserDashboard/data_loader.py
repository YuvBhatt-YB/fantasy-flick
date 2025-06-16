
import requests
from FantasyFlick.app import db
from FantasyFlick.blueprints.UserDashboard.models import Match
from FantasyFlick.blueprints.UserDashboard.models import Player
from FantasyFlick.blueprints.UserDashboard.models import Contest
from FantasyFlick.blueprints.UserDashboard.utils import convert_dt

import os
API_KEY = os.environ.get("API_KEY")
def get_matches():
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
    querystring = {"Category":"cricket","Date":"20250603","Timezone":"5.5"}
    headers = {
	"x-rapidapi-key": API_KEY,
	"x-rapidapi-host": "livescore6.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    
    
    matches = [
        {
            "series_name":stage["Snm"],
            "match_name":stage["Cnm"],
            "match_id":stage["Events"][0]["Eid"],
            "team_1":stage["Events"][0]["T1"][0]["Nm"],
            "team_1_short":stage["Events"][0]["T1"][0]["Abr"],
            "team_2":stage["Events"][0]["T2"][0]["Nm"],
            "team_2_short":stage["Events"][0]["T2"][0]["Abr"],
            "start_time": convert_dt(str(stage["Events"][0]["Ese"])),
    }
    for stage in data["Stages"]
    ]
    
    for match in matches :
        existing_match  = Match.query.filter(Match.match_id == match["match_id"]).first() 
        existing_contest = Contest.query.filter(Contest.match_id == match["match_id"]).first()
        
        if existing_match and existing_contest:
            continue 

        m = Match(match_id = match["match_id"],match_name=match["match_name"],series_name=match["series_name"],team1=match["team_1"],team2=match["team_2"],team1_short=match["team_1_short"],team2_short=match["team_2_short"],start_time=match["start_time"])
        
        contest = Contest(match_id=m.match_id,entry_fee=100,max_participants=100,prize_pool=10000)
        db.session.add(m)
        db.session.add(contest)
        db.session.commit()

def get_match_players(match_id,team_1,team_2):
    match = Match.query.filter(Match.match_id==match_id).first()
    players = Player.query.filter(Player.match_id == match_id).first()
    if not players:
        url = "https://livescore6.p.rapidapi.com/matches/v2/get-lineups"
        querystring = {"Category":"cricket","Eid":f"{match_id}"}
        headers = {
	    "x-rapidapi-key": API_KEY,
	    "x-rapidapi-host": "livescore6.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        teams = [(team_1,data["Lu"][0]["Ps"]),(team_2,data["Lu"][1]["Ps"])]
        players = [
            {
                "player_id":player["Pid"],
                "player_name":player["Snm"],
                "player_team":team_name,
                "player_base_value":10,
                "match_id": match.match_id
            }
        for team_name,team_players in teams
        for player in team_players
        ]
        for player in players:
            p = Player(player_id=player["player_id"],name=player["player_name"],team=player["player_team"],base_value=player["player_base_value"],match_id=player["match_id"])
            db.session.add(p)
            db.session.commit()

