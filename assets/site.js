/* ОБЩИЕ МЕХАНИЗМЫ САЙТА (все страницы)
   - часы «Открыто сейчас» в шапке
   - меню на телефоне и выпадающий список направлений
   - подсказки вместо звонка (номер в прототипе ненастоящий)
   - даты статей: всегда свежие, считаются от сегодняшнего дня
   - карусели со стрелками
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

/* ---------- Кнопки звонка и записи: в прототипе только подсказка ---------- */
let таймер_подсказки;
document.addEventListener("click",e=>{
  const к = e.target.closest("[data-call],[data-write],[data-book],[data-map]");
  if(!к) return;
  e.preventDefault();
  document.querySelector(".toast")?.remove();
  const п = document.createElement("div");
  п.className="toast";
  п.textContent = к.hasAttribute("data-call") ? "Здесь сразу начнётся звонок в клинику"
               : к.hasAttribute("data-book") ? "Здесь откроется запись: выбор врача и времени"
               : к.hasAttribute("data-map") ? "Здесь откроется маршрут в Яндекс Картах"
               : "Здесь откроется чат в Telegram или MAX";
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
