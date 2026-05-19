# TaskFlow — API

## Kimlik doğrulama

Tüm API istekleri `Authorization: Bearer <API_TOKEN>` başlığı gerektirir. Token oluşturma: **Ayarlar → Geliştirici → API anahtarları**.

## Temel URL

```
https://api.taskflow.io/v1
```

## Rate limit

| Plan | Limit |
|------|--------|
| Free | 100 istek / dakika |
| Pro | 1000 istek / dakika |
| Enterprise | Özel (varsayılan 5000) |

Limit aşılınca HTTP **429** döner; `Retry-After` başlığına bakın.

## Projeler endpoint

`GET /projects` — workspace’teki projeleri listeler. Free planda yalnızca ilk 3 aktif proje API’de görünür.

## Webhook

Pro ve üzeri planlarda `task.created`, `task.completed` olayları için webhook tanımlanabilir. En fazla **10** webhook URL (Pro), Enterprise’da sınırsız.
