import { CONFIG, STRINGS } from "./config.js";
import { ApiError, fetchHealth, sendChatMessage } from "./api.js";
import { dedupeSources, formatMarkdown } from "./format.js";

const t = STRINGS[CONFIG.ui.locale];

const els = {
  statusBadge: document.getElementById("status-badge"),
  messages: document.getElementById("messages"),
  emptyState: document.getElementById("empty-state"),
  suggestions: document.getElementById("suggestions"),
  form: document.getElementById("chat-form"),
  input: document.getElementById("message-input"),
  sendBtn: document.getElementById("send-btn"),
  charCount: document.getElementById("char-count"),
  sourcesPanel: document.getElementById("sources-panel"),
  sourcesList: document.getElementById("sources-list"),
  sourcesEmpty: document.getElementById("sources-empty"),
  toast: document.getElementById("toast"),
};

let isBusy = false;

function showToast(message, type = "error") {
  els.toast.textContent = message;
  els.toast.className = `toast toast--visible toast--${type}`;
  clearTimeout(showToast._timer);
  showToast._timer = setTimeout(() => els.toast.classList.remove("toast--visible"), 5000);
}

function setBusy(busy) {
  isBusy = busy;
  els.sendBtn.disabled = busy;
  els.input.disabled = busy;
  els.sendBtn.setAttribute("aria-busy", String(busy));
  els.sendBtn.querySelector(".btn__label").textContent = busy ? t.sending : t.send;
}

function hideEmptyState() {
  els.emptyState.hidden = true;
}

function scrollToBottom() {
  requestAnimationFrame(() => {
    els.messages.scrollTop = els.messages.scrollHeight;
  });
}

function appendMessage(role, contentHtml, meta = {}) {
  hideEmptyState();

  const article = document.createElement("article");
  article.className = `message message--${role}`;

  const avatar = document.createElement("div");
  avatar.className = "message__avatar";
  avatar.setAttribute("aria-hidden", "true");
  avatar.textContent = role === "user" ? "S" : "T";

  const bubble = document.createElement("div");
  bubble.className = "message__bubble";
  bubble.innerHTML = contentHtml;

  if (meta.model) {
    const foot = document.createElement("footer");
    foot.className = "message__meta";
    foot.textContent = meta.model + (meta.rag ? " · RAG" : "");
    bubble.appendChild(foot);
  }

  const wrap = document.createElement("div");
  wrap.className = "message__content";
  wrap.append(avatar, bubble);
  article.appendChild(wrap);

  els.messages.appendChild(article);
  scrollToBottom();
  return article;
}

function appendTyping() {
  const el = appendMessage("assistant", '<div class="typing"><span></span><span></span><span></span></div>');
  el.classList.add("message--typing");
  return el;
}

function renderSources(sources) {
  const unique = dedupeSources(sources);
  els.sourcesList.innerHTML = "";

  if (!unique.length) {
    els.sourcesEmpty.hidden = false;
    return;
  }

  els.sourcesEmpty.hidden = true;
  for (const src of unique) {
    const card = document.createElement("div");
    card.className = "source-card";
    card.innerHTML = `
      <h3 class="source-card__title">${escapeHtml(src.file)}</h3>
      <p class="source-card__excerpt">${escapeHtml(src.excerpt)}</p>
    `;
    els.sourcesList.appendChild(card);
  }
}

function escapeHtml(text) {
  const d = document.createElement("div");
  d.textContent = text;
  return d.innerHTML;
}

function updateCharCount() {
  const len = els.input.value.length;
  els.charCount.textContent = `${len} / ${CONFIG.limits.messageMaxLength}`;
  els.charCount.classList.toggle("char-count--warn", len > CONFIG.limits.messageMaxLength * 0.9);
}

async function loadHealth() {
  try {
    const health = await fetchHealth();
    const ragOn = health.rag_enabled;
    els.statusBadge.textContent = ragOn ? t.ragActive : t.ragInactive;
    els.statusBadge.className = `badge ${ragOn ? "badge--success" : "badge--warn"}`;
  } catch {
    els.statusBadge.textContent = "Offline";
    els.statusBadge.className = "badge badge--error";
  }
}

async function submitMessage(text) {
  const message = text.trim();
  if (!message || isBusy) return;
  if (message.length > CONFIG.limits.messageMaxLength) {
    showToast(`Mesaj en fazla ${CONFIG.limits.messageMaxLength} karakter olabilir.`);
    return;
  }

  appendMessage("user", `<p>${escapeHtml(message)}</p>`);
  els.input.value = "";
  updateCharCount();

  setBusy(true);
  const typingEl = appendTyping();

  try {
    const data = await sendChatMessage(message);
    typingEl.remove();
    appendMessage("assistant", formatMarkdown(data.answer), {
      model: data.model,
      rag: data.rag_enabled,
    });
    renderSources(data.sources);
    els.sourcesPanel.hidden = false;
  } catch (err) {
    typingEl.remove();
    let msg = t.errorGeneric;
    if (err instanceof ApiError) {
      if (err.status === 429) {
        msg = err.retryAfter
          ? `${t.errorRateLimit} (${err.retryAfter}s)`
          : t.errorRateLimit;
      } else if (err.status === 0) msg = t.errorNetwork;
      else msg = err.message;
    }
    showToast(msg);
    appendMessage("assistant", `<p class="message__error">${escapeHtml(msg)}</p>`);
  } finally {
    setBusy(false);
    els.input.focus();
  }
}

function initSuggestions() {
  els.suggestions.innerHTML = "";
  for (const q of t.suggested) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "chip";
    btn.textContent = q;
    btn.addEventListener("click", () => submitMessage(q));
    els.suggestions.appendChild(btn);
  }
}

function bindEvents() {
  els.form.addEventListener("submit", (e) => {
    e.preventDefault();
    submitMessage(els.input.value);
  });

  els.input.addEventListener("input", () => {
    updateCharCount();
    els.input.style.height = "auto";
    els.input.style.height = `${Math.min(els.input.scrollHeight, 160)}px`;
  });
  els.input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submitMessage(els.input.value);
    }
  });
}

async function init() {
  document.documentElement.lang = CONFIG.ui.locale;
  initSuggestions();
  bindEvents();
  updateCharCount();
  await loadHealth();
  els.input.focus();
}

init();
