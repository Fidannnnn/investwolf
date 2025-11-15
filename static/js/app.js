async function api(path, opts){
  const res = await fetch(path, opts);
  if(res.headers.get('content-type')?.includes('application/json')) return res.json();
  return res.text();
}

// Home: post creation
const btnPost = document.getElementById('btn-post');
if(btnPost){
  btnPost.addEventListener('click', async ()=>{
    const text = document.getElementById('post-text').value.trim();
    const symbol = document.getElementById('post-symbol').value || null;
    if(!text) return alert('Write something');
    // demo: user_id=1
    const newPost = await api('/api/posts', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({user_id:1, text, action: symbol? 'mention': null, symbol})});
    location.reload();
  });
}

// AI page: quiz and search
const aiBtn = document.getElementById('btn-ai-submit');
if(aiBtn){
  aiBtn.addEventListener('click', async ()=>{
    const exp = document.getElementById('q-exp').value;
    const risk = document.getElementById('q-risk').value;
    const timeframe = document.getElementById('q-timeframe').value;
    const sectorsEl = document.getElementById('q-sectors');
    const sectors = Array.from(sectorsEl.selectedOptions).map(o=>o.value);
    const goal = document.getElementById('q-goal').value;
    const payload = {experience: exp, risk, timeframe, sectors, goal};
    const res = await api('/api/ai/advice', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(payload)});
    document.getElementById('ai-advice').textContent = res.advice;
  });
}

const btnSearch = document.getElementById('btn-search');
if(btnSearch){
  btnSearch.addEventListener('click', async ()=>{
    const q = document.getElementById('search-input').value.trim();
    const res = await api('/api/search?q='+encodeURIComponent(q));
    const node = document.getElementById('search-results');
    node.innerHTML = '';
    if(res.stocks?.length){
      const ul = document.createElement('ul');
      res.stocks.forEach(s=>{ const li = document.createElement('li'); li.innerHTML = `<a href="/stock/${s.symbol}">${s.symbol}</a> - ${s.name}`; ul.appendChild(li); });
      node.appendChild(ul);
    }
    if(res.posts?.length){
      const h = document.createElement('h4'); h.textContent='Posts'; node.appendChild(h);
      res.posts.forEach(p=>{ const pdiv = document.createElement('div'); pdiv.textContent = p.text; node.appendChild(pdiv); });
    }
  });
}

// Demo topup & buy
const btnTopup = document.getElementById('btn-topup');
if(btnTopup){
  btnTopup.addEventListener('click', async ()=>{
    const amount = parseFloat(document.getElementById('topup-amount').value || 0);
    if(!amount || amount<=0) return alert('Enter a positive amount');
    await api('/api/demo/topup', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({amount})});
    location.reload();
  });
}

document.querySelectorAll('.btn-buy').forEach(b=> b.addEventListener('click', async (e)=>{
  alert('Demo buy executed: this is a UI placeholder.');
}));

document.getElementById && document.querySelectorAll('.btn-buy').length && console.log('Buy buttons active');
