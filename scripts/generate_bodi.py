import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
theme = os.environ.get("THEME_INPUT", "Le manager qui te fait douter de toi")

# 1. Texte
p = f"Ecris un script 50s en francais sur {theme}. Ton Bodi Tutor pose et rassurant."
r = client.models.generate_content(model="gemini-3.8-flash", contents=p)
script = r.text.strip()
open("script_du_jour.txt","w",encoding="utf-8").write(script)
os.makedirs("inputs", exist_ok=True)

# 2. Audio avec TON modele 3.8
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
print("OK Bodi 3.8")
