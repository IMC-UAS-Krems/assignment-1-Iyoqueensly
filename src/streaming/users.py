"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
from abc import ABC  #abstract representation


class User(ABC):
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def total_listening_seconds(self):
        total = 0
        for session in self.sessions:
            total = total + session.duration_listened_seconds
        return total

    #return sum(s.duration_listened_seconds for s in self.sessions)

    def total_listening_minutes(self):
        return self.total_listening_seconds() / 60

    def unique_tracks_listened(self):
       return {s.track.track_id for s in self.sessions} #returns set of unique track ids the user has listened to


class FamilyMember(User):
    def __init__(self, user_id, name, age, parent):
        super().__init__(user_id, name, age)
        self.parent = parent

class FamilyAccountUser(User):
    def __init__(self, user_id, name, age, sub_users):
        super().__init__(user_id, name, age)
        self.sub_users = sub_users

    def add_sub_user(self, sub_user):
        self.sub_users.append(sub_user)

    def all_members(self):
        return self.sub_users


class FreeUser(User):
    MAX_SKIPS_PER_HOUR = 6

    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)


class PremiumUser(User):
    def __init__(self, user_id, name, age, subscription_start):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start

    class FamilyMember(User):
        def __init__(self, user_id, name, age, parent):
            super().__init__(user_id, name, age)
            self.parent = parent
