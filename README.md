# L'ART DU LIEN - French Relationships Solo Podcast Bot

Un générateur automatisé de podcasts vidéo 16:9 Full HD (1920x1080) en français, animé par une hôte féminine solo (**Élodie**) explorant la psychologie des relations humaines, l'amour, l'attachement émotionnel et la communication de couple.

## ✨ Caractéristiques Principales
- **Hôte Solo Féminine Naturelle** : Voix neuronale française d'exception (`fr-FR-VivienneMultilingualNeural` / `fr-FR-DeniseNeural`) avec un ton chaleureux, bienveillant et intime.
- **Composition Visuelle Studio Lounge** :
  - Hôte élégante sur le tiers gauche avec microphone de studio Shure SM7B et décor d'appartement parisien tamisé et chaleureux.
  - **Bulle de dialogue flottante (Speech Bubble / Pill Container)** : positionnée sur la droite (X: 1380, Y: 320) avec bordure dorée rayonnante, fond ardoise translucide et karaoké actif mot par mot.
  - **Égaliseur Spectral Audio** : 18 barres dorées animées synchronisées en temps réel sur les fréquences de la voix.
  - **Badge de chaîne supérieur & témoin vert "EN DIRECT"**.
  - **Barre de progression dorée** continue au bas de l'écran.
- **Catalogue & Génération IA de Sujets** :
  - 10 sujets fondamentaux de thérapie de couple et communication bienveillante.
  - Synthèse dynamique de sujets uniques sans répétition via Pollinations AI (`gemini-fast`).
  - Structure en 5 Actes progressifs avec chapitrage YouTube automatique.
- **Miniature YouTube Haute Visibilité (CTR élevé)** : Génération automatique de miniature 1080p avec titres en relief 3D doré/blanc et badge d'épisode.
- **Rendu Ultra-Rapide via FFmpeg** : Encodage direct par flux binaire rawvideo sans fichiers intermédiaires volumineux.

## 📁 Structure du Projet
```text
french-relationships-podcast/
├── assets/
│   ├── host_studio.png         # Image décor 1920x1080 (Hôte à gauche, salon parisien)
│   └── channel_logo.png        # Logo rond 512x512 "L'ART DU LIEN"
├── input/                      # Textes ou sujets optionnels
├── output/                     # Vidéos MP4 finales, miniatures JPG, audios MP3
├── temp/                       # Fichiers audio temporaires par réplique
├── config.py                   # Paramètres visuels, voix, coordonnées
├── story_generator.py          # Moteur de monologue en 5 actes & sujets
├── tts_engine.py               # Synthèse Edge-TTS avec WordBoundary
├── audio_visualizer.py         # Analyse spectrale FFT & barres d'égaliseur
├── video_composer.py           # Compositeur vidéo FFmpeg avec bulle sous-titres
├── thumbnail_generator.py      # Générateur de miniatures YouTube
├── auto_pipeline.py            # Orchestrateur complet de production
├── test_preview.py             # Script de test rapide (15 secondes)
├── requirements.txt            # Dépendances Python
└── .env                        # Clés API (Pollinations, réseaux sociaux)
```

## 🚀 Utilisation

### 1. Test Rapide d'Aperçu (15 secondes)
```bash
python test_preview.py
```

### 2. Générer un Épisode Complet (20 Minutes)
```bash
python auto_pipeline.py --duration 20.0
```

### 3. Générer avec un Sujet Personnalisé
```bash
python auto_pipeline.py --topic "Apprendre à se Reconstruire Après une Rupture" --duration 15.0
```

### 4. Mode Test sans Publication Sociale
```bash
python auto_pipeline.py --duration 10.0 --dry-run
```
