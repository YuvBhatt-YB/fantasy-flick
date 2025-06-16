from flask  import render_template,Blueprint,request,flash,redirect,url_for
from flask_login import login_required,current_user
from FantasyFlick.app import db


UserProfile = Blueprint("UserProfile",__name__,template_folder="templates")

@UserProfile.route("/")
@login_required
def index():
    return render_template("UserProfile/index.html",current_user=current_user)

@UserProfile.route("/add_balance",methods=["POST"])
@login_required
def add_balance():
    amount = int(request.form["balance"])
    if amount > 0:
        current_user.wallet_balance += amount 
        db.session.commit()
        flash(f"{amount} coins added to your balance")
    elif amount > 10000:
        flash(f"{amount} must not be greater than 10,000 coins")
    elif amount ==0 or amount=="":
        flash(f"Please enter your amount")
    else:
        flash(f"Amount must be positive")

    return redirect(url_for("UserProfile.index"))