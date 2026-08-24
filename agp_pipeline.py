import os
import subprocess
from pydub import AudioSegment

# --- 1. إعدادات اللوحة والمقاطع الصوتية ---
SERIAL_NUMBER = "AGP-2026-001"  # الرقم التسلسلي للوحة
VOICE_FILE = "voice.mp3"         # صوت التعليق الصوتي للوحة
MUSIC_FILE = "music.mp3"         # الموسيقى الخلفية
ARTWORK_TITLE = "كنوز الذهب | Gold Treasures"

# --- 2. دمج الصوت والتعديل الآلي ---
def process_artwork_audio(serial_no, voice_path, music_path):
    output_dir = f"artworks/{serial_no}"
    os.makedirs(output_dir, exist_ok=True)
    output_audio_path = f"{output_dir}/{serial_no}.mp3"

    print(f"--- [AGP Pipeline] معالجة المقطع الصوتي للوحة: {serial_no} ---")

    if os.path.exists(voice_path):
        voice = AudioSegment.from_file(voice_path)
        
        if os.path.exists(music_path):
            music = AudioSegment.from_file(music_path) - 12  # خفض صوت الموسيقى خلف التعليق
            if len(music) < len(voice):
                music = music * (len(voice) // len(music) + 1)
            music = music[:len(voice)]
            final_audio = voice.overlay(music)
        else:
            final_audio = voice

        # تصدير المقطع الصوتي بدقة جيدة وحجم خفيف
        final_audio.export(output_audio_path, format="mp3", bitrate="128k")
        print(f"✅ تم حفظ المقطع الصوتي النهائي: {output_audio_path}")
    else:
        print(f"⚠️ لم يتم العثور على ملف الصوت الأساسي: {voice_path}")
        return False

    # --- 3. إنشاء صفحة التشغيل الذهبية ---
    html_content = f"""<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{ARTWORK_TITLE}</title>
    <style>
        body {{ background-color: #000; color: #d4af37; font-family: 'Segoe UI', Tahoma, sans-serif; text-align: center; padding: 40px 20px; }}
        .container {{ max-width: 500px; margin: auto; border: 2px solid #d4af37; padding: 30px; border-radius: 15px; box-shadow: 0 0 20px rgba(212,175,55,0.2); }}
        h1 {{ font-size: 1.8rem; margin-bottom: 10px; }}
        .serial {{ color: #888; font-size: 0.9rem; margin-bottom: 25px; }}
        audio {{ width: 100%; margin-top: 20px; outline: none; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{ARTWORK_TITLE}</h1>
        <div class="serial">Serial: {serial_no}</div>
        <p>المقطع الصوتي الرسمي للوحة الفنية</p>
        <audio controls autoplay controlsList="nodownload">
            <source src="{serial_no}.mp3" type="audio/mpeg">
            متصفحك لا يدعم تشغيل المقطع الصوتي.
        </audio>
    </div>
</body>
</html>"""

    with open(f"{output_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ تم إنشاء واجهة تشغيل الصوت: {output_dir}/index.html")
    return True

# --- 4. الرفع التلقائي للسيفر ---
def push_to_github(serial_no):
    print("\n[AGP] جاري رفع المقطع الصوتي إلى GitHub...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Add audio clip for artwork {serial_no}"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("🎉 تم الرفع بنجاح! المقطع الصوتي والصفحة أونلاين الآن.")
    except Exception as e:
        print(f"⚠️ حدث خطأ أثناء الرفع: {e}")

if __name__ == "__main__":
    if process_artwork_audio(SERIAL_NUMBER, VOICE_FILE, MUSIC_FILE):
        push_to_github(SERIAL_NUMBER)