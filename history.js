// Historique des épisodes & Registre des sujets
const PODCAST_HISTORY = [
  {
    "episode": 1,
    "topic": "L'Art de s'Écouter dans le Couple",
    "date": "2026-10-24T17:41:48.599892",
    "duration_sec": 125.22,
    "duration_min": 2.09,
    "video_file": "podcast_ep1_20261024_173955.mp4",
    "thumbnail_file": "thumb_ep1_20261024_173955.jpg",
    "platform": "Local"
  },
  {
    "episode": 2,
    "topic": "L'Équilibre Délicat : Donner Sans s'Épuiser en Amour",
    "date": "2026-10-24T17:56:08.966966",
    "duration_sec": 240.31,
    "duration_min": 4.01,
    "video_file": "podcast_ep2_20261024_174805.mp4",
    "thumbnail_file": "thumb_ep2_20261024_174805.jpg",
    "platform": "Local"
  }
];
if (typeof module !== 'undefined' && module.exports) { module.exports = PODCAST_HISTORY; }
if (typeof window !== 'undefined') { window.PODCAST_HISTORY = PODCAST_HISTORY; }
