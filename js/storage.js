const DB = {
  init: () => {
    if (!localStorage.getItem("users")) {
      localStorage.setItem("users", JSON.stringify([
        {id:1, name:"Ayla", username:"wolf_trader", avatar:"img/avatar1.png", bio:"Building simple investing strategies."},
        {id:2, name:"Demo", username:"demo_user", avatar:"img/avatar2.png", bio:"Testing the market."}
      ]));
    }
    if (!localStorage.getItem("posts")) {
      localStorage.setItem("posts", JSON.stringify([
        {id:1, user_id:1, text:"Bought 5 AAPL today", symbol:"AAPL", action:"buy", ts:"2025-11-15T08:00:00Z"},
        {id:2, user_id:2, text:"Thinking about MSFT long-term", symbol:"MSFT", action:"mention", ts:"2025-11-14T12:00:00Z"}
      ]));
    }
    if (!localStorage.getItem("demo")) {
      localStorage.setItem("demo", JSON.stringify({balance:10000, history:[], positions:[]})); 
    }
  },
  get: (key) => JSON.parse(localStorage.getItem(key) || "[]"),
  set: (key, val) => localStorage.setItem(key, JSON.stringify(val))
};
DB.init();
