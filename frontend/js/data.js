export async function loadData(key){
  async function tryFetch(url){
    const res = await fetch(url);
    if(!res.ok) throw new Error('fetch failed');
    return await res.json();
  }

  if(key){
    try{
      return await tryFetch(`/cases/${encodeURIComponent(key)}`);
    }catch(e){}
  }

  // Fallback mock data (used when fetch fails)
  const mock = {
    messages: [
      {role:'client', name:'Jane Doe', text:"Hi — my payment didn't go through and I need help."},
      {role:'agent', name:'Agent Sam', text:'I can help with that — can you confirm your last 4 digits of card?'},
      {role:'client', name:'Jane Doe', text:"It's 1234. Also I need assistance scheduling a visit."},
    ],
    suggestions: [
      'I can look into the payment status and follow up shortly.',
      "Thanks — I've escalated this to billing.",
      'Would Friday 2–4pm work for the visit?',
      'I will schedule and confirm back with you.'
    ],
    summary: {
      summaryText: 'Client reports payment failure and requests scheduling help. Prefers afternoon visits.',
      priority: 'Medium',
      tags: ['payment','scheduling']
    },
    clientInfo: {
      name: key ? `Client ${key}` : 'Jane Doe',
      clientId: key || 'C-00124',
      lastPayment: 'Failed on 2026-03-10',
      dues: '$0.00 (attempted payment failed)'
    }
  };

  return mock;
}

export async function pushAndWait(key, messages, options = {}){
  const { pollInterval = 1000, timeout = 30000 } = options;
  if(!key) throw new Error('pushAndWait requires a key');

  // Post worker update to the case active endpoint
  try{
    await fetch(`/cases/${encodeURIComponent(key)}/active`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ messages })
    });
  }catch(e){
    // ignore network errors here; we'll poll for updates below
  }

  const start = Date.now();
  const mockDelay = options.mockDelay || 3000;
  let sawNetwork = false;
  while(Date.now() - start < timeout){
    try{
      // prefer case endpoint for updates
      const res = await fetch(`/cases/${encodeURIComponent(key)}`);
      if(res.ok){
        const payload = await res.json();
        if(payload && Array.isArray(payload.messages)){
          return payload;
        }
        sawNetwork = true;
      }
    }catch(e){
      // swallow and retry
    }
    // If we haven't observed a working backend within mockDelay, return a simulated mock reply
    if(!sawNetwork && (Date.now() - start) >= mockDelay){
      const clientReply = { role: 'client', name: 'Client Mock', text: 'Thanks — I received the update and will follow up.' };
      const newSuggestions = [
        'Thanks for the update — I will check and confirm.',
        'Please provide the transaction ID so I can investigate.'
      ];
      return {
        messages: (messages || []).concat([clientReply]),
        suggestions: newSuggestions,
        summary: { summaryText: 'Client replied to the worker. Follow-up required.', priority: 'High', tags: ['client-replied'] },
        clientInfo: { name: `Client ${key}`, clientId: key }
      };
    }

    await new Promise(r => setTimeout(r, pollInterval));
  }

  return null;
}
