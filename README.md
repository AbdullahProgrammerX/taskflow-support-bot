# TaskFlow Support Bot (RAG)

[![GitHub](https://img.shields.io/badge/GitHub-taskflow--support--bot-181717?logo=github)](https://github.com/AbdullahProgrammerX/taskflow-support-bot)

Kurgusal **TaskFlow** SaaS dokümantasyonu üzerinde çalışan **RAG destek botu**.  
FastAPI · OpenAI · Chroma · kaynak gösterimli cevaplar · responsive web UI.

> **TaskFlow** bu repoda **örnek müşteri markasıdır**. Aynı motor; kendi `data/knowledge_base/` ve UI markanızla herhangi bir ürüne uyarlanabilir.

## Özellikler

- RAG pipeline (retrieval + grounded generation)
- Markdown bilgi tabanı + Chroma vektör index
- REST API (`/chat`, `/health`, `/admin/*`)
- Profesyonel web arayüzü (`/`)
- Rate limiting, admin reindex
- Eval seti (25 soru, otomatik skor)

## Eval sonuçları (örnek)

| Metrik | Skor |
|--------|------|
| Pass rate | **96%** (24/25) |
| Retrieval | **100%** |
| Refusal (out-of-scope) | **100%** |

```powershell
python eval/run_eval.py
```

## Hızlı başlangıç (yerel)

```powershell
git clone https://github.com/AbdullahProgrammerX/taskflow-support-bot.git
cd taskflow-support-bot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

`.env` içine `OPENAI_API_KEY` ve `ADMIN_API_KEY` gir.

```powershell
python scripts/ingest.py --reset
uvicorn src.main:app --reload
```

- **UI:** http://127.0.0.1:8000/
- **Health:** http://127.0.0.1:8000/health
- **API docs:** http://127.0.0.1:8000/docs

## Docker

```powershell
copy .env.example .env
# .env doldur
docker compose up --build
```

İlk çalıştırmada `ensure_index` boş index’i doldurur. Manuel yenileme:

```powershell
docker compose --profile setup run --rm ingest
```

## Deploy (Railway / Render)

1. Repo’yu bağla.
2. Env vars: `OPENAI_API_KEY`, `ADMIN_API_KEY`, isteğe bağlı rate limit değişkenleri.
3. Start: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
4. Persistent volume → `/app/chroma_data` (mümkünse).
5. İlk deploy: `python scripts/ingest.py --reset`

## Proje yapısı

```
src/           # FastAPI, RAG, ingestion
static/        # Web UI
data/          # Knowledge base (MD)
eval/          # Eval questions + runner
scripts/       # ingest, docker entrypoint
docs/reports/  # Faz öğrenme raporları
```

## Fazlar

| Faz | Durum |
|-----|--------|
| 1–3 | API + ingest + RAG |
| 4 | Rate limit + admin |
| 5 | Web UI |
| 6 | Eval |
| 7 | Docker + deploy |

Detay: [`docs/reports/`](docs/reports/)

## Lisans

MIT (veya ihtiyacına göre ekle)

## Gelecek vizyon

No-code KB yükleme, çok kiracılı (multi-tenant) deploy, embed widget — bu repo çekirdek motor.
