# ANGEL — gözəllik salonu saytı

## İşə salmaq

`index.html` faylını brauzerdə açın. Başqa heç nə lazım deyil.

Qovluq quruluşu:

```
index.html          — bütün sayt (HTML + CSS + JS bir faylda)
lib/three.min.js    — 3D kitabxanası (yerli, internet lazım deyil)
server.py           — söhbət botu və Telegram üçün server (istəyə bağlı)
```

Saytı yerləşdirəndə **hər iki faylı** birlikdə köçürün. `lib/` qovluğu
olmasa, sayt avtomatik CDN-dən yükləməyə çalışır, amma internet tələb edir.

## Nəyi dəyişmək lazımdır

Sayt nümunədir — aşağıdakılar uydurmadır, real məlumatınızla əvəz edin:

- **Salon adı** — `index.html` içində `ANGEL` yazılan yerlər (naviqasiya,
  hero başlığı, footer). Hero başlığında hər hərf ayrı `<span>`-dır,
  çünki bir-bir qalxır.
- **Ünvan və telefon** — `Nizami küçəsi 42` və `+994 12 555 01 42`
  (bir neçə yerdə təkrarlanır, hamısını dəyişin).
- **Ustalar** — `class="usta"` bloklarında adlar, sahələr, təcrübə illəri.
- **Giriş mətni** — salonun sahibi adından yazılmış hissə.
- **Footer-dəki qeyd** — "Bu nümunə saytdır" sətrini silin.

## Xidmətlər və qiymətlər

İkisi də JS-də massiv kimi saxlanılır, HTML-i əl ilə düzəltmək lazım deyil.

`XIDMETLER` — açılan sətirlər:

```js
{
  ad:'Saç',
  aralig:'25 – 220 ₼',
  izah:'Kəsim, rəng, balayaj...',
  siyahi:[
    ['Qadın kəsimi','25 ₼'],
    ['Balayaj','120 – 220 ₼']
  ]
}
```

`QIYMETLER` — cədvəl sətirləri, hər biri `[ad, vaxt, qiymət]`.

## Rezervasiya forması

**Forma hazırda heç nə göndərmir.** Doldurub göndərəndə nəyin
göndəriləcəyini göstərir, vəssalam. Real işləməsi üçün seçimlər:

- **Formspree / Getform** kimi xidmət — kod yazmadan, `<form>` teqinə
  `action` əlavə etmək kifayətdir
- **WhatsApp** — məlumatı hazır mesaj kimi WhatsApp linkinə yönləndirmək
- **Öz serveriniz** — `fetch()` ilə POST sorğusu

Formanın altındaki "Bu forma hələ serverə bağlanmayıb" qeydini
bağlantı qurduqdan sonra silin.

## 3D hissə

Hero-dakı forma three.js ilə çəkilir: iki halqa, mərkəz kürəsi və beş
kiçik kürə. Sedef görünüşü doku faylından deyil, üç rəngli işıqdan gəlir
(gavalı, adaçayı, qızılı) — ona görə fayl ölçüsü kiçikdir.

Dəyişmək istəsəniz, `3D SƏHNƏ` bölməsinə baxın:

- `gavaliIsiq`, `adacayiIsiq`, `qizilIsiq` — rəng və güc
- `halqa`, `halqa2`, `mervari` — formaların ölçüsü
- `yerler` massivi — kiçik kürələrin orbit radiusu və yüksəkliyi

Telefonlarda avtomatik olaraq daha az detal çəkilir və kamera geri
çəkilir. Brauzerdə "hərəkəti azalt" ayarı açıqsa, forma tərpənmir.

## Şriftlər

