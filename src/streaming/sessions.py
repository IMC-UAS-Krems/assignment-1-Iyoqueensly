"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession - records one play event(who listened, to what, when, for how long)
"""

class ListeningSession:
    def __init__(self, session_id, user, track, timestamp, duration_listened_seconds):
        self.session_id = session_id
        self.user = user #user who listened
        self.track = track
        self.timestamp = timestamp #datetime when playback started
        self.duration_listened_seconds = duration_listened_seconds

    def duration_listened_minutes(self):
        return self.duration_listened_seconds / 60 #returns listening duration in minutes