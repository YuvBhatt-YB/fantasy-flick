from flask  import render_template,Blueprint
from flask_login import login_required,current_user
from FantasyFlick.blueprints.UserDashboard.models import FantasyTeamPlayer
from FantasyFlick.blueprints.UserDashboard.models import FantasyTeam
Contests = Blueprint("Contests",__name__,template_folder="templates")

@Contests.route("/")
@login_required
def index():
    user_contests = current_user.joined_contests
    return render_template("Contests/index.html",user_contests=user_contests,current_user=current_user)

@Contests.route("/lineup/<fantasy_team_id>")
@login_required
def lineup(fantasy_team_id):
    fantasy_team_players = FantasyTeamPlayer.query.filter(FantasyTeamPlayer.fantasy_team_id == fantasy_team_id).all()
    fantasy_team = FantasyTeam.query.filter(FantasyTeam.id == fantasy_team_id).first()
    return render_template("Contests/lineup.html",fantasy_team_players=fantasy_team_players,fantasy_team=fantasy_team)