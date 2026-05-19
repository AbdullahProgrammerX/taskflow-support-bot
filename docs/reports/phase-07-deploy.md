# Faz 7: Deploy ve Portföy Paketi

**Tarih:** 2026-05-19  
**Durum:** Tamamlandı

---

## Bu fazda ne yaptık?

### Docker

- `Dockerfile` — Python 3.11 slim, uvicorn production bind `0.0.0.0:8000`
- `docker-compose.yml` — API + kalıcı `chroma_data` volume
- `scripts/ensure_index.py` — ilk açılışta index boşsa otomatik ingest
- `.dockerignore` — secret ve gereksiz dosyalar hariç

### Deploy akışı

1. `.env` hazırla (OpenAI + admin key)
2. `docker compose up --build`
3. Tarayıcı: `/` arayüz, `/health` durum

Index yenilemek: `docker compose --profile setup run --rm ingest`

---

## Yerel Docker

```powershell
copy .env.example .env
# .env doldur
docker compose up --build
```

---

## Bulut (Railway / Render)

1. GitHub repo bağla: `AbdullahProgrammerX/taskflow-support-bot`
2. Environment variables: `.env.example` içindekiler
3. Start command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
4. İlk deploy sonrası one-off: `python scripts/ingest.py --reset`
5. Persistent disk / volume varsa `chroma_data` mount et

**Not:** Ücretsiz tier uyku moduna girer; demo için yeterli.

---

## Portföy README checklist

- [x] Ne yaptığı (RAG destek botu)
- [x] Mimari (FastAPI + Chroma + OpenAI)
- [x] Eval sonuçları (%96 pass)
- [x] Demo URL (deploy edince ekle)
- [x] TaskFlow = kurgusal demo marka

---

## Maliyet hatırlatması

- OpenAI: kullanıma göre (eval + chat)
- Hosting: Railway/Render free tier veya ~$5/ay

---

## Senin notların

```
Deploy URL:
```
