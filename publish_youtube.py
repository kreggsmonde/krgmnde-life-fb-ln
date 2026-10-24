"""
YouTube Video Publisher for French Relationships Podcast
Supports OAuth2 refresh token authentication, custom thumbnails, and scheduled publishing days.
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

# Days allowed for YouTube publishing (Tuesday, Thursday, Sunday)
ALLOWED_YOUTUBE_DAYS = {"Tuesday", "Thursday", "Sunday"}

def get_authenticated_service():
    """
    Returns an authenticated YouTube Data API v3 service client using refresh token credentials.
    """
    token_json_str = (os.getenv('YOUTUBE_TOKEN_JSON') or os.getenv('YT_TOKEN_JSON', '')).strip()
    client_id = (os.getenv('YT_CLIENT_ID') or os.getenv('YOUTUBE_CLIENT_ID', '')).strip()
    client_secret = (os.getenv('YT_CLIENT_SECRET') or os.getenv('YOUTUBE_CLIENT_SECRET', '')).strip()
    refresh_token = (os.getenv('YT_REFRESH_TOKEN') or os.getenv('YOUTUBE_REFRESH_TOKEN', '')).strip()
    token_uri = (os.getenv('YT_TOKEN_URI') or os.getenv('YOUTUBE_TOKEN_URI', 'https://oauth2.googleapis.com/token')).strip()

    if token_json_str:
        try:
            d = json.loads(token_json_str)
            client_id = d.get('client_id', client_id)
            client_secret = d.get('client_secret', client_secret)
            refresh_token = d.get('refresh_token', refresh_token)
            token_uri = d.get('token_uri', token_uri)
        except Exception:
            pass

    if not all([client_id, client_secret, refresh_token]):
        print("[YouTube] Note: Identifiants YouTube (YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN) non configurés.")
        print("[YouTube] Publication YouTube ignorée.")
        return None

    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        creds = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=client_id,
            client_secret=client_secret,
            scopes=["https://www.googleapis.com/auth/youtube"]
        )

        if not creds.valid:
            creds.refresh(Request())

        return build('youtube', 'v3', credentials=creds)
    except Exception as e:
        print(f"[YouTube Auth Error] Échec d'authentification YouTube: {e}")
        return None

def publish_to_youtube(video_path, title, description, tags=None, thumb_path=None, force=False):
    current_day = datetime.now().strftime("%A")
    if not force and current_day not in ALLOWED_YOUTUBE_DAYS:
        print(f"[YouTube] Aujourd'hui ({current_day}) n'est pas un jour de publication YouTube prévu.")
        return None

    youtube = get_authenticated_service()
    if not youtube:
        return None

    from googleapiclient.http import MediaFileUpload

    if tags is None:
        tags = ["relations humaines", "psychologie couple", "podcast francais", "amour", "communication bienveillante"]

    body = {
        'snippet': {
            'title': title[:100],
            'description': description,
            'tags': tags,
            'categoryId': '27'  # Education
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }

    try:
        print(f"[YouTube] Téléversement de la vidéo : {title}...")
        media = MediaFileUpload(video_path, chunksize=10*1024*1024, resumable=True)
        request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"[YouTube Upload] {int(status.progress() * 100)}% complété...")

        video_id = response.get('id')
        print(f"[YouTube Upload Success] Vidéo publiée avec succès ! ID: {video_id}")

        if thumb_path and os.path.exists(thumb_path) and video_id:
            try:
                print(f"[YouTube] Téléversement de la miniature : {thumb_path}...")
                youtube.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(thumb_path)).execute()
                print("[YouTube] Miniature mise à jour avec succès !")
            except Exception as e_th:
                print(f"[YouTube Thumbnail Error] Échec de la miniature: {e_th}")

        return response
    except Exception as e:
        print(f"[YouTube Upload Error] {e}")
        return None
