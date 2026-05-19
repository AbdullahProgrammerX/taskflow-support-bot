# Faz 5: Profesyonel Web Arayüzü

**Tarih:** 2026-05-19  
**Durum:** Tamamlandı

---

## Bu fazda ne yaptık?

Tek sayfalık, **frameworksüz** (vanilla JS modüller) modern destek arayüzü:

- Responsive layout (mobil → masaüstü; kaynak paneli yan sütun)
- `prefers-color-scheme` ile otomatik açık/koyu tema
- Erişilebilirlik: skip link, ARIA live regions, klavye (Enter gönder)
- Modüler JS: `config`, `api`, `format`, `app` — ileride React/Vite’e taşınabilir
- Hata durumları: 429 rate limit, ağ, toast bildirimleri
- Kaynak kartları, örnek soru chip’leri, yazıyor animasyonu

---

## Dosya yapısı

```
static/
  index.html
  favicon.svg
  css/app.css      # design tokens, responsive grid
  js/
    config.js      # API yolları, i18n metinleri
    api.js         # fetch + ApiError
    format.js      # markdown subset, source dedupe
    app.js         # UI mantığı
```

`GET /` → `index.html`  
`/static/*` → statik dosyalar

---

## Geleceğe hazırlık

| Konu | Nasıl |
|------|--------|
| Yeni dil | `STRINGS.en` ekle, `CONFIG.ui.locale` |
| Farklı API URL | `config.js` veya build-time env |
| WebSocket streaming | `api.js` içine `streamChat()` |
| Tema | CSS variables zaten merkezi |

---

## Çalıştırma

```powershell
uvicorn src.main:app --reload
```

Tarayıcı: http://127.0.0.1:8000/

---

## Senin notların

```
(buraya yaz)
```
