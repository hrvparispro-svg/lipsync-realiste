import os, time
from google import genai
from google.genai import types
from pydub import AudioSegment
import io

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
theme = os.environ.get("THEME_INPUT", "manager toxique qui te fait douter")

# 1. SCRIPT LONG 1min15
prompt = f"""Tu es Bodi coach. Ecris un script de 70 secondes, 160 mots max, en francais parle naturel, sur {theme}.
Structure:
- Hook 5s
- 3 signes concrets que ce n'est pas toi le probleme
- 1 phrase de validation
- 1 conseil protecteur a appliquer demain
Style: tutoiement, rassurant, pose. Coupe en phrases courtes. Juste le texte."""

resp = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
full_script = resp.text.strip()
print(f"FULL SCRIPT: {full_script}")
open("script_du_jour.txt","w",encoding="utf-8").write(full_script)

# 2. DECOUPAGE en phrases pour TTS long
sentences = [s.strip() for s in full_script.replace('!','.').replace('?','.').split('.') if len(s.strip())>10]
print(f"Decoupage en {len(sentences)} chunks")

os.makedirs("inputs", exist_ok=True)
audios = []

for i, chunk in enumerate(sentences):
    for attempt in range(5):
        try:
            print(f"TTS 3.8 chunk {i+1}/{len(sentences)}: {chunk[:40]}...")
            r = client.models.generate_content(
                model="gemini-3.8-flash-tts",
                contents=chunk,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
                        )
                    )
                )
            )
            data = r.candidates[0].content.parts[0].inline_data.data
            audios.append(AudioSegment.from_file(io.BytesIO(data), format="wav"))
            break
        except Exception as e:
            print(f"Coupure chunk {i} tentative {attempt}: {e}")
            time.sleep(8)
            if attempt==4: raise e

# 3. CONCATENATION = 1min+
final = AudioSegment.empty()
for a in audios:
    final += a + AudioSegment.silent(duration=300) # petite pause

final.export("inputs/audio.wav", format="wav")
print(f"AUDIO FINAL: {len(final)/1000}s - {len(final)}ms")
