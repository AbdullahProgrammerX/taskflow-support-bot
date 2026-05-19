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
| 3 | Tamam | RAG pipeline || 4 | Bekliyor | API sertleştirme |

Detay: `docs/reports/phase-01-foundation.md` … `phase-03-rag-pipeline.md`
