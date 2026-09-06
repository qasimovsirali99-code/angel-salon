"""
ANGEL salonu — söhbət və rezervasiya serveri

İki endpoint:
  POST /chat    — müştərinin sualına usta kimi cavab verir (OpenAI)
  POST /rezerv  — yekun sifarişi Telegram-a göndərir

Telegram tokeni YALNIZ burada saxlanılır, brauzerə düşmür.

İşə salmaq:
    pip install fastapi uvicorn httpx openai python-dotenv
    uvicorn server:app --host 0.0.0.0 --port 8100
"""

import os
from datetime import datetime

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from pydantic import BaseModel

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    raise RuntimeError(
        "TELEGRAM_TOKEN və TELEGRAM_CHAT_ID .env faylında olmalıdır. "
        "Token @BotFather-dən, chat id @userinfobot-dan alınır."
    )

llm = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

app = FastAPI(title="ANGEL salon")

# Saytınızın ünvanını yazın. Sınaq üçün ["*"] qoya bilərsiniz,
# amma canlıda mütləq dəqiq domenə daraldın.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://angel.az",
        "https://qasimovsirali99-code.github.io",
        "http://localhost:8000",
    ],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


# ─────────────────────────────────────────────────────────────
# Salon məlumatı — botun bildiyi hər şey
# ─────────────────────────────────────────────────────────────

SALON = """
ANGEL gözəllik salonu, Nizami küçəsi 42, Bakı.
İş saatları: bazar ertəsi — şənbə 10:00–20:00. Bazar günü bağlı.
Son müştəri 19:00-da qəbul olunur. Telefon: +994 12 555 01 42.

USTALAR
- Leyla Hüseynova — rəng və kəsim, 14 il, balayaj üzrə ixtisaslaşır
- Nərmin Əliyeva — dırnaq, 8 il, aparat manikürü
- Səbinə Qasımlı — üz baxımı və qaş, 11 il, kosmetologiya diplomu

QİYMƏTLƏR
Saç: qadın kəsimi 25, kişi kəsimi 15, kök rəngi 45,
     balayaj 120–220, keratin düzləşdirmə 160
Dırnaq: aparat manikürü 20, gel-lak 35, pedikür 40,
        dırnaq uzatma 75, dizayn (bir dırnaq) 3
Üz baxımı: mexaniki təmizləmə 60, ultrasəs təmizləmə 50,
           kimyəvi pilinq 90, alginat maska 45, kurs (4 seans) 180
Qaş və kirpik: qaş forması 12, qaş boyası 18, qaş laminasiyası 40,
               kirpik laminasiyası 45, kirpik uzatma 90
Toy: tədbir makiyajı 80, saç düzümü 90, gəlin paketi 350,
     sınaq görüşü 60, evə gəlmə +50
Bütün qiymətlər manatladır.

VACİB QAYDALAR
- Rəngdən əvvəl bir tel üzərində sınaq edilir.
- Balayajda bir seansda son nəticəyə çatmağa çalışmırıq, saç yanmasın.
- Alətlər hər müştəridən sonra avtoklavda sterilizasiya olunur.
- Ləğvetmə 3 saat əvvəl bildirilsə, haqq tutulmur.
- Toy makiyajı üçün ən azı bir həftə əvvəl sınaq keçirilir.
"""

TALIMAT = f"""Sən Aysel-sən — ANGEL gözəllik salonunun ustası və sahibi.
Müştəri ilə saytdakı söhbət pəncərəsində danışırsan.

{SALON}

NECƏ DANIŞ:
- Azərbaycan dilində, sadə və səmimi. Uzun cümlə qurma.
- Cavabın 3 cümlədən uzun olmasın, siyahı verirsənsə qısa saxla.
- Qiymət soruşanda dəqiq rəqəmi de, "əlaqə saxlayın" demə.
- Bilmədiyin şeyi uydurma. Yuxarıdakı siyahıda olmayan xidmət
  soruşulsa, "onu etmirik" de və yaxın alternativ təklif et.
- Sağlamlıq və ya tibbi məsələdə (dəri xəstəliyi, dərman, allergiya)
  məsləhət vermə — həkimə müraciət etməyi tövsiyə et.
- Müştəri vaxt yazdırmaq istəyirsə, cavabının SONUNA ayrıca sətirdə
  tam olaraq belə yaz: [REZERV]
  Bu işarəni başqa halda yazma.
"""


# ─────────────────────────────────────────────────────────────
# Modellər
# ─────────────────────────────────────────────────────────────

class Danisiq(BaseModel):
    rol: str          # 'usta' ya da 'musteri'
    metn: str


class ChatSorgu(BaseModel):
    sual: str
    tarixce: list[Danisiq] = []


class Rezerv(BaseModel):
    ad: str
    telefon: str
    xidmet: str
    vaxt: str


# ─────────────────────────────────────────────────────────────
# Söhbət
# ─────────────────────────────────────────────────────────────

@app.post("/chat")
async def chat(s: ChatSorgu):
    if llm is None:
        raise HTTPException(503, "OPENAI_API_KEY qurulmayıb")

    if len(s.sual) > 800:
        raise HTTPException(400, "Sual çox uzundur")

    mesajlar = [{"role": "system", "content": TALIMAT}]
    for d in s.tarixce[-8:]:
        mesajlar.append({
            "role": "assistant" if d.rol == "usta" else "user",
            "content": d.metn[:800],
        })
    mesajlar.append({"role": "user", "content": s.sual})

    try:
        cavab = await llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=mesajlar,
            temperature=0.6,
            max_tokens=320,
        )
        metn = (cavab.choices[0].message.content or "").strip()
    except Exception:
        raise HTTPException(502, "Cavab alına bilmədi")

    rezerv_basla = "[REZERV]" in metn
    metn = metn.replace("[REZERV]", "").strip()

    return {"cavab": metn, "rezerv_basla": rezerv_basla}


# ─────────────────────────────────────────────────────────────
# Rezervasiya → Telegram
# ─────────────────────────────────────────────────────────────

def temizle(s: str, uzunluq: int = 120) -> str:
    """Telegram HTML rejimi üçün təhlükəsizləşdirir."""
    s = s[:uzunluq].strip()
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


@app.post("/rezerv")
async def rezerv(r: Rezerv):
    reqemler = "".join(c for c in r.telefon if c.isdigit())
    if len(reqemler) < 9:
        raise HTTPException(400, "Telefon nömrəsi düzgün deyil")
    if not r.ad.strip():
        raise HTTPException(400, "Ad boşdur")

    metn = (
        "<b>Yeni rezervasiya sorğusu</b>\n\n"
        f"<b>Ad:</b> {temizle(r.ad)}\n"
        f"<b>Telefon:</b> {temizle(r.telefon, 30)}\n"
        f"<b>Xidmət:</b> {temizle(r.xidmet)}\n"
        f"<b>İstədiyi vaxt:</b> {temizle(r.vaxt)}\n\n"
        f"<i>{datetime.now():%d.%m.%Y %H:%M}</i> · saytdakı söhbətdən"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            cavab = await c.post(url, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": metn,
                "parse_mode": "HTML",
            })
        if cavab.status_code != 200:
            raise HTTPException(502, "Telegram qəbul etmədi")
    except httpx.HTTPError:
        raise HTTPException(502, "Telegram-a çıxış yoxdur")

    return {"ok": True}


@app.get("/saglamliq")
async def saglamliq():
    return {"ok": True, "ai": llm is not None}
