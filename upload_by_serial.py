import os
import sys
from huggingface_hub import HfApi

# إجبار محرر الأوامر في ويندوز على استخدام ترميز UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stdin.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# 1. إعدادات الحساب
HF_TOKEN = "Enter your Hugging Face Token:"
REPO_ID = "alwan-protocol/gold-treasures-audio"

# 2. قراءة الرمز التسلسلي للوحة
if len(sys.argv) > 1:
    serial_number = sys.argv[1].strip()
else:
    serial_number = input("ادخل الرمز التسلسلي للوحة (مثال: AGP-2026-001): ").strip()

if not serial_number:
    print("[!] لم يتم إدخال رمز تسلسلي!")
    exit(1)

# 3. تحديد ملفات الصوت الخاصة بالرمز المدخل (عربي وإنجليزي)
file_ar = f"{serial_number}-AR.mp3"
file_en = f"{serial_number}-EN.mp3"

paths_to_check = [
    "",
    f"artworks/{serial_number}/",
    "audio/"
]

def get_local_path(filename):
    for path in paths_to_check:
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            return full_path
    return None

local_ar = get_local_path(file_ar)
local_en = get_local_path(file_en)

# 4. الرفع إلى Hugging Face
api = HfApi()

def upload(local_path, filename, lang):
    if local_path:
        repo_path = f"audio/{filename}"
        print(f"[*] جاري رفع المقطع ({lang}): {filename}...")
        api.upload_file(
            path_or_fileobj=local_path,
            path_in_repo=repo_path,
            repo_id=REPO_ID,
            repo_type="dataset",
            token=HF_TOKEN
        )
        url = f"https://huggingface.co/datasets/{REPO_ID}/resolve/main/{repo_path}"
        print(f"[OK] تم الرفع بنجاح! الرابط المباشر:\n   {url}\n")
    else:
        print(f"[!] الملف غير موجود محليا: {filename}\n")

print(f"\n--- بدء رفع المقاطع الصوتية للوحة: [{serial_number}] ---\n")
upload(local_ar, file_ar, "العربي")
upload(local_en, file_en, "الإنجليزي")
print("--- اكتملت العملية للوحة المحددة! ---")