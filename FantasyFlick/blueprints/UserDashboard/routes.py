from flask import render_template,Blueprint,request,redirect,url_for
from flask_login import login_required,current_user
from FantasyFlick.blueprints.UserDashboard.data_loader import get_matches
from FantasyFlick.blueprints.UserDashboard.models import Match
from FantasyFlick.blueprints.UserDashboard.models import Player
from FantasyFlick.blueprints.UserDashboard.models import FantasyTeam
from FantasyFlick.blueprints.UserDashboard.models import FantasyTeamPlayer
from FantasyFlick.blueprints.UserDashboard.models import UserContest
from FantasyFlick.blueprints.UserDashboard.models import Contest
from FantasyFlick.blueprints.UserDashboard.data_loader import get_match_players
from FantasyFlick.app import db
import json


UserDashboard = Blueprint("UserDashboard",__name__,template_folder="templates")

@UserDashboard.route("/")
@login_required
def index():
    get_matches()
    matches = Match.query.all()
    return render_template("UserDashboard/index.html",current_user=current_user,matches=matches)

@UserDashboard.route("/match/<int:match_id>")
@login_required
def match(match_id):
    match = Match.query.filter(Match.match_id == match_id).first()
    get_match_players(match_id=match_id,team_1=match.team1,team_2=match.team2)
    players = Player.query.filter(Player.match_id == match_id).all()

    return render_template("UserDashboard/match.html",players=players,match_id=match_id)

@UserDashboard.route("/match/<int:match_id>/review",methods=["POST"])
@login_required
def review(match_id):
    players_list_json = request.form.get("players_json")
    selected_players = json.loads(players_list_json)
    captain= request.form["captain"]
    vice_captain = request.form["vice_captain"]
    team_name = request.form["team_name"]
    return render_template("UserDashboard/review.html",players=selected_players,captain=captain,vice_captain=vice_captain,match_id=match_id,players_list_json=players_list_json,team_name=team_name)

@UserDashboard.route("/match/<int:match_id>/create_fantasy_team",methods=["POST"])
@login_required
def create_fantasy_team(match_id):
    players_list = request.form.get("players")
    players = json.loads(players_list)
    captain= request.form["captain"]
    captain_id = None
    vice_captain_id = None
    vice_captain = request.form["vice_captain"]
    team_name = request.form["team_name"]
    for p in players:
        if p["name"] == captain:
            captain_id = p["id"]
        elif p["name"] == vice_captain:
            vice_captain_id =p["id"]
    

    

    fantasy_team = FantasyTeam(user_id=current_user.uid,match_id=match_id,captain_id=captain_id,vice_captain_id=vice_captain_id,team_name=team_name)
    db.session.add(fantasy_team)
    db.session.commit()

    for player in players:
        fantasy_team_player = FantasyTeamPlayer(fantasy_team_id=fantasy_team.id,player_id=player["id"])
        db.session.add(fantasy_team_player)
        db.session.commit()

    contest = Contest.query.filter(Contest.match_id == match_id).first()
    current_user.wallet_balance = int(current_user.wallet_balance - contest.entry_fee)
    user_contest = UserContest(user_id=current_user.uid,contest_id=contest.id,fantasy_team_id=fantasy_team.id)
    db.session.add(user_contest)
    db.session.commit()

    

    return redirect(url_for('UserDashboard.index'))

