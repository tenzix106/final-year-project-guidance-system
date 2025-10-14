const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

function getAuthHeaders() {
  const token = localStorage.getItem('auth_token');
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return headers;
}

export async function register(email, password) {
  const resp = await fetch(`${API_BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!resp.ok) {
    const err = await safeJson(resp);
    throw new Error(err?.message || 'Registration failed');
  }
  return resp.json();
}

export async function login(email, password) {
  const resp = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!resp.ok) {
    const err = await safeJson(resp);
    throw new Error(err?.message || 'Login failed');
  }
  const data = await resp.json();
  if (data?.access_token) {
    localStorage.setItem('auth_token', data.access_token);
  }
  return data;
}

export async function me() {
  const resp = await fetch(`${API_BASE_URL}/api/auth/me`, {
    method: 'GET',
    headers: getAuthHeaders()
  });
  if (!resp.ok) {
    const err = await safeJson(resp);
    throw new Error(err?.message || 'Failed to fetch user');
  }
  return resp.json();
}

export function logout() {
  localStorage.removeItem('auth_token');
}

async function safeJson(resp) {
  try { return await resp.json(); } catch { return null; }
}


