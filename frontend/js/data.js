export async function loadData(){
  try{
    const res = await fetch('/data');
    if(!res.ok) throw new Error('fetch failed');
    const json = await res.json();
    return json;
  }catch(e){
    // Fallback mock data
    return {
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
        name: 'Jane Doe',
        clientId: 'C-00124',
        lastPayment: 'Failed on 2026-03-10',
        dues: '$0.00 (attempted payment failed)'
      }
    };
  }
}
