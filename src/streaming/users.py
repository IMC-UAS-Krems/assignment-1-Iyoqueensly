"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser - no subscription, limited to 6 skips per hour
    - PremiumUser - paid subscriber with subscription start date
    - FamilyAccountUser - manages a group of FamilyMember subaccounts
    - FamilyMember - subaccount belonging to a FamilyAccountUser
"""
from abc import ABC  #abstract representation
from datetime import date

class User(ABC):
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = [] #list of ListeningSession objectsw

    def add_session(self, session):
        self.sessions.append(session) #attaching a ListeningSession to users history

    def total_listening_seconds(self):
        total = 0
        for session in self.sessions:
            total = total + session.duration_listened_seconds
        return total #sum all listening duration in seconds across all sessions


    def total_listening_minutes(self):
        return self.total_listening_seconds() / 60 #converts total listening time from secs to  mins

    def unique_tracks_listened(self):
       return {s.track.track_id for s in self.sessions} #returns set of unique track ids the user has listened to

class FreeUser(User):
    MAX_SKIPS_PER_HOUR = 6 #no subscription, max skips per hour

    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)

class PremiumUser(User): #paid subscriber with full platform access
    def __init__(self, user_id, name, age, subscription_start):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start #stores date of sub start for billings


class FamilyAccountUser(User): #owner of family plan account, can add members and view all
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.sub_users = []

    def add_sub_user(self, sub_user):
        self.sub_users.append(sub_user)

    def all_members(self):
        return [self] + self.sub_users #returns the owner plus all subusers as a single list


class FamilyMember(User): #second account that belongs to FamilyAccountUser
     def __init__(self, user_id, name, age, parent):
        super().__init__(user_id, name, age)
        self.parent = parent #who manages the account
