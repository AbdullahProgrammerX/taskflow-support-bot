# Deploy rehberi (Render)

## Ön koşullar

- [ ] GitHub repo güncel: https://github.com/AbdullahProgrammerX/taskflow-support-bot
- [ ] OpenAI API key hazır
- [ ] Admin key hazır (uzun rastgele string)

---

## Adım 1 — Render hesabı

1. https://render.com → **Get Started**
2. **Sign in with GitHub**
3. GitHub erişimine izin ver

---

## Adım 2 — Yeni Web Service

1. Dashboard → **New +** → **Web Service**
2. **Connect** `AbdullahProgrammerX/taskflow-support-bot`
3. Ayarlar:

| Alan | Değer |
|------|--------|
| Name | `taskflow-support-bot` |
| Region | Frankfurt (veya yakın) |
| Branch | `main` |
| Runtime | **Docker** |
| Instance type | **Free** |

Render `Dockerfile` dosyasını otomatik bulur.

---

## Adım 3 — Environment Variables

**Environment** sekmesinde ekle:

| Key | Value |
|-----|--------|
| `OPENAI_API_KEY` | (OpenAI key — gizli) |
| `ADMIN_API_KEY` | (uzun rastgele secret) |
| `OPENAI_CHAT_MODEL` | `gpt-4o-mini` |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` |

İsteğe bağlı: `RATE_LIMIT_REQUESTS=30`, `RATE_LIMIT_WINDOW_SECONDS=60`

---

## Adım 4 — Deploy

1. **Create Web Service**
2. Build 5–10 dk sürebilir (ilk sefer)
3. Logda görmen gerekenler:
   - `Index empty — running ingest…` veya `Index OK: 10 chunks`
   - `Application startup complete`

---

## Adım 5 — Test

URL: `https://taskflow-support-bot-xxxx.onrender.com`

| Test | URL |
|------|-----|
| UI | `/` |
| Health | `/health` → `rag_enabled: true`, `chunk_count: 10` |
| Chat | Arayüzden soru sor |

**Not:** Free planda ~15 dk kullanılmazsa uyku modu; ilk istek 30–60 sn sürebilir.

---

## Sorun giderme

### `rag_enabled: false` / chunk 0

Render **Shell** (Dashboard → Service → Shell):

```bash
python scripts/ingest.py --reset
```

### Build hatası

Logs → Python/Chroma build; tekrar **Manual Deploy**.

### 502 / timeout

Free tier cold start; bir kez daha dene.

---

## Deploy sonrası

- README’ye **Live demo:** URL ekle
- LinkedIn / CV’de link ver
- OpenAI usage limit / billing alert açık olsun
