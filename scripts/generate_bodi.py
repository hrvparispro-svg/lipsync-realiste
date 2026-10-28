import os, time
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
theme = os.environ.get("THEME_INPUT", "manager toxique")

# 1. Script
prompt = f"Ecris 65s, 155 mots max, francais oral sur {theme}. Hook + 3 signes + validation + 1 conseil. Phrases courtes."
r = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
script = r.text.strip()
print(f"SCRIPT: {script}")
open("script_du_jour.txt","w",encoding="utf-8").write(script)
os.makedirs("inputs", exist_ok=True)

# 2. TTS avec retry anti-503 + anti-quota
models_to_try = [
    "gemini-3.8-flash-tts",
    "gemini-3.8-flash-lite-tts",  # meme famille mais quota separe, moins surcharge
    "gemini-2.5-flash-preview-tts" # fallback final
]

audio_data = None
for model_name in models_to_try:
    for attempt in range(4):
        try:
            print(f"Essai {model_name} tentative {attempt+1}/4...")
            resp = client.models.generate_content(
                model=model_name,
                contents=script,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
                        )
                    )
                )
            )
            audio_data = resp.candidates[0].content.parts[0].inline_data.data
            print(f"OK avec {model_name}")
            break
        except Exception as e:
            msg = str(e)
            if "503" in msg or "UNAVAILABLE" in msg:
                print(f"  -> 503 surcharge, on attend 20s et retry...")
                time.sleep(20)
                continue
            elif "RESOURCE_EXHAUSTED" in msg:
                print(f"  -> Quota cramé sur {model_name}, on passe au suivant")
                break
            else:
                print(f"  -> Erreur {e}")
                time.sleep(5)
    if audio_data:
        break

if not audio_data:
    raise Exception("Tous les modeles TTS surchargés, reessaye dans 10min")

open("inputs/audio.wav","wb").write(audio_data)
print("✅ AUDIO 1min+ genere")
