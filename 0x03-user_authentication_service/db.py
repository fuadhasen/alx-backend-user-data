#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """instance method to Add new User
        """
        session = self._session
        obj = User()
        obj.email = email
        obj.hashed_password = hashed_password

        session.add(obj)
        session.commit()
        return obj

    def find_user_by(self, **kwargs):
        """find user from Database
        """
        session = self._session
        for key, val in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError
            filter_user = session.query(User)
            user = filter_user.filter(getattr(User, key) == val).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """update user from the Databse
        """
        user = self.find_user_by(id=user_id)
        if not user:
            return None
        for key, val in kwargs.items():
            if not hasattr(User, key):
                raise ValueError
            setattr(user, key, val)
        self._session.commit()
        return None
