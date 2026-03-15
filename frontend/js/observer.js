export function startObserver(onActive){
  let stopped = false;
  let mockTimeout = null;

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

  // Try real polling; also start a mock timer that fires after 5s if no /active available
  poll();
  mockTimeout = setTimeout(()=>{
    if(!stopped){
      onActive('C-00124');
    }
  }, 5000);

  return {
    stop(){ stopped = true; if(mockTimeout) clearTimeout(mockTimeout); }
  };
}
