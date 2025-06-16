from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os


load_dotenv()
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__,static_folder="static",template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SECRET_KEY"] = os.urandom(24)
    
    db.init_app(app)
    bcrypt.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from FantasyFlick.blueprints.Auth.models import User
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    


    #register Blueprints
    from FantasyFlick.blueprints.HomePage.routes import HomePage
    from FantasyFlick.blueprints.Auth.routes import Auth
    from FantasyFlick.blueprints.UserDashboard.routes import UserDashboard
    from FantasyFlick.blueprints.Contests.routes import Contests
    from FantasyFlick.blueprints.LeaderBoard.routes import LeaderBoard
    from FantasyFlick.blueprints.UserProfile.routes import UserProfile
    app.register_blueprint(HomePage,url_prefix="/")
    app.register_blueprint(Auth,url_prefix="/auth")
    app.register_blueprint(UserDashboard,url_prefix="/user")
    app.register_blueprint(Contests,url_prefix="/contests")
    app.register_blueprint(LeaderBoard,url_prefix="/")
    app.register_blueprint(UserProfile,url_prefix="/profile")

    migrate = Migrate(app,db)
    return app