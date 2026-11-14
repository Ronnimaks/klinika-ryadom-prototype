"""
СБОРКА САЙТА КЛИНИКИ «ИНДИВИТА» (прототип, многостраничный)

Что делает: собирает готовые страницы из исходников - вставляет общую шапку, меню и подвал,
создаёт страницы направлений и статей.
Вход:  _исходники/главная.html, _исходники/стоматология.html (содержимое страниц),
       _исходники/статьи.py (тексты статей), список НАПРАВЛЕНИЯ ниже.
Выход: index.html (главная), stomatologiya/index.html, <направление>/index.html, stati/<статья>/index.html,
       stati/index.html (все статьи).
Запуск: python собрать_сайт.py   (после любой правки исходников)

Почему так: у каждого направления и статьи свой адрес - рекламу ведём сразу на нужную страницу,
и поиск видит много отдельных страниц.
"""
import os, sys, html

ЗДЕСЬ = os.path.dirname(os.path.abspath(__file__))
ИСХОДНИКИ = os.path.join(ЗДЕСЬ, "_исходники")
sys.path.insert(0, ИСХОДНИКИ)
from статьи import СТАТЬИ  # noqa: E402

# ---------- НАСТРОЙКИ: телефон и название (в прототипе - примеры) ----------
ТЕЛЕФОН = "+7 (495) 000-00-00"
НАЗВАНИЕ = "Индивита"   # бренд Давида (klinikaindivita.ru), решение владельца 14.11
ЛОГОТИП = 'Индивита'  # пишется ЗАГЛАВНЫМИ (CSS): буквы и цифры одной высоты (ПРАВИЛА_САЙТА.md)

# ---------- НАПРАВЛЕНИЯ: адрес, название, состояние, коротко, картинка ----------
НАПРАВЛЕНИЯ = [
 ("stomatologiya", "Стоматология", "открыта", "Лечение, удаление, импланты, брекеты. Круглосуточно.", "dir_stom.jpg"),
 ("kt", "КТ и рентген", "открыта", "Объёмный снимок за несколько минут, файл сразу у вас.", "dir_kt.jpg"),
 ("ginekologiya", "Гинекология", "скоро", "Приём, УЗИ и анализы в одном месте.", "dir_gyn.jpg"),
 ("urologiya", "Урология", "скоро", "Приём уролога без долгого ожидания.", "dir_uro.jpg"),
 ("uzi", "УЗИ", "скоро", "Все виды ультразвуковой диагностики.", "dir_uzi.jpg"),
 ("laboratoriya", "Анализы", "скоро", "Своя лаборатория, результаты на почту.", "dir_lab.jpg"),
 ("hirurgiya", "Хирургия", "в планах", "Амбулаторная хирургия и операционная.", "dir_hir.jpg"),
 ("proktologiya", "Проктология", "в планах", "Деликатно, без очередей.", "dir_proct.jpg"),
]


def подпись_состояния(с):
    return {"открыта": "работает", "скоро": "скоро открытие", "в планах": "в планах"}[с]


# ---------- ОБЩАЯ ГОЛОВА СТРАНИЦЫ ----------
def голова(заголовок, описание, к):
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>{html.escape(заголовок)}</title>
<meta name="description" content="{html.escape(описание)}">
<meta name="robots" content="noindex,nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geologica:wght@200;300;400;500&family=Onest:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{к}assets/site.css">
"""


# ---------- ШАПКА С МЕНЮ ----------
def шапка(к, текущий=""):
    пункты = "".join(
        f'<a href="{к}{а}/" class="{"live" if с == "открыта" else ""}">{н}<small>{подпись_состояния(с)}</small></a>'
        for а, н, с, _, _ in НАПРАВЛЕНИЯ)
    def отметка(имя): return ' aria-current="page"' if текущий == имя else ""
    # Разделы стоматологии - в меню из трёх полосок (отдельной строки под шапкой больше нет)
    разделы = ""
    if текущий == "stomatologiya":
        разделы = ('<span class="tag">Стоматология</span>'
                   '<a href="#ask">Что случилось</a><a href="#ct">КТ на месте</a><a href="#night">Как прийти ночью</a>'
                   '<a href="#doctors">Врачи</a><a href="#prices">Цены</a><a href="#where">Где мы</a>')
    return f"""<div class="proto">Прототип. Название, адрес, телефон, цены и фото - примеры, заменим настоящими.</div>
