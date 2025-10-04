async function sendMessage() {
  const input = document.getElementById("userInput");
  const chatbox = document.getElementById("chatbox");

  if (!input.value.trim()) return;

  let userMsg = document.createElement("div");
  userMsg.className = "message user";
  userMsg.innerText = input.value;
  chatbox.appendChild(userMsg);

  let response = await fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: input.value })
  });

  let data = await response.json();

  let botMsg = document.createElement("div");
  botMsg.className = "message bot";
  botMsg.innerText = data.answer;
  chatbox.appendChild(botMsg);

  chatbox.scrollTop = chatbox.scrollHeight;
  input.value = "";
}

// Welcome message
window.onload = () => {
  const chatbox = document.getElementById("chatbox");
  let welcomeMsg = document.createElement("div");
  welcomeMsg.className = "message bot";
  welcomeMsg.innerText =
    "👋 Welcome! I’m your Current Affairs Chatbot. I can answer around 50 questions about recent events like elections, economy, sports, and world news. Try asking me something!";
  chatbox.appendChild(welcomeMsg);
};

// Rotating placeholder examples
const examples = [
  "Who is the Prime Minister of India?",
  "Which country hosted G20 in 2023?",
  "Who won the Cricket World Cup 2023?",
  "What is India’s GDP growth forecast?"
];

let idx = 0;
setInterval(() => {
  document.getElementById("userInput").placeholder = "Ask me: " + examples[idx];
  idx = (idx + 1) % examples.length;
}, 3000);
