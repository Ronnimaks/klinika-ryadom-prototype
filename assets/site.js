/* ОБЩИЕ МЕХАНИЗМЫ САЙТА (все страницы)
   - часы «Открыто сейчас» в шапке
   - меню на телефоне и выпадающий список направлений
   - подсказки вместо звонка (номер в прототипе ненастоящий)
   - даты статей: всегда свежие, считаются от сегодняшнего дня
   - карусели со стрелками (врачи) и лента статей по кругу
   - чат: круглая кнопка и демо цифрового диспетчера 24/7
   - плавное появление блоков и медленный сдвиг фоновых фото при прокрутке */

/* ---------- Часы в шапке ---------- */
function обновить_часы(){
  const т = new Date(), место = document.getElementById("clock");
  if(место) место.textContent = String(т.getHours()).padStart(2,"0")+":"+String(т.getMinutes()).padStart(2,"0");
}
обновить_часы(); setInterval(обновить_часы, 20000);

/* ---------- Меню ---------- */
document.querySelector(".burger")?.addEventListener("click",()=>{
  const открыто = document.body.classList.toggle("menu-open");
  document.querySelector(".burger").setAttribute("aria-expanded", открыто);
});
document.querySelectorAll(".drop>button").forEach(к=>к.addEventListener("click",()=>{
  const откр = к.parentElement.classList.toggle("on"); к.setAttribute("aria-expanded", откр);
}));
document.addEventListener("click",e=>{ if(!e.target.closest(".drop")) document.querySelectorAll(".drop.on").forEach(д=>д.classList.remove("on")); });
// Нажали пункт меню - меню закрывается (иначе якорь «Врачи» прокрутит страницу под открытым меню)
document.querySelectorAll(".mobile-menu a").forEach(с=>с.addEventListener("click",()=>{
  document.body.classList.remove("menu-open"); document.querySelector(".burger")?.setAttribute("aria-expanded",false);
}));

/* ---------- Кнопки звонка и записи: в прототипе только подсказка ---------- */
let таймер_подсказки;
document.addEventListener("click",e=>{
  const к = e.target.closest("[data-call],[data-write],[data-book],[data-map]");
  if(!к) return;
  e.preventDefault();
  if(к.hasAttribute("data-write")){ открыть_чат(); return; }   // «Написать» везде открывает чат
  document.querySelector(".toast")?.remove();
  const п = document.createElement("div");
  п.className="toast";
  п.textContent = к.hasAttribute("data-call") ? "Здесь сразу начнётся звонок в клинику"
               : к.hasAttribute("data-book") ? "Здесь откроется запись: выбор врача и времени"
               : "Здесь откроется маршрут в Яндекс Картах";
  document.body.append(п);
  clearTimeout(таймер_подсказки); таймер_подсказки=setTimeout(()=>п.remove(),2400);
});

/* ---------- Даты статей ----------
   Для показа: дата у статьи = сегодня минус data-ago дней. Открыли сайт 12.11 - верхняя статья от 12.11. */
const МЕСЯЦЫ = ["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"];
document.querySelectorAll("time[data-ago]").forEach(т=>{
  const д = new Date(); д.setDate(д.getDate() - Number(т.dataset.ago||0));
  т.dateTime = д.toISOString().slice(0,10);
  const сегодня = т.dataset.ago === "0";
  т.innerHTML = (сегодня ? "Сегодня, " : "") + д.getDate()+" "+МЕСЯЦЫ[д.getMonth()]+" "+д.getFullYear()
               + (сегодня && т.hasAttribute("data-new") ? '<span class="new">новое</span>' : "");
});

/* ---------- Карусели со стрелками ---------- */
document.querySelectorAll("[data-rail]").forEach(блок=>{
  const лента = блок.querySelector(".rail"), назад = блок.querySelector("[data-prev]"), вперёд = блок.querySelector("[data-next]");
  if(!лента) return;
  const шаг = ()=> (лента.firstElementChild?.getBoundingClientRect().width||300) + 18;
  назад?.addEventListener("click",()=>лента.scrollBy({left:-шаг(),behavior:"smooth"}));
  вперёд?.addEventListener("click",()=>лента.scrollBy({left:шаг(),behavior:"smooth"}));
  const кнопки = ()=>{ if(назад) назад.disabled = лента.scrollLeft < 8;
    if(вперёд) вперёд.disabled = лента.scrollLeft + лента.clientWidth > лента.scrollWidth - 8; };
  лента.addEventListener("scroll",кнопки,{passive:true}); addEventListener("resize",кнопки); кнопки();
});

/* ---------- Появление блоков ---------- */
const наблюдатель = new IntersectionObserver(записи=>записи.forEach(з=>{ if(з.isIntersecting){ з.target.classList.add("in"); наблюдатель.unobserve(з.target);} }),{rootMargin:"0px 0px -8% 0px"});
document.querySelectorAll(".rise").forEach(э=>наблюдатель.observe(э));

