import datetime
import enum
import flask_login
from typing import List, Optional

from sqlalchemy import ARRAY, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


from sqlalchemy import ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime
from sqlalchemy import Date

from . import db

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List, Optional

import pathlib
from pathlib import Path
from flask import current_app


class ProposalStatus(enum.Enum):
    proposed = 1
    accepted = 2
    rejected = 3
    ignored = 4
    reschedule = 5

# Intermediate table for the many-to-many relationship
class LikingAssociation(db.Model):
    liker_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    liked_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

class BlockingAssociation(db.Model):
    blocker_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    blocked_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non-binary"
    OTHER = "other"

class User(flask_login.UserMixin,db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[str] = mapped_column(String(256))
    profile: Mapped["Profile"] = relationship(back_populates="user")
    matching_preferences: Mapped["MatchingPreferences"] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False)


    sent_proposals: Mapped[List["DateProposal"]] = relationship(
        back_populates="proposer", foreign_keys="DateProposal.proposer_id"
    )
    received_proposals: Mapped[List["DateProposal"]] = relationship(
        back_populates="recipient", foreign_keys="DateProposal.recipient_id"
    )
    liking: Mapped[List["User"]] = relationship(
        secondary=LikingAssociation.__table__,
        primaryjoin=LikingAssociation.liker_id == id,
        secondaryjoin=LikingAssociation.liked_id == id,
        back_populates="likers",
    )
    likers: Mapped[List["User"]] = relationship(
        secondary=LikingAssociation.__table__,
        primaryjoin=LikingAssociation.liked_id == id,
        secondaryjoin=LikingAssociation.liker_id == id,
        back_populates="liking",
    )
    blocking: Mapped[List["User"]] = relationship(
        secondary=BlockingAssociation.__table__,
        primaryjoin=BlockingAssociation.blocker_id == id,
        secondaryjoin=BlockingAssociation.blocked_id == id,
        back_populates="blockers",
    )
    blockers: Mapped[List["User"]] = relationship(
        secondary=BlockingAssociation.__table__,
        primaryjoin=BlockingAssociation.blocked_id == id,
        secondaryjoin=BlockingAssociation.blocker_id == id,
        back_populates="blocking",
    )


class Photo(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    profile: Mapped["Profile"] = relationship(back_populates="photo")
    file_extension: Mapped[str] = mapped_column(String(8))


class Profile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    name: Mapped[str] = mapped_column(String(64))
    gender: Mapped[str] = mapped_column(String(256))
    year: Mapped[int] 
    bio: Mapped[str] = mapped_column(String(256))
    allergies: Mapped[Optional[str]] = mapped_column(String(256))   
    city: Mapped[Optional[str]] = mapped_column(String(64))  
    study: Mapped[Optional[str]] = mapped_column(String(64))
    hobbies: Mapped[str] = mapped_column(String(256))  
    music: Mapped[Optional[str]] = mapped_column(String(256))  
    cuisine: Mapped[Optional[str]] = mapped_column(String(256))  
    personality_traits: Mapped[Optional[str]] = mapped_column(String(256))  
    lifestyle: Mapped[Optional[str]] = mapped_column(String(256))
    

    user: Mapped["User"] = relationship(
        back_populates="profile",
        single_parent=True,
    )
    photo_id: Mapped[int] = mapped_column(ForeignKey("photo.id"))
    photo: Mapped[Optional["Photo"]] = relationship(back_populates="profile")
    # Relationship with additional photos
    additional_photos: Mapped[List["AdditionalPhoto"]] = relationship(
        "AdditionalPhoto",
        back_populates="profile",
        cascade="all, delete-orphan",  # Delete photos if profile is deleted
    )


class AdditionalPhoto(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))  
    file_extension: Mapped[str] = mapped_column(String(8))  
    profile: Mapped["Profile"] = relationship(back_populates="additional_photos")


class MatchingPreferences(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    interested_genders: Mapped[str]= mapped_column(String(256))
    min_age: Mapped[int]
    max_age: Mapped[int]
    relationship_type: Mapped[str] = mapped_column(String(20))

    user: Mapped["User"] = relationship(
        back_populates="matching_preferences",
        single_parent=True,
    )

class DateProposal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[ProposalStatus] = mapped_column(Enum(ProposalStatus), nullable=False)

    proposer_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    proposer: Mapped["User"] = relationship(
        foreign_keys=[proposer_id], back_populates="sent_proposals"
    )
    recipient_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    recipient: Mapped["User"] = relationship(
        foreign_keys=[recipient_id], back_populates="received_proposals"
    )

    message : Mapped[str]= mapped_column(String(256))
    response_message : Mapped[str]= mapped_column(String(256),nullable=True)
    time: Mapped[str]= mapped_column(String(256),nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False) 
    proposal_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    response_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    table_id : Mapped[int]

class RestaurantAvailability(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    table_id : Mapped[int] 
    date : Mapped[date] = mapped_column(Date, nullable=False) 

class ContactSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  
    email = db.Column(db.String(120), nullable=False)  
    subject = db.Column(db.String(200), nullable=False)  
    message = db.Column(db.Text, nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  

