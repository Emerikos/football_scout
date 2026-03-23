from datetime import datetime,date
from decimal import Decimal
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, UniqueConstraint

db = SQLAlchemy()




class Admin(db.Model):
    __tablename__ = "admin"

    admin_id = db.Column(db.Integer, primary_key=True)

    admin_username = db.Column(db.String(50), unique=True)
    admin_email = db.Column(db.String(150), nullable=False, unique=True)
    admin_password_hash = db.Column(db.String(255), nullable=False)
    admin_created_at = db.Column(db.DateTime,default=datetime.utcnow)




class Player(db.Model):
    __tablename__ = "players"

    player_id = db.Column(db.Integer, primary_key=True)
    player_firstname = db.Column(db.String(100), nullable=False)
    player_lastname = db.Column(db.String(100), nullable=False)
    player_height = db.Column(db.Integer)
    # player_pref_foot = db.Column(db.Enum("left", "right", "both"), nullable=False)
    player_email = db.Column(db.String(100), unique=True)
    player_phone = db.Column(db.String(20), nullable=True)
    player_password_hash = db.Column(db.String(255), nullable=False)
    player_photo = db.Column(db.String(200), nullable=True)
    player_date_of_birth = db.Column(db.Date, nullable=False)
    player_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    player_updated_at = db.Column(db.DateTime,default=None,onupdate=datetime.utcnow)

    primary_position_id = db.Column(db.Integer,db.ForeignKey("position.position_id"))
    club_id = db.Column(db.Integer,db.ForeignKey("clubs.club_id"),nullable=True)
    country_id = db.Column(db.Integer,db.ForeignKey("country.country_id"),nullable=False)

    secondary_positions = db.relationship("PlayerPosition", back_populates="player")
    primary_position = db.relationship("Position",back_populates="player")
    videos = db.relationship("Video", back_populates="player")
    reports = db.relationship("ScoutReport", back_populates="player")
    club = db.relationship("Club", back_populates="players")
    country = db.relationship("Country", back_populates="players")

    @classmethod
    def is_email_used(cls,email):
        email_used = cls.query.filter(cls.player_email==email).first()
        return email_used
    
    def get_age(self):
        if not self.player_date_of_birth:
            return "Null"
        else:
            today = date.today()
            dob = self.player_date_of_birth
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))





class PlayerPosition(db.Model):
    __tablename__ = "player_positions"

    player_position_id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer,db.ForeignKey("players.player_id"),nullable=False)
    position_id = db.Column(db.Integer,db.ForeignKey("position.position_id"),nullable=False)
    player = db.relationship("Player", back_populates="secondary_positions")
    position = db.relationship("Position", back_populates="players")




class Position(db.Model):
    __tablename__ = "position"

    position_id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String(100), nullable=False)
    player = db.relationship("Player",back_populates="primary_position")
    players = db.relationship("PlayerPosition", back_populates="position")





class Scout(db.Model):
    __tablename__ = "scout"

    scout_id = db.Column(db.Integer, primary_key=True)
    scout_firstname = db.Column(db.String(100), nullable=False)
    scout_lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    scout_photo = db.Column(db.String(200), nullable=True)
    scout_password_hash = db.Column(db.String(255), nullable=False)
    scout_reg_date = db.Column(db.DateTime,default=datetime.utcnow)
    scout_updated_at = db.Column(db.DateTime,default=None,onupdate=datetime.utcnow)
    reports = db.relationship("ScoutReport", back_populates="scout")


    @classmethod
    def is_email_used(cls,email):
        email_used = cls.query.filter(cls.email==email).first()
        return email_used




class ScoutReport(db.Model):
    __tablename__ = "scout_report"

    report_id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer,db.ForeignKey("players.player_id"),nullable=False)
    scout_id = db.Column(db.Integer,db.ForeignKey("scout.scout_id"),nullable=False)
    strengths = db.Column(db.Text)
    weaknesses = db.Column(db.Text)
    comments = db.Column(db.String(200))
    report_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scout = db.relationship("Scout", back_populates="reports")
    player = db.relationship("Player", back_populates="reports")



class Video(db.Model):
    __tablename__ = "videos"

    video_id = db.Column(db.Integer, primary_key=True)
    video_link = db.Column(db.String(300))
    player_id = db.Column(db.Integer,db.ForeignKey("players.player_id"),nullable=False)
    video_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    video_description = db.Column(db.String(200))
    video_caption = db.Column(db.String(100)) 
    player = db.relationship("Player", back_populates="videos")




class Club(db.Model):
    __tablename__ = "clubs"

    club_id = db.Column(db.Integer, primary_key=True)
    club_name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))
    country_id = db.Column(db.Integer,db.ForeignKey("country.country_id"),nullable=False)
    players = db.relationship("Player", back_populates="club")
    country = db.relationship("Country", back_populates="clubs")





class Country(db.Model):
    __tablename__ = "country"

    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(100), nullable=False)
    players = db.relationship("Player", back_populates="country")
    clubs = db.relationship("Club", back_populates="country")

    def __repr__(self):
        return f"<Country {self.name}>"