/* ---------- Фоновые фото и кадры медленно сдвигаются при прокрутке ---------- */
const ФОНЫ = [...document.querySelectorAll(".bgphoto>.bgimg, [data-parallax] img")];
function сдвиг_фонов(){
  ФОНЫ.forEach(ф=>{ const р=ф.parentElement.getBoundingClientRect();
    if(р.bottom<0||р.top>innerHeight) return;
    const д=(р.top+р.height/2-innerHeight/2)/(innerHeight+р.height);
    ф.style.transform = ф.tagName==="IMG" ? `translate3d(0,${(-8+д*-16).toFixed(2)}%,0)` : `translate3d(0,${(д*-8).toFixed(2)}%,0)`; });
}
if(!matchMedia("(prefers-reduced-motion: reduce)").matches){ addEventListener("scroll",сдвиг_фонов,{passive:true}); сдвиг_фонов(); }

/* ---------- Лента статей по кругу ----------
   Карточки повторены трижды: [копия][настоящие][копия]. Листаем по средней тройке; дошли до копии -
   незаметно перескакиваем на ту же статью в середине. Поэтому листать можно бесконечно в обе стороны. */
document.querySelectorAll("[data-loop]").forEach(блок=>{
  const окно = блок.querySelector(".loop"), дорожка = блок.querySelector(".loop-track");
  const исходные = [...дорожка.children], N = исходные.length;
  if(!N) return;
  исходные.forEach(к=>дорожка.append(к.cloneNode(true)));
  исходные.slice().reverse().forEach(к=>дорожка.prepend(к.cloneNode(true)));
  const все = [...дорожка.children];
  let номер = N, ширина = 0, зазор = 22;

  function размер(){
    const ш = окно.clientWidth;
    ширина = ш <= 720 ? Math.round(ш*.8) : Math.min(620, Math.round(ш*.46));   // по бокам видны края соседних
    зазор = ш <= 720 ? 12 : 22;
    все.forEach(к=>к.style.setProperty("--w", ширина+"px"));
    поставить(false);
  }
  function поставить(плавно, сдвиг=0){
    дорожка.classList.toggle("anim", плавно);
    const x = окно.clientWidth/2 - (номер*(ширина+зазор) + ширина/2) + сдвиг;
    дорожка.style.transform = `translate3d(${x}px,0,0)`;
    все.forEach((к,и)=>к.classList.toggle("on", и===номер));
  }
  function листать(на){ номер += на; поставить(true); }
  дорожка.addEventListener("transitionend",e=>{
    if(e.target!==дорожка) return;
    if(номер < N){ номер += N; поставить(false); }        // ушли в левую копию - прыжок в середину
    else if(номер >= 2*N){ номер -= N; поставить(false); } // ушли в правую копию
  });
  блок.querySelector("[data-prev]")?.addEventListener("click",()=>листать(-1));
  блок.querySelector("[data-next]")?.addEventListener("click",()=>листать(1));

  // Палец и мышь: тянем ленту; отпустили - листаем на соседнюю, если сдвинули достаточно
  let старт = null, сдвиг = 0, тянули = false;
  окно.addEventListener("pointerdown",e=>{ старт = e.clientX; сдвиг = 0; тянули = false; });
  addEventListener("pointermove",e=>{
    if(старт===null) return;
    сдвиг = e.clientX - старт;
    if(Math.abs(сдвиг) > 6){ тянули = true; поставить(false, сдвиг); }
  });
  addEventListener("pointerup",()=>{
    if(старт===null) return;
    старт = null;
    if(Math.abs(сдвиг) > 50) листать(сдвиг < 0 ? 1 : -1); else if(тянули) поставить(true);
  });
  addEventListener("pointercancel",()=>{ if(старт!==null){ старт = null; поставить(true); } });
  // Нажатие на боковую статью листает к ней, на центральную - открывает её
  все.forEach((к,и)=>к.addEventListener("click",e=>{
    if(тянули){ e.preventDefault(); тянули = false; return; }
    if(и!==номер){ e.preventDefault(); листать(и - номер); }
  }));
  addEventListener("resize",размер); размер();
});

/* ---------- Чат: кнопка-кружок ----------
   Пока страницу листают - кнопка прячется «бульком», через секунду после остановки появляется снова. */
const КНОПКА_ЧАТА = document.querySelector(".chat-fab"), ЧАТ = document.querySelector(".chat");
let таймер_чата;
addEventListener("scroll",()=>{
  if(!КНОПКА_ЧАТА || document.body.classList.contains("chat-open")) return;
  КНОПКА_ЧАТА.classList.add("hid");
  clearTimeout(таймер_чата);
  таймер_чата = setTimeout(()=>КНОПКА_ЧАТА.classList.remove("hid"), 1000);
},{passive:true});

