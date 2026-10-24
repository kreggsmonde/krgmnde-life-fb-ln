"""
Facebook Page Video Publisher (Meta Graph API v20.0)
"""
import os
import sys
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()
GRAPH_API_VERSION = "v20.0"
CHUNK_SIZE_BYTES = 32 * 1024 * 1024  # 32 MB chunks

def get_facebook_credentials():
    page_id = (os.getenv('FB_PAGE_ID') or os.getenv('FACEBOOK_PAGE_ID') or '').strip()
    access_token = (os.getenv('FB_PAGE_ACCESS_TOKEN') or os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN') or '').strip()

    if not page_id or not access_token:
        print("[facebook] Identifiants FB_PAGE_ID ou FB_PAGE_ACCESS_TOKEN non configurés.")
        return None, None
    return page_id, access_token

def upload_to_facebook(video_path: str, title: str, description: str):
    page_id, access_token = get_facebook_credentials()
    if not page_id or not access_token:
        print("[facebook] Téléversement ignoré (absence d'identifiants).")
        return None

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/videos"
    try:
        print(f"[facebook] Publication vers Facebook Page ID {page_id}...")
        with open(video_path, 'rb') as vf:
            files = {'source': vf}
            data = {
                'title': title,
                'description': description,
                'access_token': access_token
            }
            res = requests.post(url, files=files, data=data, timeout=300)
            if res.status_code == 200:
                print(f"[facebook] Vidéo publiée avec succès : {res.json()}")
                return res.json()
            else:
                print(f"[facebook] Erreur : {res.status_code} {res.text}")
                return None
    except Exception as e:
        print(f"[facebook] Exception lors de la publication : {e}")
        return None
