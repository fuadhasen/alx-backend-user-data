#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine(
            "sqlite:///a.db", echo=True)
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
        obj = User()
        obj.email = email
        obj.hashed_password = hashed_password
        self._session.add(obj)
        self._session.commit()
        return obj

    def find_user_by(self, **kwargs: str) -> User:
        """method to find user
        """
        for key, val in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError
            filtered_user = self._session.query(User)
            row = filtered_user.filter(getattr(User, key) == val).first()
        if not row:
            return NoResultFound
        return row

            
        key1, value1 = list(kwargs.items())[0]
        if hasattr(User, key1):
            filtered_user = self._session.query(User)
            row = filtered_user.filter(getattr(User, key1) == value1).first()
            if row is None:
                raise NoResultFound
            return row
        else:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs: str):
        """method to Update user instance
        """
        user_filter = self._session.query(User)
        user = user_filter.filter(User.id == user_id).first()

        key1, value1 = list(kwargs.items())[0]
   
        setattr(user, key1, value1)
        self._session.commit()

        try:
            self.find_user_by(**kwargs)
        except Exception:
            raise ValueError
