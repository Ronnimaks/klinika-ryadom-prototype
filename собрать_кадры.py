"""
КАДРЫ ДЛЯ ПРОТОТИПА. Обрезает снимки экрана с картинками из ChatGPT и пишет текст на пустую вывеску.
Вход: снимки в папке assets_сырьё (ночной вход, холл, кабинет, дневной вход), размер 1536x730, картинка занимает левые 1297 точек.
Выход: assets/entry.jpg, entry_day.jpg, hall.jpg, cabinet.jpg
Запуск: python собрать_кадры.py
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ЗДЕСЬ = os.path.dirname(os.path.abspath(__file__))
СЫРЬЁ = os.path.join(ЗДЕСЬ, "assets_сырьё")
ГОТОВО = os.path.join(ЗДЕСЬ, "assets")
ШРИФТ = r"C:\Windows\Fonts\segoeuil.ttf"
ТЕКСТ_ВЫВЕСКИ = "СТОМАТОЛОГИЯ 24 ЧАСА"


def коэффициенты_перспективы(куда, откуда):
    # Стандартная формула для PIL: переводит плоскую надпись на вывеску, снятую под углом.
    строки = []
    for (x, y), (u, v) in zip(куда, откуда):
        строки.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        строки.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    return np.linalg.solve(np.array(строки, float), np.array(откуда, float).reshape(8))


def написать_на_вывеске(кадр, углы, цвет):
    # углы: левый верх, правый верх, правый низ, левый низ - по кадру 1297x730
    Ш, В = 1600, 240
    плоская = Image.new("RGBA", (Ш, В), (0, 0, 0, 0))
    рисунок = ImageDraw.Draw(плоская)
    шрифт = ImageFont.truetype(ШРИФТ, 118)
    рамка = рисунок.textbbox((0, 0), ТЕКСТ_ВЫВЕСКИ, font=шрифт)
    x = (Ш - (рамка[2] - рамка[0])) / 2 - рамка[0]
    y = (В - (рамка[3] - рамка[1])) / 2 - рамка[1]
    рисунок.text((x, y), ТЕКСТ_ВЫВЕСКИ, font=шрифт, fill=цвет)
    к = коэффициенты_перспективы(углы, [(0, 0), (Ш, 0), (Ш, В), (0, В)])
    слой = плоская.transform(кадр.size, Image.PERSPECTIVE, к, Image.BICUBIC)
    return Image.alpha_composite(кадр.convert("RGBA"), слой).convert("RGB")


def обрезать(имя):
    return Image.open(os.path.join(СЫРЬЁ, имя)).convert("RGB").crop((0, 0, 1297, 730))


os.makedirs(ГОТОВО, exist_ok=True)
for имя, куда in (("hall.jpg", "hall.jpg"), ("cabinet.jpg", "cabinet.jpg"), ("pano.jpg", "pano.jpg")):
    обрезать(имя).save(os.path.join(ГОТОВО, куда), quality=84)
написать_на_вывеске(обрезать("entry.jpg"), [(687, 134), (1081, 68), (1081, 160), (687, 201)], (58, 34, 8, 255)).save(
    os.path.join(ГОТОВО, "entry.jpg"), quality=84)
if os.path.exists(os.path.join(СЫРЬЁ, "entry_day.jpg")):
    написать_на_вывеске(обрезать("entry_day.jpg"), [(685, 137), (1085, 68), (1085, 152), (685, 202)], (13, 34, 38, 255)).save(
        os.path.join(ГОТОВО, "entry_day.jpg"), quality=84)
print("готово", os.listdir(ГОТОВО))
