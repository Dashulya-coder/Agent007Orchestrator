export function createStructure(clientName){
  const root = document.getElementById('app');
  root.innerHTML = '';

  const topbar = document.createElement('div');
  topbar.className = 'topbar';
  const title = document.createElement('h1');
  title.textContent = 'Support Worker — Chat Dashboard (Mock)';
  topbar.appendChild(title);

  const mainGrid = document.createElement('div');
  mainGrid.className = 'main-grid';

  // Chat column
  const chatColumn = document.createElement('div');
  chatColumn.className = 'chat-column';

  const chatHeader = document.createElement('div');
  chatHeader.className = 'chat-header';
  chatHeader.innerHTML = `Conversation with: <strong>${clientName}</strong>`;

  const chat = document.createElement('div');
  chat.id = 'chat';
  chat.className = 'chat';

  const suggestionsPanel = document.createElement('div');
  suggestionsPanel.className = 'suggestions-panel';
  const spTitle = document.createElement('h3');
  spTitle.textContent = 'AI Suggested Responses';
  const suggestions = document.createElement('div');
  suggestions.id = 'suggestions';
  suggestions.className = 'suggestions';
  suggestionsPanel.appendChild(spTitle);
  suggestionsPanel.appendChild(suggestions);

  const inputRow = document.createElement('div');
  inputRow.className = 'input-row';
  const messageInput = document.createElement('input');
  messageInput.id = 'messageInput';
  messageInput.placeholder = 'Type a message or click a suggestion';
  const sendBtn = document.createElement('button');
  sendBtn.id = 'sendBtn';
  sendBtn.textContent = 'Send';
  inputRow.appendChild(messageInput);
  inputRow.appendChild(sendBtn);

  chatColumn.appendChild(chatHeader);
  chatColumn.appendChild(chat);
  chatColumn.appendChild(suggestionsPanel);
  chatColumn.appendChild(inputRow);

  // Sidebar
  const sidebar = document.createElement('div');
  sidebar.className = 'sidebar';

  const summaryCard = document.createElement('div');
  summaryCard.className = 'summary-card';
  const sumTitle = document.createElement('h3'); sumTitle.textContent = 'AI Quick Summary';
  const summary = document.createElement('div'); summary.id = 'summary'; summary.className='summary';
  summaryCard.appendChild(sumTitle); summaryCard.appendChild(summary);

  const infoCard = document.createElement('div');
  infoCard.className = 'info-card';
  const infoTitle = document.createElement('h3'); infoTitle.textContent = 'Client Info';
  const clientInfo = document.createElement('div'); clientInfo.id = 'clientInfo'; clientInfo.className='client-info';
  infoCard.appendChild(infoTitle); infoCard.appendChild(clientInfo);

  sidebar.appendChild(summaryCard);
  sidebar.appendChild(infoCard);

  mainGrid.appendChild(chatColumn);
  mainGrid.appendChild(sidebar);

  root.appendChild(topbar);
  root.appendChild(mainGrid);
}

export function renderMessages(messages){
  const container = document.getElementById('chat');
  if(!container) return;
  container.innerHTML = '';
  messages.forEach(m => {
    const div = document.createElement('div');
    div.className = 'bubble ' + m.role;
    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.textContent = `${m.name} • ${m.role}`;
    const text = document.createElement('div');
    text.textContent = m.text;
    div.appendChild(meta);
    div.appendChild(text);
    container.appendChild(div);
  });
  // Keep scroll inside chat box
  container.scrollTop = container.scrollHeight;
}

export function renderSuggestions(suggestions){
  const s = document.getElementById('suggestions');
  if(!s) return;
  s.innerHTML = '';
  suggestions.forEach((t)=>{
    const btn = document.createElement('button');
    btn.className = 'suggestion';
    btn.textContent = t;
    btn.addEventListener('click', ()=>{ const inp = document.getElementById('messageInput'); if(inp) inp.value = t; });
    s.appendChild(btn);
  });
}

export function renderSummary(summary){
  const el = document.getElementById('summary');
  if(!el) return;
  el.innerHTML = '';
  const p = document.createElement('p');
  p.textContent = summary.summaryText || '';
  const meta = document.createElement('p');
  meta.innerHTML = `<strong>Priority:</strong> ${summary.priority || ''} — <strong>Tags:</strong> ${(summary.tags||[]).join(', ')}`;
  el.appendChild(p);
  el.appendChild(meta);
}

export function renderClientInfo(clientInfo){
  const area = document.getElementById('clientInfo');
  if(!area) return;
  area.innerHTML = '';
  const d = clientInfo || {};
  area.innerHTML = `<div><strong>${d.name||''}</strong></div><div>ID: ${d.clientId||''}</div><div>Last payment: ${d.lastPayment||''}</div><div>Dues: ${d.dues||''}</div>`;
}

export function renderAll(state){
  renderMessages(state.messages || []);
  renderSuggestions(state.suggestions || []);
  renderSummary(state.summary || {});
  renderClientInfo(state.clientInfo || {});
}
