import { CONFIG } from "./config.js";

export class ApiError extends Error {
  constructor(message, { status = 0, retryAfter = null } = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.retryAfter = retryAfter;
  }
}

async function parseError(response) {
  let detail = response.statusText;
  try {
    const body = await response.json();
    if (typeof body.detail === "string") detail = body.detail;
    else if (Array.isArray(body.detail)) detail = body.detail.map((d) => d.msg).join(", ");
  } catch {
    /* ignore */
  }
  return detail;
}

export async function fetchHealth() {
  const response = await fetch(CONFIG.api.health);
  if (!response.ok) throw new ApiError(await parseError(response), { status: response.status });
  return response.json();
}

export async function sendChatMessage(message) {
  const response = await fetch(CONFIG.api.chat, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    const retryAfter = response.headers.get("Retry-After");
    throw new ApiError(await parseError(response), {
      status: response.status,
      retryAfter: retryAfter ? Number(retryAfter) : null,
    });
  }

  return response.json();
}
