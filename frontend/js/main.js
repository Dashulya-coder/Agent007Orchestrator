import { loadData } from './data.js';
import * as R from './renderer.js';

let state = null;

function sendMessage(){
  const input = document.getElementById('messageInput');
  const text = input.value.trim();
  if(!text) return;
  const role = 'worker';
  const name = 'Worker Lee';
  state.messages.push({role, name, text});
  input.value = '';
  R.renderMessages(state.messages);
}

async function init(){
  state = await loadData();
  R.createStructure(state.clientInfo?.name || 'Client');
  R.renderAll(state);

  // Wire events
  const sendBtn = document.getElementById('sendBtn');
  if(sendBtn) sendBtn.addEventListener('click', sendMessage);
  const input = document.getElementById('messageInput');
  if(input) input.addEventListener('keydown', (e)=>{ if(e.key === 'Enter') sendMessage(); });
}

window.addEventListener('DOMContentLoaded', init);
