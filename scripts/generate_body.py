import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 1. THÈME DU JOUR - Tu peux le changer à chaque run
# Si tu lances manuellement depuis GitHub, tu pourras le taper
theme = os.environ.get("THEME_INPUT", "Le manager toxique qui te fait douter de toi")

prompt_text = f"""
Tu es Bodi, créateur de contenu éducatif sur le travail.
Écris un script de 55 secondes max, en français parlé naturel.

Sujet : {theme}
Mission : Expliquer ce comportement toxique + donner 1 conseil concret et bienveillant pour se protéger.
Ton : Tutor, posé, pédagogue, rassurant, pas agressif. Comme un coach qui veut vraiment aider.
Structure : 
- Hook 3s: "Si ton manager fait ça, ce n'est pas normal..."
- 2 signes concrets
- 1 phrase de validation: "Ce n'est pas toi le problème"
- 1 conseil actionnable
Interdiction : Pas de jargon RH, pas de didascalies [comme ça].

Texte brut à dire uniquement.
"""

print(f"Thème: {theme}")
text_resp = client.models.generate_content(model="gemini-3.8-flash", contents=prompt_text)
script = text_resp.text.strip()
print(f"SCRIPT BODI:\n{script}\n")

with open("script_du_jour.txt", "w", encoding="utf-8") as f:
    f.write(script)

# 2. AUDIO AVEC LA VRAIE VOIX BODI TUTOR
print("Génération audio avec Bodi (Tutor)...")
audio_resp = client.models.generate_content(
    model="gemini-3.8-flash-tts",
    contents=script,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Bodi"  # <-- TA VOIX DANS LA CATÉGORIE TUTOR
                )
            )
        )
    )
)

# Sauvegarde
os.makedirs("inputs", exist_ok=True)
audio_data = audio_resp.candidates[0].content.parts[0].inline_data.data
with open("inputs/audio.wav", "wb") as f:
    f.write(audio_data)

print("✅ Audio Bodi généré : inputs/audio.wav")
