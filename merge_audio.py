import os
import sys

# 1. إجبار موجه الأوامر على استخدام ترميز UTF-8 لمنع أخطاء الطباعة
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 2. تفعيل مسارات ffmpeg أولاً قبل استيراد pydub
import static_ffmpeg
static_ffmpeg.add_paths()

from pydub import AudioSegment

# =========================================================
# ⚙️ مدخلات اللوحة الحالية
# =========================================================
SERIAL_NUMBER = "AGP-2026-001"    # الرقم التسلسلي للوحة
VOICE_FILE    = "voice.mp3"         # اسم ملف التعليق الصوتي
MUSIC_FILE    = "music.mp3"         # اسم ملف الخلفية الموسيقية

# =========================================================
# 📁 التسمية التلقائية وإنشاء المجلدات
# =========================================================
ARTWORK_DIR  = f"artworks/{SERIAL_NUMBER}"
OUTPUT_AUDIO = f"{ARTWORK_DIR}/{SERIAL_NUMBER}.mp3"

# إنشاء مجلد mخصص للوحة تلقائياً
os.makedirs(ARTWORK_DIR, exist_ok=True)

print(f"--- [AGP] Processing Artwork: {SERIAL_NUMBER} ---")
print(f"Voice File: {VOICE_FILE}")
print(f"Music File: {MUSIC_FILE}")

# 1. تحميل الملفات الصوتية
voice = AudioSegment.from_file(VOICE_FILE)
music = AudioSegment.from_file(MUSIC_FILE)

# 2. تكرار الموسيقى إذا كانت أقصر من الصوت البشري
if len(music) < len(voice):
    multiplier = int(len(voice) / len(music)) + 2
    music = music * multiplier

chunk_length = 500  # بالميلي ثانية
processed_music = AudioSegment.empty()

# 3. معالجة خفض الموسيقى الذكي (Auto-Ducking)
for i in range(0, len(voice), chunk_length):
    chunk_voice = voice[i:i + chunk_length]
    music_chunk = music[i:i + chunk_length]

    if chunk_voice.dBFS > -35:  # يوجد كلام
        processed_music += (music_chunk - 25)
    else:                       # توقف أو صمت
        processed_music += (music_chunk - 12)

# 4. استمرار الموسيقى المتبقية بعد انتهاء الكلام
remaining_music = music[len(voice):] - 3
processed_music += remaining_music

# 5. دمج الصوت مع الموسيقى
final_mix = processed_music.overlay(voice)

# 6. التصدير والحفظ في مجلد اللوحة المخصص
final_mix.export(OUTPUT_AUDIO, format="mp3", bitrate="192k")

print(f"SUCCESS: Audio file saved to {OUTPUT_AUDIO}")