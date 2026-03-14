export async function loadData(caseId) {
  if (!caseId) return null;
  const res = await fetch(`/cases/${encodeURIComponent(caseId)}`);
  if (!res.ok) throw new Error('Fetch failed');
  return await res.json();
}

export async function pushAndWait(caseId, messages) {
  if (!caseId) throw new Error('pushAndWait requires a caseId');

  // Відправка повідомлень та очікування оновленого стану
  const response = await fetch(`/cases/${encodeURIComponent(caseId)}/active`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages })
  });

  if (!response.ok) {
    throw new Error('Failed to update case');
  }

  // Повертаємо актуальний стан з бекенду (повідомлення + саджести)
  return await response.json();
}