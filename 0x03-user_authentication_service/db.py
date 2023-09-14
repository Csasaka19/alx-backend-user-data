#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User, Base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def add_user(self, email: str, hashed_password: str) -> User:
        '''Method that saves a new user instance to the database'''
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user
    
    def find_user_by(self, **kwargs) -> User:
        '''Method takes in arbitrary keyword arguments and returns the 
        first row found in the users table as filtered by the method’s
        input arguments '''
        fields = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in fields:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        '''Method that takes as argument a required user_id integer
        and arbitrary keyword arguments, and returns None'''
        user = self.find_user_by(id=user_id)
        fields = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in fields:
                raise ValueError
            setattr(user, key, kwargs[key])
        self._session.commit()
        return None