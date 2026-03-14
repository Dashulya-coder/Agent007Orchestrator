// Mock frontend behavior for Support Worker chat dashboard

const mock = {
  messages: [
    {role:'client', name:'Jane Doe', text:'Hi — my payment didn\'t go through and I need help.'},
    {role:'agent', name:'Agent Sam', text:'I can help with that — can you confirm your last 4 digits of card?' },
    {role:'client', name:'Jane Doe', text:'It\'s 1234. Also I need assistance scheduling a visit.'},
    {role:'worker', name:'Worker Lee', text:'I can take the visit on Friday afternoon.'}
  ],
  suggestions: [
    'I can look into the payment status and follow up shortly.',
    'Thanks — I\'ve escalated this to billing.',
    'Would Friday 2–4pm work for the visit?',
    'I will schedule and confirm back with you.'
  ],
  summary: {
    summaryText: 'Client reports payment failure and requests scheduling help. Prefers afternoon visits.',
    priority: 'Medium',
    tags: ['payment','scheduling']
  },
  clientInfo: {
    name: 'Jane Doe',
    clientId: 'C-00124',
    lastPayment: 'Failed on 2026-03-10',
    dues: '$0.00 (attempted payment failed)'
  }
}

function el(id){return document.getElementById(id)}

function createStructure(){
  const root = el('app');

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
  chatHeader.innerHTML = `Conversation with: <strong>${mock.clientInfo.name}</strong>`;

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
  const senderSelect = document.createElement('select');
  senderSelect.id = 'senderSelect';
  senderSelect.className = 'sender-select';
  const optAgent = document.createElement('option'); optAgent.value='agent'; optAgent.textContent='Agent';
  const optWorker = document.createElement('option'); optWorker.value='worker'; optWorker.textContent='Worker';
  senderSelect.appendChild(optAgent); senderSelect.appendChild(optWorker);
  const messageInput = document.createElement('input');
  messageInput.id = 'messageInput';
  messageInput.placeholder = 'Type a message or click a suggestion';
  const sendBtn = document.createElement('button');
  sendBtn.id = 'sendBtn';
  sendBtn.textContent = 'Send';
  inputRow.appendChild(senderSelect);
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

function renderMessages(){
  const container = el('chat');
  container.innerHTML = '';
  mock.messages.forEach(m => {
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
  container.scrollTop = container.scrollHeight;
}

function renderSuggestions(){
  const s = el('suggestions');
  s.innerHTML = '';
  mock.suggestions.forEach((t, i) => {
    const btn = document.createElement('button');
    btn.className = 'suggestion';
    btn.textContent = t;
    btn.onclick = () => { el('messageInput').value = t; }
    s.appendChild(btn);
  });
}

function renderSummary(){
  el('summary').innerHTML = '';
  const p = document.createElement('p');
  p.textContent = mock.summary.summaryText;
  const meta = document.createElement('p');
  meta.innerHTML = `<strong>Priority:</strong> ${mock.summary.priority} — <strong>Tags:</strong> ${mock.summary.tags.join(', ')}`;
  el('summary').appendChild(p);
  el('summary').appendChild(meta);
}

function renderClientInfo(){
  const area = el('clientInfo');
  area.innerHTML = '';
  const d = mock.clientInfo;
  area.innerHTML = `<div><strong>${d.name}</strong></div><div>ID: ${d.clientId}</div><div>Last payment: ${d.lastPayment}</div><div>Dues: ${d.dues}</div>`;
}

function sendMessage(){
  const input = el('messageInput');
  const text = input.value.trim();
  if(!text) return;
  const role = el('senderSelect').value;
  const name = role === 'agent' ? 'Agent Sam' : 'Worker Lee';
  mock.messages.push({role, name, text});
  input.value = '';
  renderMessages();
}

document.addEventListener('DOMContentLoaded', ()=>{
  createStructure();
  renderMessages();
  renderSuggestions();
  renderSummary();
  renderClientInfo();

  el('sendBtn').addEventListener('click', sendMessage);
  el('messageInput').addEventListener('keydown', (e)=>{ if(e.key === 'Enter') sendMessage(); });
});
