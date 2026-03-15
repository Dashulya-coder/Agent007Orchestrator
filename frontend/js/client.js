// backend/frontend/js/client.js

import * as R from './renderer.js';

const initialState = {
  messages: [],
  case_id: null, // Отримуємо від бекенду
  clientInfo: { name: 'Oleksiy', clientId: '1' } // Дані з твоєї mock_db.py
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
  const input = document.createElement('input');
  input.id = 'messageInput';
  input.placeholder = 'Type a message...';

  const btn = document.createElement('button');
  btn.id = 'sendBtn';
  btn.textContent = 'Send';

  inputRow.appendChild(input);
  inputRow.appendChild(btn);

  chatBox.appendChild(chatHeader);
  chatBox.appendChild(chat);
  chatBox.appendChild(inputRow);

  root.appendChild(chatBox);
}

function wire(){
  const sendBtn = document.getElementById('sendBtn');
  const input = document.getElementById('messageInput');

  sendBtn.addEventListener('click', async () => {
    const txt = input.value.trim();
    if(!txt) return;

    // Оптимістичне оновлення UI
    initialState.messages.push({ role: 'client', name: initialState.clientInfo.name, text: txt });
    R.renderMessages(initialState.messages);
    input.value = '';

    try {
      if (!initialState.case_id) {
        // Крок 1: Якщо це перше повідомлення — створюємо кейс
        const response = await fetch('/process', {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({
            user_id: parseInt(initialState.clientInfo.clientId),
            message: txt
          })
        });

        const data = await response.json();
        initialState.case_id = data.case_id;
        if (data.final_reply_to_user) {
        initialState.messages.push({
          role: 'agent',
          name: 'AI',
          text: data.final_reply_to_user
        });
      }
      } else {
        // Крок 2: Якщо кейс вже є — оновлюємо існуючий
        const response = await fetch(`/cases/${initialState.case_id}/active`, {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({ messages: initialState.messages })
        });

        const data = await response.json();
        initialState.messages = data.messages || initialState.messages;
      }

      // Фінальний рендер після відповіді бекенду
      R.renderMessages(initialState.messages);

    } catch(e) {
      console.error("Connection lost. Backend might be down.");
    }
  });

  input.addEventListener('keydown', (e) => {
    if(e.key === 'Enter') sendBtn.click();
  });
}

document.addEventListener('DOMContentLoaded', () => {
  createClientStructure();
  R.renderMessages(initialState.messages);
  wire();
});