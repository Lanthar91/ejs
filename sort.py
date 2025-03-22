import os
import shutil
import json

SOURCE_DIR = "roms_unsorted"
TARGET_DIR = "roms"
COVER_DIR = "covers"
JSON_FILE = "roms.json"

# Расширения и платформы с ядрами EmulatorJS
CORE_MAP = {
    "nes":       ["nes", "unf", "unif", "fds"],
    "snes":      ["smc", "sfc"],
    "gba":       ["gba"],
    "gb":        ["gb"],
    "n64":       ["z64", "n64"],
    "nds":       ["nds"],
    "pce":       ["pce"],
    "ws":        ["ws", "wsc"],
    "ngp":       ["ngp", "ngc"],
    "coleco":    ["col", "cv"],
    "segaMD":    ["gen", "md", "bin"]  # Sega Mega Drive / Genesis
}

def get_core_from_extension(ext):
    ext = ext.lower()
    for core, exts in CORE_MAP.items():
        if ext in exts:
            return core
    return None

roms_dict = {}
os.makedirs(TARGET_DIR, exist_ok=True)

for filename in os.listdir(SOURCE_DIR):
    file_path = os.path.join(SOURCE_DIR, filename)
    if not os.path.isfile(file_path):
        continue

    name, ext = os.path.splitext(filename)
    ext = ext.lstrip(".")
    core = get_core_from_extension(ext)

    if core is None:
        print(f"❌ Пропущен: {filename}")
        continue

    target_folder = os.path.join(TARGET_DIR, core)
    os.makedirs(target_folder, exist_ok=True)

    dst_path = os.path.join(target_folder, filename)
    if not os.path.exists(dst_path):
        shutil.copy2(file_path, dst_path)
        print(f"✅ Скопировано: {filename} → {core}/")
    else:
        print(f"⚠️ Уже существует: {filename}")

    # Ищем обложку
    cover_path = ""
    for ext_cover in [".png", ".jpg", ".jpeg"]:
        cover_candidate = os.path.join(COVER_DIR, f"{name}{ext_cover}")
        if os.path.exists(cover_candidate):
            cover_path = cover_candidate.replace("\\", "/")
            break

    rom_entry = {
        "file": dst_path.replace("\\", "/"),
        "cover": cover_path,
        "core": core
    }

    roms_dict.setdefault(core.upper(), []).append(rom_entry)

# Сохраняем JSON
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(roms_dict, f, indent=2)

print(f"\n📦 Готово! JSON-файл сохранен как {JSON_FILE}")
