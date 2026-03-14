import { loadData, pushAndWait } from './data.js';
import * as R from './renderer.js';
import { startObserver } from './observer.js';

let state = null;
let isWaitingForBackend = false;

async function sendMessage() {
  // Перевірка наявності стану та case_id перед відправкою
  if (!state || !state.case_id || isWaitingForBackend) return;
  
  const input = document.getElementById('messageInput');
  const text = input.value.trim();
  if (!text) return;

  // Оптимістичне відображення повідомлення оператора
  state.messages.push({ role: 'worker', name: 'Worker Lee', text });
  input.value = '';
  R.renderMessages(state.messages);

  isWaitingForBackend = true;
  try {
    R.showSuggestionsPlaceholder('AI is thinking...');

    // Отримання оновлених даних (включаючи нові саджести AI)
    const resp = await pushAndWait(state.case_id, state.messages);
    
    if (resp) {
      // Оновлюємо стан на основі відповіді бекенду
      state = { ...state, ...resp }; 
      R.renderMessages(state.messages);
      R.renderSuggestions(state.suggestions);
      R.renderSummary(state.summary);
    }
  } catch (e) {
    console.error('Update failed:', e);
  } finally {
    isWaitingForBackend = false;
  }
}

async function init(){
  R.createStructure('Waiting for active case...');
  R.renderAll({messages:[], suggestions:[], summary:{}, clientInfo:{name:'—'}});

  function wireSend(){
    const sendBtn = document.getElementById('sendBtn');
    const input = document.getElementById('messageInput');
    
    if(sendBtn){
      sendBtn.disabled = !state;
      // Очищення старих лісенерів для уникнення дублікатів
      const newBtn = sendBtn.cloneNode(true);
      sendBtn.parentNode.replaceChild(newBtn, sendBtn);
      newBtn.addEventListener('click', sendMessage);
    }
    
    if(input){
      input.disabled = !state;
      input.onkeydown = (e) => { if(e.key === 'Enter') sendMessage(); };
    }
  }

  wireSend();

  // Запуск спостерігача: як тільки з'явиться кейс — завантажуємо та активуємо UI
  startObserver(async (key)=>{
    const caseData = await loadData(key);
    if (caseData) {
      state = caseData;
      R.createStructure(state.clientInfo?.name || `Client ${key}`);
      R.renderAll(state);
      wireSend();
    }
  });
}

window.addEventListener('DOMContentLoaded', init);