<header class="top">
  <div class="wrap">
    <a class="logo" href="{к}index.html" aria-label="{НАЗВАНИЕ}, на главную">{ЛОГОТИП}</a>
    <div class="open"><i></i><b>Открыто</b> <span>сейчас <span id="clock"></span></span></div>
    <nav class="nav" aria-label="Разделы сайта">
      <div class="drop"><button type="button" aria-expanded="false">Направления</button><div class="drop-menu">{пункты}</div></div>
      <a href="{к}yurlicam/"{отметка("yurlicam")}>Юрлицам</a>
      <a href="{к}stati/"{отметка("stati")}>Статьи</a>
      <a href="{к}stomatologiya/#prices">Цены</a>
      <a href="{к}index.html#contacts">Контакты</a>
      <a class="phone" href="#call" data-call>{ТЕЛЕФОН}</a>
      <a class="btn main sm" href="#book" data-book>Записаться</a>
    </nav>
    <button class="burger" type="button" aria-label="Меню" aria-expanded="false"><i></i></button>
  </div>
</header>
<div class="mobile-menu">
  {разделы}
  <span class="tag">Направления</span>{пункты}
  <span class="tag">Клиника</span>
  <a href="{к}yurlicam/">Юрлицам: медосмотры</a><a href="{к}stati/">Статьи</a><a href="{к}stomatologiya/#prices">Цены</a><a href="{к}index.html#contacts">Контакты</a>
  <a href="#book" data-book>Записаться</a>
</div>
"""


# ---------- ПОДВАЛ ----------
def подвал(к):
    напр = "".join(f'<a href="{к}{а}/">{н}</a>' for а, н, *_ in НАПРАВЛЕНИЯ[:6])
    статьи = "".join(f'<a href="{к}stati/{с["адрес"]}/">{с["заголовок"].split(":")[0]}</a>' for с in СТАТЬИ[:4])
    return f"""<footer>
  <div class="wrap">
    <div class="foot">
      <div><a class="logo" href="{к}index.html">{ЛОГОТИП}</a><p style="margin-top:14px">Многопрофильная клиника в Южном Бутово. Круглосуточно, без выходных.</p><p style="margin-top:10px">Лицензия: номер после выдачи на новый адрес</p></div>
      <div><h4>Направления</h4>{напр}</div>
      <div><h4>Статьи</h4>{статьи}<a href="{к}stati/">Все статьи</a></div>
      <div><h4>Компаниям</h4><a href="{к}yurlicam/">Медосмотры и диспансеризация</a><a href="{к}yurlicam/#zayavka">Заявка от компании</a><h4 style="margin-top:22px">Связь</h4><a href="#call" data-call>{ТЕЛЕФОН}</a><a href="#write" data-write>Написать в чат</a><span style="display:block;padding:3px 0">Москва, Южное Бутово,<br>адрес ТЦ уточняется</span></div>
    </div>
    <p class="warn">Имеются противопоказания. Необходима консультация специалиста.</p>
  </div>
</footer>
<!-- ЧАТ: круглая кнопка справа внизу. Прячется при прокрутке, возвращается через секунду после остановки.
     Внутри демо «цифрового диспетчера 24/7»: готовые вопросы и ответы (site.js, ДИСПЕТЧЕР). -->
<button class="chat-fab" type="button" aria-label="Написать в чат" aria-expanded="false">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8a2.5 2.5 0 0 1-2.5 2.5H10l-4.2 3.6c-.5.4-1.3.1-1.3-.6V16A2.5 2.5 0 0 1 4 13.5z"/></svg>
</button>
<div class="chat" role="dialog" aria-label="Диспетчер клиники" aria-hidden="true">
  <div class="chat-head"><div><b>Диспетчер 24/7</b><span><i></i>на связи круглосуточно</span></div><button type="button" class="chat-x" aria-label="Закрыть чат"></button></div>
  <div class="chat-body" aria-live="polite"></div>
  <div class="chat-quick"></div>
  <form class="chat-form"><input type="text" placeholder="Напишите вопрос" aria-label="Ваш вопрос" autocomplete="off"><button type="submit" aria-label="Отправить"><svg viewBox="0 0 24 24"><path d="M4 12l16-8-6 16-2.5-6.5z"/></svg></button></form>
</div>
<script src="{к}assets/site.js"></script>
"""


СТРЕЛКИ = """<div class="arrows"><button type="button" data-prev aria-label="Назад"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button><button type="button" data-next aria-label="Вперёд"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button></div>"""


def лента_статей(к, заголовок="Свежие статьи"):
    карточки = "".join(f"""<a class="card post" href="{к}stati/{с["адрес"]}/"><div class="ph"><img src="{к}assets/img/{с["картинка"]}" alt="" loading="lazy"></div>
      <time data-ago="{с["дней_назад"]}"{" data-new" if с["дней_назад"] == 0 else ""}></time><h3>{с["заголовок"]}</h3><p>{с["анонс"]}</p></a>""" for с in СТАТЬИ)
    # Лента по кругу: текущая статья по центру, по бокам края соседних, листается бесконечно (site.js, «Лента статей»)
    return f"""<section id="stati" data-loop>
  <div class="wrap">
    <div class="rail-head"><div><span class="tag">Статьи врачей</span><h2 style="margin-top:14px">{заголовок}</h2></div>{СТРЕЛКИ}</div>
  </div>
  <div class="loop"><div class="loop-track">{карточки}</div></div>
  <div class="wrap"><p style="margin-top:28px"><a class="btn line" href="{к}stati/">Все статьи</a></p></div>
