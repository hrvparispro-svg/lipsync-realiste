import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
theme = os.environ.get("THEME_INPUT", "manager toxique")

# 1. Script 1min10 en 1 fois (150 mots)
prompt = f"Ecris un script de 65 secondes, 155 mots, francais oral, sur {theme}. Structure: hook, 3 signes, validation, 1 conseil. Phrases courtes, tutoiement."
r = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
script = r.text.strip()
print(f"SCRIPT {len(script)} chars:\n{script}")
open("script_du_jour.txt","w",encoding="utf-8").write(script)
os.makedirs("inputs", exist_ok=True)

# 2. 1 SEUL APPEL TTS = 1 quota au lieu de 6
try:
    audio = client.models.generate_content(
        model="gemini-3.8-flash-tts",
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
    open("inputs/audio.wav","wb").write(audio.candidates[0].content.parts[0].inline_data.data)
    print("✅ Audio 1min genere en 1 appel")
except Exception as e:
    # FALLBACK si quota 3.8 cramé -> utilise l'ancien modele qui a un autre quota
    if "RESOURCE_EXHAUSTED" in str(e):
        print("Quota 3.8 cramé, fallback sur 2.5-flash-tts")
        audio = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
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
        open("inputs/audio.wav","wb").write(audio.candidates[0].content.parts[0].inline_data.data)
    else:
        raise e
