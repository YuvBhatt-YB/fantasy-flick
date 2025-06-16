from flask  import render_template,Blueprint
from flask_login import login_required,current_user
from FantasyFlick.blueprints.LeaderBoard.calculate_points import generate_leaderboard

LeaderBoard = Blueprint("LeaderBoard",__name__,template_folder="templates")

@LeaderBoard.route("/<int:match_id>/leaderboard")
@login_required
def index(match_id):
    data = generate_leaderboard(match_id)
    return render_template("LeaderBoard/index.html",data=data)

