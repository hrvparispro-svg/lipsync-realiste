import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
theme = os.environ.get("THEME_INPUT", "manager toxique")

p = f"Tu es Bodi coach. Script 50s francais sur {theme}. Hook, 2 signes, 1 conseil. Ton pose."

r = client.models.generate_content(model="gemini-3.8-flash", contents=p)
script = r.text.strip()

open("script_du_jour.txt","w",encoding="utf-8").write(script)
os.makedirs("inputs", exist_ok=True)

a = client.models.generate_content(
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

data = a.candidates[0].content.parts[0].inline_data.data
open("inputs/audio.wav","wb").write(data)
