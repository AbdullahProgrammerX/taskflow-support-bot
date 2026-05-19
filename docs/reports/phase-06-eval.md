# Faz 6: Değerlendirme (Eval)

**Tarih:** 2026-05-19  
**Durum:** Tamamlandı

---

## Bu fazda ne öğrendik?

“Çalışıyor” ile “doğru” aynı değil. **Eval** = sabit soru seti + otomatik skor + rapor.

### Metrikler

| Metrik | Ne ölçer? |
|--------|-----------|
| **Retrieval hit** | Beklenen MD dosyası top-k veya cevap kaynaklarında var mı? |
| **Keyword hit** | Cevapta beklenen sayı/kelime var mı? (ör. "3", "12 USD") |
| **Refusal (trap)** | Dokümanda olmayan soruda uydurmadan “bilmiyorum” diyor mu? |

### Soru seti

- `eval/questions.jsonl` — **25 soru**
  - 20 factual (TaskFlow dokümanında cevabı var)
  - 5 trap (Bitcoin, CEO, Notion vb. — cevap vermemeli)

---

## Çalıştırma

```powershell
.\.venv\Scripts\Activate.ps1
python eval/run_eval.py
python eval/run_eval.py --limit 5   # hızlı test
```

Çıktılar:

- `eval/results/latest.json`
- `eval/results/latest.md`

**Maliyet:** 25 soru ≈ 25× (retrieval + chat) — birkaç cent–dolar arası.

---

## Hedefler (ilk iterasyon)

| Metrik | Hedef |
|--------|--------|
| Retrieval | ≥ 70% |
| Keywords | ≥ 70% |
| Refusal | ≥ 80% |
| Genel pass | ≥ 65% |

Skor düşükse: `rag_top_k`, chunk boyutu, prompt iyileştir.

---

## Gelecek ürün vizyonu ile bağlantı

İleride teknik bilgisi olmayan kullanıcılar için:

- Bu eval pipeline → müşteri KB güncelleyince **otomatik regresyon testi**
- “Satın alan entegrasyon” → önce **tek tenant deploy**, sonra no-code upload + eval dashboard

Şu an: geliştirici eliyle `questions.jsonl` düzenler.

---

## Senin notların

```
(buraya yaz — ilk eval skorlarını yapıştır)
```
