# Deploy: Railway (Render alternatifi)

## Neden Railway?

- GitHub ile tek tık deploy
- Dockerfile otomatik
- Ücretsiz deneme kredisi ($5/ay civarı — kart gerekebilir)
- `PORT` otomatik — projemiz hazır

---

## Adım 1 — Hesap

1. https://railway.com
2. **Login with GitHub**
3. E-posta doğrulama (istersen)

---

## Adım 2 — Proje oluştur

1. **New Project**
2. **Deploy from GitHub repo**
3. `AbdullahProgrammerX/taskflow-support-bot` seç
4. **Deploy Now**

Railway `Dockerfile` ile build eder.

---

## Adım 3 — Environment variables

Projeye tıkla → servis kartı → **Variables** → **RAW Editor** veya tek tek ekle:

```env
OPENAI_API_KEY=sk-...
ADMIN_API_KEY=uzun-rastgele-secret
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW_SECONDS=60
```

**Add** / kaydet → otomatik **redeploy** başlar.

---

## Adım 4 — Public URL

1. Servis → **Settings**
2. **Networking** → **Generate Domain**
3. URL örneği: `https://taskflow-support-bot-production.up.railway.app`

---

## Adım 5 — Log kontrol

**Deployments** → son deploy → **View Logs**

Beklenen:

```
Index empty — running ingest…
Ingest done: 10 chunks
Uvicorn running on http://0.0.0.0:XXXX
```

---

## Adım 6 — Test

| Test | URL |
|------|-----|
| Health | `https://SENIN-DOMAIN/health` |
| UI | `https://SENIN-DOMAIN/` |

`rag_enabled: true` ve `chunk_count: 10` olmalı.

---

## Index yenileme

Railway → servis → **Shell** (veya local):

```bash
python scripts/ingest.py --reset
```

---

## Maliyet

- Küçük demo: genelde kredi içinde kalır
- Dashboard → **Usage** takip et
- Uyarı limiti koy

---

## Sorun giderme

| Sorun | Çözüm |
|-------|--------|
| Build fail | Logs; `requirements.txt` / Docker |
| 502 | Redeploy; env vars eksik mi |
| rag false | Shell’de ingest |
| OpenAI 401 | Key yanlış / süresi dolmuş |
