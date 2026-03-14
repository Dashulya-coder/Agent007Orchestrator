export async function loadData(key){
  async function tryFetch(url){
    const res = await fetch(url);
    if(!res.ok) throw new Error('fetch failed');
    return await res.json();
  }

  if(key){
    try{
      // try path-style first
      return await tryFetch(`/data/${encodeURIComponent(key)}`);
    }catch(e){}}

  // Fallback mock data (used when fetch fails)
  const mock = {
    messages: [
      {role:'client', name:'Jane Doe', text:"Hi — my payment didn't go through and I need help."},
      {role:'agent', name:'Agent Sam', text:'I can help with that — can you confirm your last 4 digits of card?'},
      {role:'client', name:'Jane Doe', text:"It's 1234. Also I need assistance scheduling a visit."},
      {role:'worker', name:'Worker Lee', text:'I can take the visit on Friday afternoon.'}
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
