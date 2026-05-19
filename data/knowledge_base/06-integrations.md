# TaskFlow — Entegrasyonlar

## Slack

Pro ve üzeri: kanala görev bildirimi ve `/taskflow create` komutu. Kurulum: Entegrasyonlar → Slack → OAuth ile bağlan.

## GitHub

Pro ve üzeri: commit ve PR’ları görevlere bağlama. Free planda yalnızca **salt okunur** bağlantı (webhook alınmaz).

## Zapier

Tüm planlarda mevcut; Free’de ayda **100** Zap çalıştırma limiti, Pro’da **2000**.

## Dışa aktarma

- **CSV:** görev listesi (tüm planlar)
- **JSON tam yedek:** Pro ve üzeri, ayda 1 otomatik yedek
- Enterprise: S3 bucket’a günlük yedek

## Desteklenmeyen

TaskFlow şu an **Jira Server Data Center** ile doğrudan iki yönlü senkron sunmaz; yalnızca Jira Cloud import aracı (tek seferlik) vardır.