</section>"""


def записать(путь, текст):
    полный = os.path.join(ЗДЕСЬ, путь)
    os.makedirs(os.path.dirname(полный), exist_ok=True)
    with open(полный, "w", encoding="utf-8", newline="\n") as ф:
        ф.write(текст)
    print("готово:", путь)


def собрать_из_исходника(имя_исходника, куда, к, текущий):
    """Исходник: строка 1 - заголовок, строка 2 - описание, дальше - <style>, содержимое <main> и <script>.
    Метки {{К}}, {{ЛЕНТА_СТАТЕЙ}}, {{СТРЕЛКИ}}, {{ТЕЛЕФОН}} заменяются при сборке."""
    with open(os.path.join(ИСХОДНИКИ, имя_исходника), encoding="utf-8") as ф:
        заголовок, описание, тело = ф.read().split("\n", 2)
    тело = (тело.replace("{{ЛЕНТА_СТАТЕЙ}}", лента_статей(к)).replace("{{СТРЕЛКИ}}", СТРЕЛКИ)
                .replace("{{ТЕЛЕФОН}}", ТЕЛЕФОН).replace("{{К}}", к))
    стиль, _, остаток = тело.partition("</style>")
    содержимое, _, скрипт = остаток.partition("<!--СКРИПТ-->")
    записать(куда, голова(заголовок, описание, к) + стиль + "</style>\n</head>\n<body>\n" + шапка(к, текущий)
             + содержимое + подвал(к) + скрипт + "\n</body>\n</html>\n")


# ---------- СТРАНИЦА НАПРАВЛЕНИЯ (кроме стоматологии): раздел готовится ----------
def страница_направления(адрес, имя, состояние, коротко, картинка):
    к = "../"
    другие = "".join(f'<a href="{к}{а}/">{н}</a>' for а, н, *_ in НАПРАВЛЕНИЯ if а != адрес)
    if адрес == "kt":
        суть = ('<p class="lead" style="margin-top:22px">Кабинет КТ уже работает рядом с кабинетом стоматолога. '
                'Снимок без записи, <span class="acc">файл сразу в телефон или на почту</span>.</p>'
                f'<p style="margin-top:30px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn main" href="#book" data-book>Записаться на снимок</a>'
                f'<a class="btn line" href="{к}stomatologiya/#ct">Как это устроено</a></p>')
    else:
        суть = ('<p class="lead" style="margin-top:22px">Здесь будет страница направления: врачи, услуги, цены и запись. '
                f'<span class="acc">Направление откроется {"следующим этапом" if состояние == "скоро" else "позже"}.</span> '
                'Оставьте номер - напишем, когда откроем запись.</p>'
                '<p style="margin-top:30px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn main" href="#write" data-write>Сообщить об открытии</a>'
                f'<a class="btn line" href="{к}stomatologiya/">Стоматология уже работает</a></p>')
    содержимое = f"""<main>
<section class="bgphoto" style="min-height:72vh;display:flex;align-items:center">
  <div class="bgimg" style="background-image:url({к}assets/img/{картинка})"></div>
  <div class="wrap">
    <p class="crumbs" style="padding:0 0 30px"><a href="{к}index.html">Главная</a> / {имя}</p>
    <span class="tag">{подпись_состояния(состояние)}</span>
    <h1 style="font-size:clamp(44px,6vw,88px);font-weight:200;margin-top:16px">{имя}</h1>
    <p style="margin-top:14px;font-size:20px">{коротко}</p>
    {суть}
  </div>
</section>
<section style="padding-top:0"><div class="wrap"><span class="tag">Другие направления</span><div class="areas">{другие.replace("<a ", '<a ')}</div></div></section>
</main>
"""
    записать(f"{адрес}/index.html", голова(f"{имя} - {НАЗВАНИЕ}, Южное Бутово", коротко, к)
             + "</head>\n<body>\n" + шапка(к) + содержимое + подвал(к) + "</body>\n</html>\n")


# ---------- СТАТЬЯ ----------
def страница_статьи(с, номер):
    к = "../../"
    абзацы = "".join(f"<h2>{html.escape(т[3:])}</h2>" if т.startswith("## ") else f"<p>{html.escape(т)}</p>" for т in с["текст"])
    другие = [x for x in СТАТЬИ if x is not с][:3]
    ещё = "".join(f'<a class="card post" href="{к}stati/{x["адрес"]}/"><div class="ph"><img src="{к}assets/img/{x["картинка"]}" alt="" loading="lazy"></div><time data-ago="{x["дней_назад"]}"></time><h3>{x["заголовок"]}</h3></a>' for x in другие)
    стиль = """<style>
