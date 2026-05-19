# Faz 4: API Kalitesi ve Güvenlik

**Tarih:** 2026-05-19  
**Durum:** Tamamlandı

---

## Bu fazda ne öğrendik?

### Rate limiting

- **Amaç:** `/chat` endpoint’ini kötüye kullanımdan ve API maliyet patlamasından korumak.
- **Yöntem:** Bellek içi sabit pencere — IP başına `RATE_LIMIT_REQUESTS` / `RATE_LIMIT_WINDOW_SECONDS`.
- **Yanıt:** HTTP `429` + `Retry-After` başlığı.

Üretimde Redis tabanlı limiter tercih edilir; öğrenme ve demo için in-memory yeterli.

### Admin endpoint

- `POST /admin/reindex` — bilgi tabanını yeniden indexler (`scripts/ingest.py` ile aynı iş).
- `GET /admin/index-stats` — Chroma chunk sayısı.
- Koruma: `X-Admin-Key` header = `.env` içindeki `ADMIN_API_KEY`.
- Karşılaştırma: `secrets.compare_digest` (timing attack azaltma).

### Hata yönetimi

- `422` — Pydantic doğrulama hataları yapılandırılmış JSON.
- `401` — yanlış admin key.
- `503` — OpenAI veya admin key sunucuda yok.

---

## Yeni dosyalar

| Dosya | Rol |
|-------|-----|
| `src/middleware/rate_limit.py` | IP rate limit |
| `src/api/deps.py` | Admin key doğrulama |
| `src/api/routes_admin.py` | `/admin/*` |

---

## Kullanım

### `.env` ekle

```env
ADMIN_API_KEY=uzun-rastgele-bir-deger-uret
```

### Reindex (PowerShell)

```powershell
$headers = @{ "X-Admin-Key" = "senin-admin-key" }
Invoke-RestMethod -Uri http://127.0.0.1:8000/admin/reindex `
  -Method Post -Headers $headers `
  -ContentType "application/json" `
  -Body '{"reset": true}'
```

### Index stats

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/admin/index-stats -Headers $headers
```

---

## `/health` yeni alanlar

- `phase: 4`
- `admin_configured`
- `rate_limit: { requests, window_seconds }`

---

## Sonraki faz (Faz 5)

- Basit web UI (`static/index.html`)
- CORS

---

## Senin notların

```
(buraya yaz)
```
