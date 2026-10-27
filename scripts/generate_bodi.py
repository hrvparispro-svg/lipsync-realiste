import os
from google import genai
from google.genai import types

# Client avec ta clé GEMINI_API_KEY
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Thème - changeable depuis GitHub Actions
theme = os.environ.get("THEME_INPUT", "Le manager toxique qui te fait douter de toi")

prompt_text = f"""
Tu es Bodi, coach bienveillant spécialiste des relations au travail.
Écris un script de 50 secondes max, en français parlé naturel et fluide.

Sujet : {theme}
Mission : Expliquer ce comportement toxique simplement + donner 1 conseil concret et protecteur.
Ton : Tutor, posé, pédagogue, rassurant. Comme un grand frère qui aide.
Structure obligatoire :
- Hook 3s : "Si ton manager fait ça, ce n'est pas normal..."
- 2 signes concrets que tout le monde peut reconnaître
- 1 phrase de validation : "Ce n'est pas toi le problème"
- 1 conseil actionnable pour se protéger
Règles : Pas de jargon RH, pas de didascalies [rire], juste le texte à dire. Français naturel.

Texte final uniquement :
"""

print(f"Thème: {theme}")
text_resp = client.models.generate_content(model="gemini-3.8-flash", contents=prompt_text)
script = text_resp.text.strip()
print(f"SCRIPT BODI:\n{script}\n")

# Sauvegarde du script
with open("script_du_jour.txt", "w", encoding="utf-8") as f:
    f.write(script)

# Génération audio avec la VRAIE voix Bodi Tutor
print("Génération audio Bodi Tutor...")
audio_resp = client.models.generate_content(
    model="gemini-3.8-flash-tts",
    contents=script,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Bodi"
                )
            )
        )
    )
)

os.makedirs("inputs", exist_ok=True)
audio_data = audio_resp.candidates[0].content.parts[0].inline_data.data
with open("inputs/audio.wav", "wb") as f:
    f.write(audio_data)

print("✅ Audio Bodi généré : inputs/audio.wav")
