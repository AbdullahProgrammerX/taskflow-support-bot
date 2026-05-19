# TaskFlow — Güvenlik ve SSO

## Veri şifreleme

- Aktarım: TLS 1.2+
- Bekleyen veri: AES-256 (AWS KMS)

## İki faktörlü kimlik doğrulama (2FA)

Tüm planlarda TOTP (Google Authenticator, Authy vb.) desteklenir. Workspace yöneticisi Pro ve üzerinde **2FA zorunlu** kılabilir.

## SSO (Single Sign-On)

- **Yalnızca Enterprise** planında kullanılabilir.
- Protokol: **SAML 2.0**
- Sağlayıcı örnekleri: Okta, Azure AD, Google Workspace
- Kurulum: Ayarlar → Güvenlik → SSO; metadata URL veya XML yüklenir.

## Oturum süresi

Varsayılan oturum süresi **7 gün**; Enterprise’da 1 saat ile 30 gün arası yapılandırılabilir.

## Veri silme (GDPR)

Hesap silme talebi **30 gün** içinde kalıcı silme ile tamamlanır; yedeklerden arındırma ek 14 gün sürebilir.