.article{max-width:760px;margin:0 auto}
.article h1{font-size:clamp(34px,4.6vw,60px);line-height:1.06;margin-top:14px}
.article .hero-ph{margin:34px 0 10px;aspect-ratio:16/9;overflow:hidden}
.article .hero-ph img{width:100%;height:100%;object-fit:cover;display:block}
.article .body p{margin-top:18px;color:#C9D5D2;font-size:18.5px;line-height:1.65}
.article .body h2{font-size:clamp(24px,2.4vw,30px);margin-top:42px;color:var(--lamp)}
.article .cta{margin-top:48px;padding:28px;border:1px solid var(--line);display:flex;justify-content:space-between;gap:20px;align-items:center;flex-wrap:wrap}
.article .cta b{font:300 22px/1.3 var(--display)}
.more{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:30px}
@media (max-width:720px){.more{grid-template-columns:minmax(0,1fr)}}
</style>"""
    содержимое = f"""<main>
<section style="padding-top:0"><div class="wrap">
  <article class="article">
    <p class="crumbs"><a href="{к}index.html">Главная</a> / <a href="{к}stati/">Статьи</a></p>
    <time data-ago="{с["дней_назад"]}" style="display:block;color:var(--lamp);font-size:14px;margin-top:26px"></time>
    <h1>{с["заголовок"]}</h1>
    <p class="lead" style="margin-top:16px">{с["анонс"]}</p>
    <div class="hero-ph"><img src="{к}assets/img/{с["картинка"]}" alt=""></div>
    <div class="body">{абзацы}</div>
    <div class="cta"><b>Болит сейчас? <span class="acc">Мы открыты круглосуточно.</span></b><a class="btn main" href="#book" data-book>Записаться</a></div>
    <p style="margin-top:22px;font-size:13px;color:var(--dim)">Статья носит справочный характер и не заменяет осмотр врача.</p>
  </article>
</div></section>
<section style="padding-top:0"><div class="wrap"><span class="tag">Ещё статьи</span><div class="more">{ещё}</div></div></section>
</main>
"""
    записать(f"stati/{с['адрес']}/index.html", голова(с["заголовок"] + " - " + НАЗВАНИЕ, с["анонс"], к) + стиль
             + "\n</head>\n<body>\n" + шапка(к, "stati") + содержимое + подвал(к) + "</body>\n</html>\n")


def страница_всех_статей():
    к = "../"
    карточки = "".join(f'<a class="card post rise" href="{к}stati/{с["адрес"]}/"><div class="ph"><img src="{к}assets/img/{с["картинка"]}" alt="" loading="lazy"></div><time data-ago="{с["дней_назад"]}"{" data-new" if с["дней_назад"] == 0 else ""}></time><h3>{с["заголовок"]}</h3><p>{с["анонс"]}</p></a>' for с in СТАТЬИ)
    содержимое = f"""<main>
<section style="padding-top:0"><div class="wrap">
  <p class="crumbs"><a href="{к}index.html">Главная</a> / Статьи</p>
  <h1 style="font-size:clamp(40px,5.4vw,76px);font-weight:200;margin-top:30px">Статьи <em style="font-style:normal;color:var(--lamp)">врачей</em></h1>
  <p class="lead" style="margin-top:16px">Простыми словами о том, что делать, когда болит, и как проходит лечение. Новые статьи выходят каждую неделю.</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:36px 18px;margin-top:44px">{карточки}</div>
</div></section>
</main>
"""
    записать("stati/index.html", голова("Статьи - " + НАЗВАНИЕ, "Статьи врачей клиники", к)
             + "</head>\n<body>\n" + шапка(к, "stati") + содержимое + подвал(к) + "</body>\n</html>\n")


if __name__ == "__main__":
    собрать_из_исходника("главная.html", "index.html", "", "главная")
    собрать_из_исходника("стоматология.html", "stomatologiya/index.html", "../", "stomatologiya")
    собрать_из_исходника("юрлица.html", "yurlicam/index.html", "../", "yurlicam")
    for н in НАПРАВЛЕНИЯ:
        if н[0] != "stomatologiya":
            страница_направления(*н)
    for номер, с in enumerate(СТАТЬИ):
        страница_статьи(с, номер)
    страница_всех_статей()
