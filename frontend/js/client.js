import * as R from './renderer.js';

const initialState = {
  messages: [],
  suggestions: [],
  summary: {},
  clientInfo: { name: 'Testing Kate', clientId: 'TEST-001' }
};

function createClientStructure(){
  const root = document.getElementById('app');
  root.innerHTML = '';

  const chatBox = document.createElement('div');
  chatBox.className = 'chat-box client-only';

  const chatHeader = document.createElement('div');
  chatHeader.className = 'chat-header';
  chatHeader.textContent = 'Support chat';

  const chat = document.createElement('div');
  chat.id = 'chat';
  chat.className = 'chat';
  chat.style.flex = '1';
  chat.style.minHeight = '0';
  chat.style.display = 'flex';
  chat.style.flexDirection = 'column';

  const inputRow = document.createElement('div');
  inputRow.className = 'input-row';
  const input = document.createElement('input'); input.id = 'messageInput'; input.placeholder = 'Type a message';
  const btn = document.createElement('button'); btn.id = 'sendBtn'; btn.textContent = 'Send';
  inputRow.appendChild(input); inputRow.appendChild(btn);

  chatBox.appendChild(chatHeader);
  chatBox.appendChild(chat);
  chatBox.appendChild(inputRow);

  root.appendChild(chatBox);
}

function wire(){
  const sendBtn = document.getElementById('sendBtn');
  const input = document.getElementById('messageInput');
  let caseId = null;
  function makeId(){
    if(window.crypto && window.crypto.randomUUID) return window.crypto.randomUUID();
    // fallback simple uuid v4
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c){
      const r = Math.random()*16|0, v = c=='x'?r:(r&0x3|0x8);
      return v.toString(16);
    });
  }

  sendBtn.addEventListener('click', async () => {
    const txt = input.value.trim(); if(!txt) return;
    if(!caseId) caseId = makeId();

    // send initial process to backend with user_id, message and case_id
    try{
      await fetch('/process', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ user_id: initialState.clientInfo.clientId || initialState.clientInfo.name, message: txt, case_id: caseId })
      });
    }catch(e){
      // ignore network errors in mock
    }

    initialState.messages.push({ role: 'client', name: 'Testing Kate', text: txt });
    input.value = '';
    R.renderMessages(initialState.messages);
  });
  input.addEventListener('keydown', (e)=>{ if(e.key === 'Enter') sendBtn.click(); });
}

document.addEventListener('DOMContentLoaded', ()=>{
  createClientStructure();
  R.renderMessages(initialState.messages);
  wire();
});