Bodoni Moda və Jost Google Fonts-dan yüklənir, yəni ilk açılışda
internet lazımdır. Şriftləri də yerli saxlamaq istəsəniz,
[google-webfonts-helper](https://gwfh.mranftl.com) ilə endirib
`@font-face` yaza bilərsiniz.


## Hero fonu

Fon dörd qatdan ibarətdir:

1. Kənarlarda rəngli işıq zonaları (gavalı, jade, qızılı)
2. **Divar rəsmi** — xətlə çəkilmiş qadın profili, qırmızı dodaqlarla
3. İncə dənəvər doku
4. Kənarlara doğru yumşaq qaralma

Divar rəsmi tamamilə SVG-dir, şəkil faylı deyil — istənilən ölçüdə
kəskin qalır. Səhifə açılanda xətlər özlərini çəkir (2.3 saniyə), saç
isə yavaş-yavaş yellənir. Rəngini və qalınlığını dəyişmək üçün `.hero-divar .cizgi`
(profil), `.hero-divar .sac-cizgi` (saç) və `.hero-divar .dodaq`
(dodaqlar) qaydalarına baxın. Daha zəif istəyirsinizsə `opacity`
dəyərlərini azaldın.

Profili tamam çıxarmaq istəsəniz, `<div class="hero-divar">` blokunu
silmək kifayətdir — qalan qatlar öz-özünə işləyir.

**Hazırda foto rejimi işləkdir** — fonda salon fotosu
(`sekiller/salon.jpg`) var.

Fotonun orijinalında ANGEL loqosu, halqa, "QADIN GÖZƏLLİK SALONU"
yazısı və şüar vardı. Onları şəkildən sildim (mərkəz sahə ətraf
divarın rəngi ilə dolduruldu), çünki saytın öz ANGEL yazısı və
hərəkətli halqaları ilə ikiqat görünürdü.

İndi hər şeydən bir dənədir: bir ANGEL yazısı (qalın Bodoni), bir
dəst hərəkətli halqa, bir ünvan sətri.

Foto açıq rəngli olduğu üçün üstünə yumşaq işıq pərdəsi qoyulub —
tünd yazılar beləcə oxunur. Pərdəni `.hero-foto::after` qaydasında
tənzimləmək olar.

Dar ekranda foto tam sığmadığı üçün onun loqosuz sağ hissəsi
göstərilir, saytın öz ANGEL yazısı isə geri qayıdır.

**Cizgi rəsmi rejiminə qayıtmaq** üçün iki sözü silin:

```html
<header class="hero foto-rejim" id="ust">
<div class="hero-fon foto-var" id="hero-fon" aria-hidden="true">
```

`foto-rejim` və `foto-var` sözlərini silsəniz, sayt xətlə çəkilmiş
qadın profilinə, 3D mirvari formasına və salon əşyalarına
(asma lampalar, güzgü, rəf, quru çiçək, qayçı-daraq) qayıdır.

Fotonu dəyişmək üçün `sekiller/salon.jpg` faylını yenisi ilə əvəz edin
— kodda heç nə dəyişmir.

⚠️ **Hazırkı şəkil orijinalda kiçik idi (595×472 piksel).** Onu Lanczos
üsulu ilə 1785 piksel-ə böyüdüb kəskinləşdirdim — brauzerin öz
böyütməsindən xeyli aydındır, amma olmayan detalı yaratmaq mümkün deyil.

Tam kəskinlik üçün **ən azı 1920 piksel enində** orijinal foto lazımdır.
Ən yaxşısı salonu özünüz çəkməkdir: telefonla üfüqi, geniş kadr,
gündüz işığında.

Fotonun hansı hissəsinin görünəcəyini `object-position` idarə edir:

```css
.hero-foto img{ object-position:center 42%; }
```

`42%` rəqəmini azaltsanız yuxarısı, artırsanız aşağısı görünür.

**Fotonu tamamilə çıxarmaq** üçün `<header class="hero foto-rejim">`
sətrindən `foto-rejim`, `<div class="hero-fon foto-var">` sətrindən isə
`foto-var` sözünü silin. Onda sayt açıq fona və xətlə çəkilmiş profil
rəsminə qayıdır.

Foto varkən hero avtomatik tündləşir: yazılar ağ olur, düymə açıq
rəngə keçir, naviqasiya işıqlanır. Bunu ayrıca ayarlamaq lazım deyil.

## Söhbət botu

Sağ aşağıdakı "Ustaya yaz" düyməsi söhbəti açır. Bot Aysel adından
danışır, xidmətlər və qiymətlər barədə cavab verir, sonda rezervasiya
məlumatını toplayır.

**Serversiz** (indiki hal) bot saytdakı məlumatdan cavab verir —
qiymətlər, ünvan, iş saatları, xidmət təfərrüatları hamısı işləyir.
Rezervasiya toplanır, amma göndərilmir: bot bunu açıq deyir və telefon
nömrəsini verir.

**Serverlə** bot süni intellektlə sərbəst suallara cavab verir və
rezervasiya birbaşa Telegram-ınıza düşür.

### Serveri qurmaq

Telegram tokenini brauzerə qoymaq olmaz — hər kəs görüb botunuzu ələ
keçirər. Ona görə token serverdə qalır.

**1.** Telegram-da `@BotFather`-ə yazın, `/newbot` ilə bot yaradın,
tokeni götürün. Sonra `@userinfobot`-a yazıb öz chat id-nizi alın.

**2.** Server qovluğunda `.env` faylı yaradın:

```
TELEGRAM_TOKEN=BotFather verdiyi token
TELEGRAM_CHAT_ID=sizin chat id
OPENAI_API_KEY=openai açarınız
```

**3.** Quraşdırın və işə salın:

```bash
pip install fastapi uvicorn httpx openai python-dotenv
uvicorn server:app --host 0.0.0.0 --port 8100
```

**4.** `server.py`-də `allow_origins` siyahısına saytınızın domenini
yazın. Orada olmayan domendən sorğu qəbul edilmir.

**5.** `index.html`-də söhbət bölməsinin başında bu sətri doldurun:

```js
const SERVER = 'https://sizin-domen.com';
```

Boş qalsa bot oflayn rejimdə işləməyə davam edir.

### Botun bildiklərini dəyişmək

`server.py` içindəki `SALON` mətni botun bütün bilik mənbəyidir —
qiymətlər, ustalar, saatlar, qaydalar. Orada dəyişiklik etsəniz, bot
dərhal yeni məlumatla danışır.

`TALIMAT` isə botun necə danışdığını müəyyən edir. Orada yazılıb ki,
bot uydurmasın, tibbi məsləhət verməsin və cavabları qısa saxlasın.

Oflayn cavablar `index.html`-dəki `oflaynCavab` funksiyasındadır —
server olmayanda bot oradan cavab verir.
