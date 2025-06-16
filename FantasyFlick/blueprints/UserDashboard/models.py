from FantasyFlick.app import db
from FantasyFlick.blueprints.Auth.models import User

class Match(db.Model):
    __tablename__ = "matches"

    match_id = db.Column(db.Integer,primary_key=True)
    match_name = db.Column(db.String)
    series_name = db.Column(db.String)
    team1 = db.Column(db.String)
    team2 = db.Column(db.String)
    team1_short = db.Column(db.String)
    team2_short = db.Column(db.String)
    start_time = db.Column(db.String)
    players = db.relationship("Player",backref="match",lazy=True)

    def __repr__(self):
        return f"<Match id : {self.match_id} , Match name: {self.match_name} , team1 :{self.team1}>, team2 : {self.team2}>"
    

class Contest(db.Model):
    __tablename__ = "contests"

    id = db.Column(db.Integer,primary_key=True)
    match_id = db.Column(db.Integer,db.ForeignKey("matches.match_id"),nullable=False)
    entry_fee = db.Column(db.Integer,nullable=False)
    max_participants = db.Column(db.Integer,nullable=False)
    prize_pool = db.Column(db.Integer,nullable=False)
    
    match = db.relationship("Match",backref="contests")
    def __repr__(self):
        return f"<Contest {self.id} of match {self.match_id} with prize pool {self.prize_pool}>"

class Player(db.Model):
    __tablename__ = "players"

    player_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    team = db.Column(db.String)
    base_value = db.Column(db.Integer)
    match_id = db.Column(db.Integer,db.ForeignKey("matches.match_id"),nullable=False)
    def __repr__(self):
        return f"<Name : {self.name} , team : {self.team} , base_value : {self.base_value}>"
    
class FantasyTeam(db.Model):
    __tablename__ = "fantasy_team"

    id = db.Column(db.Integer,primary_key=True)
    team_name = db.Column(db.String,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.uid"),nullable=False)
    match_id = db.Column(db.Integer,db.ForeignKey("matches.match_id"),nullable=False)
    captain_id = db.Column(db.Integer,db.ForeignKey("players.player_id"),nullable=False)
    vice_captain_id = db.Column(db.Integer,db.ForeignKey("players.player_id"),nullable=False)

    user = db.relationship("User",backref="fantasy_team")
    match = db.relationship("Match",backref="fantasy_team")
    captain = db.relationship("Player",foreign_keys=[captain_id])
    vice_captain = db.relationship("Player",foreign_keys=[vice_captain_id])
    

    def __repr__(self):
        return f"<Fantasy Team of userid {self.user_id} of match {self.match_id}>"

class FantasyTeamPlayer(db.Model):
    __tablename__ = "fantasy_team_player"

    id = db.Column(db.Integer,primary_key=True)
    fantasy_team_id = db.Column(db.Integer,db.ForeignKey("fantasy_team.id"),nullable=False)
    player_id = db.Column(db.Integer,db.ForeignKey("players.player_id"),nullable=False)

    fantasy_team = db.relationship("FantasyTeam",backref="players")
    player = db.relationship("Player",backref="fantasy_teams")

    def __repr__(self):
        return f"<Fantasy team player {self.player_id} of fantasy team {self.fantasy_team_id}>"
    

class UserContest(db.Model):
    __tablename__ = "user_contests"

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.uid"),nullable=False)
    contest_id = db.Column(db.Integer,db.ForeignKey("contests.id"),nullable=False)
    fantasy_team_id = db.Column(db.Integer,db.ForeignKey("fantasy_team.id"),nullable=False)
    

    user = db.relationship("User",backref="joined_contests")
    contest = db.relationship("Contest",backref="participants")
    fantasy_team = db.relationship("FantasyTeam",backref="entries")
    def __repr__(self):
        return f"<UserContest {self.id} of user {self.user_id}>"