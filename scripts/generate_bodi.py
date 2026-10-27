import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
theme = os.environ.get("THEME_INPUT", "Le manager toxique qui te fait douter de toi")

prompt = f"Tu es Bodi, coach bienveillant. Ecris un script de 50s max en francais parle naturel. Sujet : {theme}. Structure : Hook 3s, 2 signes concrets, 1 validation 'Ce n est pas toi le probleme', 1 conseil protecteur. Ton : pose, rassurant, tutor. Juste le texte a dire."

resp = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
script = resp.text.strip()
print(f"SCRIPT: {script}")

with open("script_du_jour.txt", "w", encoding="utf-8") as f:
    f.write(script)

os.makedirs("inputs", exist_ok=True)

audio_resp = client.models.generate_content(
    model="gem
