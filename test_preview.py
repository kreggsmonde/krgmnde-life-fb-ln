"""
Script de test rapide : génère un extrait court de 15 secondes pour valider la synthèse audio,
le positionnement de la bulle de sous-titres, l'égaliseur et le rendu visuel.
"""
import sys, os
from auto_pipeline import run_auto_pipeline

if __name__ == "__main__":
    print("[TEST] Lancement du test aperçu de 15 secondes...")
    run_auto_pipeline(
        target_minutes=0.5,
        topic="L'Art de s'Écouter dans le Couple",
        dry_run=True,
        preview_seconds=15.0
    )