/* ---------- Цифровой диспетчер 24/7: демо на готовых вопросах и ответах ----------
   Настоящего диспетчера подключим позже. Здесь только показ, как это будет выглядеть.
   Ответы без выдуманных фактов о клинике: где данных нет, обещаем уточнить. */
const ДИСПЕТЧЕР = [
  {вопрос:"Болит зуб, можно сейчас?", слова:["болит","боль","сейчас","срочно","ночью"],
   ответ:"Да, приезжайте без записи: мы работаем круглосуточно. Ночью вход с торца здания, у двери домофон. Напишите имя и номер - предупрежу администратора, что вы едете."},
  {вопрос:"Как пройти ночью?", слова:["пройти","вход","дорога","адрес","где"],
   ответ:"Днём - через главный вход ТЦ на второй этаж. Ночью - отдельный вход с торца здания, вывеска видна с дороги. Лифт на второй этаж работает всю ночь."},
  {вопрос:"Сколько стоит?", слова:["стоит","цена","стоимость","сколько","деньги"],
   ответ:"Цены по ситуациям есть в разделе «Цены». Врач называет сумму до начала лечения - без сюрпризов."},
  {вопрос:"Нужен снимок КТ", слова:["кт","снимок","томограф","рентген"],
   ответ:"Кабинет КТ за соседней дверью от стоматолога. Снимок занимает несколько минут, файл отправим вам в телефон или вашему врачу."},
  {вопрос:"Принимаете детей?", слова:["ребёнок","ребенок","дети","детей","сын","дочь"],
   ответ:"Да, у нас есть детский стоматолог. Подскажите возраст ребёнка и что беспокоит - уточню, кто из врачей на смене."},
  {вопрос:"Записаться на приём", слова:["записаться","запись","приём","прием","время"],
   ответ:"С удовольствием запишу. Напишите удобный день и время, имя и номер телефона - администратор подтвердит запись."}
];
const ТЕЛО_ЧАТА = ЧАТ?.querySelector(".chat-body"), ПОДСКАЗКИ = ЧАТ?.querySelector(".chat-quick");
let чат_начат = false;
function сообщение(текст, чьё){
  const м = document.createElement("div"); м.className = "msg " + чьё; м.textContent = текст;
  ТЕЛО_ЧАТА.append(м); ТЕЛО_ЧАТА.scrollTop = ТЕЛО_ЧАТА.scrollHeight; return м;
}
function ответить(текст){
  const печатает = сообщение("", "bot typing"); печатает.innerHTML = "<i></i><i></i><i></i>";
  ТЕЛО_ЧАТА.scrollTop = ТЕЛО_ЧАТА.scrollHeight;
  setTimeout(()=>{ печатает.remove(); сообщение(текст, "bot"); }, 900 + Math.min(1400, текст.length*8));
}
function найти_ответ(вопрос){
  const в = вопрос.toLowerCase();
  const п = ДИСПЕТЧЕР.find(д=>д.слова.some(с=>в.includes(с)));
  return п ? п.ответ : "Передал ваш вопрос администратору, он ответит здесь же. Если болит сильно - приезжайте без записи, мы открыты круглосуточно.";
}
function спросить(текст){
  if(!текст.trim()) return;
  сообщение(текст, "me");
  ответить(найти_ответ(текст));
}
function открыть_чат(){
  if(!ЧАТ) return;
  document.body.classList.add("chat-open");
  ЧАТ.setAttribute("aria-hidden","false"); КНОПКА_ЧАТА?.setAttribute("aria-expanded","true");
  if(!чат_начат){
    чат_начат = true;
    ответить("Здравствуйте! Я диспетчер клиники, на связи круглосуточно. Что случилось? Выберите вопрос или напишите свой.");
    ДИСПЕТЧЕР.forEach(д=>{ const к = document.createElement("button"); к.type="button"; к.textContent = д.вопрос;
      к.addEventListener("click",()=>{ сообщение(д.вопрос,"me"); ответить(д.ответ); }); ПОДСКАЗКИ.append(к); });
  }
}
function закрыть_чат(){
  document.body.classList.remove("chat-open");
  ЧАТ?.setAttribute("aria-hidden","true"); КНОПКА_ЧАТА?.setAttribute("aria-expanded","false");
}
КНОПКА_ЧАТА?.addEventListener("click",открыть_чат);
ЧАТ?.querySelector(".chat-x").addEventListener("click",закрыть_чат);
ЧАТ?.querySelector(".chat-form").addEventListener("submit",e=>{
  e.preventDefault(); const поле = e.target.querySelector("input"); спросить(поле.value); поле.value = "";
});
addEventListener("keydown",e=>{ if(e.key==="Escape") закрыть_чат(); });
