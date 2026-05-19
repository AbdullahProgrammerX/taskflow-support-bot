/** App configuration — extend here for env-specific builds later. */
export const CONFIG = {
  api: {
    chat: "/chat",
    health: "/health",
  },
  limits: {
    messageMaxLength: 4000,
  },
  ui: {
    locale: "tr",
  },
};

export const STRINGS = {
  tr: {
    appName: "TaskFlow Support",
    appTagline: "Dokümantasyon destekli yapay zeka asistanı",
    placeholder: "TaskFlow hakkında bir soru yazın…",
    send: "Gönder",
    sending: "Yanıt hazırlanıyor…",
    emptyTitle: "Size nasıl yardımcı olabilirim?",
    emptyHint: "Planlar, faturalandırma, API veya güvenlik hakkında sorabilirsiniz.",
    sourcesTitle: "Kaynaklar",
    sourcesEmpty: "Bu yanıt için kaynak gösterilmedi.",
    ragActive: "RAG aktif",
    ragInactive: "RAG kapalı",
    errorGeneric: "Bir hata oluştu. Lütfen tekrar deneyin.",
    errorRateLimit: "Çok fazla istek. Bir süre sonra tekrar deneyin.",
    errorNetwork: "Sunucuya ulaşılamıyor. Bağlantınızı kontrol edin.",
    poweredBy: "TaskFlow bilgi tabanı · OpenAI",
    suggested: [
      "Ücretsiz planda kaç proje açabilirim?",
      "Pro plan ne kadar?",
      "SSO hangi planda var?",
      "API rate limit nedir?",
    ],
  },
};
