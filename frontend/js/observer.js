export function startObserver(onActive){
  let stopped = false;

  async function poll(){
    if(stopped) return;
    try{
      const res = await fetch('/active');
      if(res.ok){
        const data = await res.json();
        if(data && data.key){
          onActive(data.key);
          return; // stop after receiving a key
        }
      }
    }catch(e){
      // network error - fall back to mock below
    }
    // schedule next poll
    setTimeout(()=>{ if(!stopped) poll(); }, 2000);
  }

  poll();
}
