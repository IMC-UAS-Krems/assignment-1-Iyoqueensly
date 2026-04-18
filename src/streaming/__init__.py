"""
Package initialiser for the streaming platform.
Re-exports every public class so the rest of the codebase can import directly from
'streaming' instead of each submodule
"""

from .tracks import Track, Song, AlbumTrack, SingleRelease, Podcast, NarrativeEpisode, InterviewEpisode, AudiobookTrack
from .artists import Artist
from .albums import Album
from .sessions import ListeningSession
from .users import User, FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from .playlists import Playlist, CollaborativePlaylist
from .platform import StreamingPlatform

__all__ =[ #defines what is available when I do 'from streaming import'
    "Track", "Song", "AlbumTrack", "SingleRelease",
    "Podcast", "NarrativeEpisode", "InterviewEpisode",
    "AudiobookTrack", "Artist", "Album",
    "ListeningSession", "User", "FreeUser",
    "PremiumUser", "FamilyAccountUser", "FamilyMember",
    "Playlist", "CollaborativePlaylist", "StreamingPlatform"
]
