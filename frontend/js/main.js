import { loadData } from './data.js';
import * as R from './renderer.js';
import { startObserver } from './observer.js';

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
  // Show a minimal waiting UI and DO NOT fetch full case data yet.
  R.createStructure('Waiting for active case...');
  // Render empty placeholders so chat area exists but contains no messages yet
  R.renderAll({messages:[], suggestions:[], summary:{}, clientInfo:{name:'—'}});

  // Wire send UI (will operate on whichever state is current)
  // Wire send UI but keep it disabled until a case is loaded
  function wireSend(){
    const sendBtn = document.getElementById('sendBtn');
    const input = document.getElementById('messageInput');
    if(sendBtn){ sendBtn.removeEventListener('click', sendMessage); sendBtn.addEventListener('click', ()=>{ if(state) sendMessage(); }); sendBtn.disabled = !state; }
    if(input){ input.removeEventListener('keydown', sendMessageListener); input.addEventListener('keydown', (e)=>{ if(state) sendMessageListener(e); }); input.disabled = !state; }
  }

  function sendMessageListener(e){ if(e.key === 'Enter') sendMessage(); }
  wireSend();

  // Start observer to monitor /active. When a key is found, load that case and render.
  startObserver(async (key)=>{
    const caseState = await loadData(key);
    state = caseState;
    R.createStructure(state.clientInfo?.name || `Client ${key}`);
    R.renderAll(state);
    wireSend();
  });
}

window.addEventListener('DOMContentLoaded', init);
