# ЗАБРАТЬ КАРТИНКИ ИЗ ЗАГРУЗОК В САЙТ
# Что делает: берёт из папки «Загрузки» файлы ryadom_<имя>.png (их скачивает ChatGPT),
#   сохраняет в assets/img/<имя>.jpg в хорошем качестве (90) без уменьшения.
# Зачем: прошлые картинки были мутными из-за снимков экрана и сильного сжатия.
# Запуск: python _исходники/забрать_картинки.py
from pathlib import Path
from PIL import Image

ЗАГРУЗКИ = Path.home() / "Downloads"
КУДА = Path(__file__).resolve().parent.parent / "assets" / "img"

for файл in sorted(ЗАГРУЗКИ.glob("ryadom_*.png")):
    имя = файл.stem.removeprefix("ryadom_")
    картинка = Image.open(файл).convert("RGB")
    картинка.save(КУДА / f"{имя}.jpg", "JPEG", quality=90, optimize=True)
    print(f"{имя}.jpg  {картинка.size[0]}x{картинка.size[1]}")
