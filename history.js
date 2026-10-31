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
  },
  {
    "episode": 3,
    "topic": "L'Art de s'Écouter dans le Couple",
    "date": "2026-10-24T19:28:11.300109",
    "duration_sec": 125.22,
    "duration_min": 2.09,
    "video_file": "podcast_ep3_20261024_192455.mp4",
    "thumbnail_file": "thumb_ep3_20261024_192455.jpg",
    "platform": "Local"
  },
  {
    "episode": 3,
    "topic": "La Tendresse : Le Ciment Invisible de nos Liens",
    "date": "2026-10-24T15:01:07.574322",
    "duration_sec": 1228.14,
    "duration_min": 20.47,
    "video_file": "podcast_ep3_20261024_144949.mp4",
    "thumbnail_file": "thumb_ep3_20261024_144949.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 4,
    "topic": "Naviguer les Zones d'Ombre : La Confrontation Bienveillante",
    "date": "2026-10-25T07:27:14.889543",
    "duration_sec": 1312.36,
    "duration_min": 21.87,
    "video_file": "podcast_ep4_20261025_070816.mp4",
    "thumbnail_file": "thumb_ep4_20261025_070816.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 5,
    "topic": "L'Art d'Aimer en Toute Sécurité : Construire un Attachement Serein",
    "date": "2026-10-26T07:34:08.022015",
    "duration_sec": 1289.22,
    "duration_min": 21.49,
    "video_file": "podcast_ep5_20261026_071517.mp4",
    "thumbnail_file": "thumb_ep5_20261026_071517.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 6,
    "topic": "L'Art de Dire 'Je T'aime' Sans le Dire : La Communication Non Verbale en Amour",
    "date": "2026-10-27T07:24:31.274667",
    "duration_sec": 1346.91,
    "duration_min": 22.45,
    "video_file": "podcast_ep6_20261027_070525.mp4",
    "thumbnail_file": "thumb_ep6_20261027_070525.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 7,
    "topic": "L'Art de Cultiver la Confiance : Le Terreau de l'Amour Durable",
    "date": "2026-10-28T08:02:55.968433",
    "duration_sec": 1250.05,
    "duration_min": 20.83,
    "video_file": "podcast_ep7_20261028_074514.mp4",
    "thumbnail_file": "thumb_ep7_20261028_074514.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 8,
    "topic": "L'Art de Cultiver la Joie Partagée : Le Bonheur à Deux",
    "date": "2026-10-29T08:04:38.094544",
    "duration_sec": 1213.57,
    "duration_min": 20.23,
    "video_file": "podcast_ep8_20261029_075134.mp4",
    "thumbnail_file": "thumb_ep8_20261029_075134.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 9,
    "topic": "L'Art d'Évoluer Ensemble : Quand Nos Chemins Divergent",
    "date": "2026-10-30T08:14:58.286367",
    "duration_sec": 1327.52,
    "duration_min": 22.13,
    "video_file": "podcast_ep9_20261030_075501.mp4",
    "thumbnail_file": "thumb_ep9_20261030_075501.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 10,
    "topic": "L'Art de se Retrouver : Réinventer l'Amour Après la Routine",
    "date": "2026-10-31T08:02:56.812014",
    "duration_sec": 1256.48,
    "duration_min": 20.94,
    "video_file": "podcast_ep10_20261031_074717.mp4",
    "thumbnail_file": "thumb_ep10_20261031_074717.jpg",
    "platform": "Facebook"
  }
];
if (typeof module !== 'undefined' && module.exports) { module.exports = PODCAST_HISTORY; }
if (typeof window !== 'undefined') { window.PODCAST_HISTORY = PODCAST_HISTORY; }
