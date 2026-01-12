import re

class URLDetector:
    YOUTUBE_PATTERNS = [
        r'(https?://)?(www\.)?youtube\.com/.*',
        r'(https?://)?(www\.)?youtu\.be/.*'
    ]
    SPOTIFY_PATTERNS = [
        r'(https?://)?(open\.)?spotify\.com/.*'
    ]

    @staticmethod
    def detect(url):
        for pattern in URLDetector.YOUTUBE_PATTERNS:
            if re.match(pattern, url):
                return 'youtube'
        
        for pattern in URLDetector.SPOTIFY_PATTERNS:
            if re.match(pattern, url):
                return 'spotify'
        
        return 'search'
