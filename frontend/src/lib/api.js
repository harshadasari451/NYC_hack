const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function uploadWhatsApp(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const res = await fetch(`${API_BASE}/api/upload/whatsapp`, {
    method: 'POST',
    body: formData,
  });
  return res.json();
}

export async function uploadPhotos(files) {
  const formData = new FormData();
  for (const file of files) {
    formData.append('files', file);
  }
  
  const res = await fetch(`${API_BASE}/api/upload/photos`, {
    method: 'POST',
    body: formData,
  });
  return res.json();
}

export async function uploadAudioVideo(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const res = await fetch(`${API_BASE}/api/upload/audio-video`, {
    method: 'POST',
    body: formData,
  });
  return res.json();
}

export async function createPersona(personName, description = '') {
  const res = await fetch(`${API_BASE}/api/persona/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ person_name: personName, description }),
  });
  return res.json();
}

export async function sendChatMessage(message, conversationId = null) {
  const res = await fetch(`${API_BASE}/api/chat/send`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, conversation_id: conversationId }),
  });
  return res.json();
}

export async function getChatHistory(conversationId) {
  const res = await fetch(`${API_BASE}/api/chat/history/${conversationId}`);
  return res.json();
}
