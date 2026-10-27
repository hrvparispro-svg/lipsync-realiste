import os, time
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
theme = os.environ.get("THEME_INPUT", "Le manager toxique qui te fait douter de toi")

prompt_text = f"""
Tu es Bodi, coach bienveillant.
Script 50s max en français parlé naturel.
Sujet : {theme}
Structure : Hook 3s, 2 signes concrets, 1 validation "Ce n'est pas toi le problème", 1 conseil protecteur.
Ton : posé, rassurant, tutor.
Juste le texte à dire.
"""

print(f"Thème: {theme}")
resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt_text)
script = resp.text.strip()
print(f"SCRIPT: {script}")

with open("script_du_jour.txt", "w", encoding="utf-8") as f:
    f.write(script)

os.makedirs("inputs", exist_ok=True)
print("Génération audio Bodi-like avec Kore...")

# ON REMPLACE BODI PAR KORE (LA VOIX TUTOR AUTORISÉE)
audio_resp = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents=f"Dis avec un ton de tuteur bienveillant, posé et rassurant, comme un coach qui aide : {script}",
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Kore"  # <- REMPLAÇANT OFFICIEL DE BODI TUTOR
                )
            )
        )
    )
)

data = audio_resp.candidates[0].content.parts[0].inline_data.data
with open("inputs/audio.wav", "wb") as f:
    f.write(data)

print("✅ Audio Bodi (Kore) généré")
