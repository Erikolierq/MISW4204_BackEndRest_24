from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import UniqueConstraint
from marshmallow import fields
import enum


db = SQLAlchemy()



class User(db.Model):
    __table_args__ = (UniqueConstraint('email', name='unique_email'),)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    processed = db.Column(db.String(100), default="uploaded")
    uploaded_at = db.Column(db.DateTime, nullable=False)
    url_original = db.Column(db.String(100), nullable=False)
    url_processed = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('videos', lazy=True))
    

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref=db.backref('votes', lazy=True))
    video = db.relationship('Video', backref=db.backref('votes', lazy=True))
    
    
class VideoLeaderboard(db.Model):
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    total_votes = db.Column(db.Integer, nullable=False, default=0)
    video = db.relationship('Video', backref=db.backref('leaderboard', lazy=True))

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = User
         include_relationships = True
         load_instance = True

class VideoSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Video
         include_relationships = True
         load_instance = True

class VoteSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Vote
         include_relationships = True
         load_instance = True
         
class VideoLeaderboardSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = VideoLeaderboard
         include_relationships = True
         load_instance = True