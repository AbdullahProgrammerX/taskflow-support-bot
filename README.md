# TaskFlow Support Bot (RAG)

Kurgusal **TaskFlow** SaaS dokümantasyonu üzerinde çalışan RAG destek botu. FastAPI + OpenAI + Chroma.

**Özellikler:** kaynak gösterimli cevaplar, markdown bilgi tabanı, faz faz öğrenme raporları (`docs/reports/`).

| Faz | Özellik |
|-----|---------|
| 1 | FastAPI + OpenAI chat |
| 2 | Chunking, embedding, Chroma ingest |
| 3 | RAG retrieval + grounded answers |

> **Güvenlik:** `.env` ve API anahtarları repoya girmez. Clone sonrası `ingest` ile vektör indexini yerelde oluşturursun (`chroma_data/` gitignore'da).
## Gereksinimler

- Python 3.11+
- OpenAI API key

## Kurulum

```powershell
git clone https://github.com/AbdullahProgrammerX/taskflow-support-bot.git
cd taskflow-support-bot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```
`.env` dosyasını açıp `OPENAI_API_KEY` değerini gir.

## Çalıştırma

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```

- **Arayüz:** http://127.0.0.1:8000/
- Sağlık: http://127.0.0.1:8000/health
- Swagger UI: http://127.0.0.1:8000/docs
- Sohbet: `POST http://127.0.0.1:8000/chat` — RAG açıkken `sources` döner

## Bilgi tabanını indexleme (Faz 2)

```powershell
pip install -r requirements.txt
python scripts/ingest.py --reset
```

`/health` içinde `index.chunk_count` artmalı.

## Proje yapısı

```
src/
  main.py              # FastAPI uygulaması
  config.py            # .env ayarları
  llm/openai_client.py # OpenAI chat çağrısı
  api/routes_chat.py   # /chat endpoint
  ingestion/           # loader, chunker, indexer
data/knowledge_base/   # TaskFlow MD dosyaları
scripts/ingest.py      # index CLI
docs/reports/          # Faz raporları
```

## Fazlar

| Faz | Durum | Açıklama |
|-----|--------|----------|
| 1 | Tamam | FastAPI + düz LLM chat |
| 2 | Tamam | Doküman ingest + Chroma |
| 3 | Tamam | RAG pipeline |
| 4 | Tamam | Rate limit + admin reindex |
| 5 | Tamam | Profesyonel web UI |
| 6 | Tamam | Eval pipeline |
| 7 | Bekliyor | Deploy |

Detay: `docs/reports/phase-01-foundation.md` … `phase-05-ui.md`

## Admin (Faz 4)

`.env` içine `ADMIN_API_KEY` ekle. İsteklerde header: `X-Admin-Key: <değer>`.

```powershell
$h = @{ "X-Admin-Key" = "your-admin-key" }
Invoke-RestMethod -Uri http://127.0.0.1:8000/admin/reindex -Method Post -Headers $h `
  -ContentType "application/json" -Body '{"reset": true}'
```

Varsayılan rate limit: **30** istek / **60** saniye / IP (`POST /chat`).

## Eval (Faz 6)

```powershell
python eval/run_eval.py
```

Rapor: `eval/results/latest.md` (gitignore — yerelde üretilir).
