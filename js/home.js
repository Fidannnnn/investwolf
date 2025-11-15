// js/home.js

// ----- Seeded posts (preloaded demo data) -----
const defaultPosts = [
  { user: 'WolfTrader', text: 'Bought 5 AAPL today', symbol: 'AAPL', action: 'buy' },
  { user: 'DemoUser', text: 'Sold 2 MSFT shares', symbol: 'MSFT', action: 'sell' },
  { user: 'WolfTrader', text: 'Considering TSLA long-term', symbol: 'TSLA', action: 'buy' },
];

// Load posts from localStorage or seed if empty
let postsDB = JSON.parse(localStorage.getItem('postsDB') || 'null');
if (!postsDB) {
  postsDB = defaultPosts;
  localStorage.setItem('postsDB', JSON.stringify(postsDB));
}

// ----- Render posts -----
function renderPosts() {
  const container = document.getElementById('posts-list');
  container.innerHTML = '';
  postsDB.forEach(post => {
    const postEl = document.createElement('div');
    postEl.className = 'post card';
    postEl.innerHTML = `
      <div class="post-header">
        <div><strong>${post.user}</strong></div>
      </div>
      <div class="post-body">${post.text}</div>
      ${post.symbol ? `<div class="post-action">Symbol: <strong>${post.symbol}</strong> — ${post.action}</div>` : ''}
    `;
    container.appendChild(postEl);
  });
}

// Initial render
renderPosts();

// ----- Handle new post creation -----
document.getElementById('btn-post').addEventListener('click', () => {
  const text = document.getElementById('post-text').value.trim();
  const symbol = document.getElementById('post-symbol').value || null;
  if (!text) return alert('Write something!');

  // Determine action based on symbol (random buy/sell)
  let action = null;
  if (symbol) action = Math.random() > 0.5 ? 'buy' : 'sell';

  const newPost = {
    user: 'WolfTrader',
    text,
    symbol,
    action,
  };

  postsDB.unshift(newPost);
  localStorage.setItem('postsDB', JSON.stringify(postsDB));
  renderPosts();

  // Clear textarea and symbol select
  document.getElementById('post-text').value = '';
  document.getElementById('post-symbol').value = '';
});
