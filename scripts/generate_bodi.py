import os, time
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
theme = os.environ.get("THEME_INPUT", "Le manager toxique qui te fait douter de toi")

# 1. GÉNÈRE LE TEXTE AVEC RETRY
prompt_text = f"""
Tu es Bodi, coach bienveillant sur le travail.
Écris un script de 50s max en français parlé.
Sujet : {theme}
Mission : 1 hook, 2 signes concrets, 1 conseil protecteur.
Ton : Tutor, posé, pédagogue.
Juste le texte à dire.
"""

script = None
for model_name in ["gemini-2.0-flash", "gemini-1.5-flash"]:
    try:
        print(f"Essai texte avec {model_name}")
        resp = client.models.generate_content(model=model_name, contents=prompt_text)
        script = resp.text.strip()
        break
    except Exception as e:
        print(f"Echec {model_name}: {e}")
        time.sleep(2)

if not script:
    script = "Si ton manager te fait douter de toi constamment, ce n'est pas normal. Ce n'est pas toi le problème. Un bon manager te fait grandir, pas douter."

print(f"SCRIPT: {script}")
with open("script_du_jour.txt", "w", encoding="utf-8") as f:
    f.write(script)

# 2. GÉNÈRE AUDIO BODI TUTOR AVEC RETRY
os.makedirs("inputs", exist_ok=True)
audio_ok = False
for attempt in range(5): # 5 tentatives
    try:
        print(f"Tentative audio Bodi {attempt+1}/5...")
        audio_resp = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts", # Modèle TTS stable avec Bodi
            contents=script,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Bodi")
                    )
                )
            )
        )
        data = audio_resp.candidates[0].content.parts[0].inline_data.data
        with open("inputs/audio.wav", "wb") as f:
            f.write(data)
        audio_ok = True
        print("✅ Audio Bodi OK")
        break
    except Exception as e:
        print(f"503 surchargé, on réessaye dans 10s... {e}")
        time.sleep(10)

if not audio_ok:
    raise Exception("Gemini TTS surchargé, relance le workflow dans 2 min")
