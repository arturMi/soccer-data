from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Time, Date, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class League(Base):
    """
    League data class
    """
    __tablename__ = 'league'

    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.name


class Season(Base):
    """
    Season data class
    """
    __tablename__ = 'season'

    # relationship to dataset table
    league_id = Column(Integer, ForeignKey('league.id'), nullable=False)
    league = relationship(League, backref=backref("season", cascade="all, delete-orphan"))

    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    def __init__(self, league_id, **kwargs):
        self.league_id = league_id
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.title


class Team(Base):
    """
    Team data class
    """
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    team_id = Column(Integer)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.name


class Match(Base):
    """
    Match data class
    """
    __tablename__ = 'match'

    # relationship to team table
    hometeamid = Column(Integer, ForeignKey('team.id'), nullable=False)
    team1 = relationship("Team", foreign_keys=[hometeamid])

    # team1 = relationship(Team, backref=backref("match", cascade="all, delete-orphan"))

    # relationship to team table
    awayteamid = Column(Integer, ForeignKey('team.id'), nullable=False)
    team2 = relationship("Team", foreign_keys=[awayteamid])
    # team2 = relationship(Team, backref=backref("match", cascade="all, delete-orphan"))

    # relationship to season table
    season_id = Column(Integer, ForeignKey('season.id'), nullable=False)
    season = relationship(Season, backref=backref("match", cascade="all, delete-orphan"))

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    time = Column(Time)
    matchday = Column(Integer)
    hometeamname = Column(String, nullable=False)
    awayteamname = Column(String, nullable=False)
    hometeamgoals = Column(Integer, nullable=False)
    awayteamgoals = Column(Integer, nullable=False)
    match_id = Column(Integer)
    hometeamrank = Column(Integer)
    awayteamrank = Column(Integer)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
