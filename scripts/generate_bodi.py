import os, time
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
theme = os.environ.get("THEME_INPUT", "Le manager toxique qui te fait douter de toi")

# 1. TEXTE - Avec gemini-3.8-flash (le nouveau obligatoire)
def gen_text_with_retry():
    prompt = f"""
Tu es Bodi, coach bienveillant.
Script 50s max en français parlé naturel.
Sujet : {theme}
Structure : Hook 3s, 2 signes concrets, 1 validation "Ce n'est pas toi le problème", 1 conseil protecteur.
Ton : posé, rassurant, tutor.
Juste le texte à dire.
"""
    for i in range(3):
        try:
            print(f"Tentative texte {i+1}/3 avec gemini-3.8-flash")
            resp = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
            return resp.text.strip()
        except Exception as e:
            print(f"Echec texte: {e}, retry dans 5s")
            time.sleep(5)
    return "Si ton manager te fait douter de toi constamment, ce n'est pas normal. Ce n'est pas toi le problème."

script = gen_text_with_retry()
print(f"SCRIPT: {script}")
with open("script_du_jour.txt", "w", encoding="utf-8") as f:
    f.write(script)

# 2. AUDIO - Voix Kore (remplaçante officielle de Bodi Tutor)
os.makedirs("inputs", exist_ok=True)
for i in range(5):
    try:
        print(f"Tentative audio Bodi-Kore {i+1}/5...")
        audio_resp = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=f"Dis avec un ton de tuteur bienveillant, posé et rassurant : {script}",
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
                    )
                )
            )
        )
        data = audio_resp.candidates[0].content.parts[0].inline_data.data
        with open("inputs/audio.wav", "wb") as f:
            f.write(data)
        print("✅ Audio Bodi (Kore) généré")
        break
   
