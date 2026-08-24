from elevenlabs import ElevenLabs
from elevenlabs import save

client = ElevenLabs(
    api_key="sk_55c1277c28f64159d9c26140c45125b1dace51bf05159c9a"
)

audio = client.text_to_speech.convert(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    text="السلام عليكم",
    model_id="eleven_multilingual_v2"
)

save(audio, "output.mp3")

print("تم إنشاء الملف الصوتي بنجاح.")