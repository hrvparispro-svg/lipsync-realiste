import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# --- 1. ON GÉNÈRE LE TEXTE ÉDUCATIF ---
# Tu peux changer le thème ici
theme = "La toxicité par le manager : micro-management et dévalorisation"

prompt_text = f"""
Écris un script de 45-60 secondes pour une vidéo TikTok/Short éducative.
Sujet : {theme}
Ton : Bienveillant, expert RH, direct, comme un grand frère qui conseille. Pas moralisateur.
Structure : 1 accroche forte (3 sec), 2-3 signes concrets, 1 conseil actionnable pour se protéger.
Langue : Français, parlé naturel.
Persona : Bodi.
Ne mets pas de didascalies, juste le texte à dire.
"""

print(f"Génération du script sur : {theme}")
text_response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt_text
)
script_final = text_response.text.strip()
print(f"Script: {script_final}")

# Sauvegarde le script
with open("script_du_jour.txt", "w", encoding="utf-8") as f:
    f.write(script_final)

# --- 2. ON GÉNÈRE L'AUDIO BODI ---
# C'est ici qu'on définit la voix Bodi
# Tu peux ajuster la description jusqu'à avoir TON Bodi parfait

print("Génération audio Bodi...")
response = client.models.generate_content(
    model="gemini-3.8-flash-tts",
    contents=script_final,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Kore" # On va customiser pour Bodi
                )
            )
        )
    )
)

# Pour avoir VRAIMENT ta voix Bodi unique, remplace le bloc ci-dessus par un Custom Voice :
# Il faut d'abord créer Bodi une fois dans AI Studio avec cette description :
# "Jeune homme 25-30 ans, voix chaleureuse et posée, léger accent maghrébin, débit calme et pédagogue, style Bodi"

# Sauvegarde WAV
with open("inputs/audio.wav", "wb") as f:
    f.write(response.candidates[0].content.parts[0].inline_data.data)

print("Audio Bodi prêt -> inputs/audio.wav")
