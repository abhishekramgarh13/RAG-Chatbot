document.addEventListener("DOMContentLoaded", fetchHistory);

async function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;

    let chatBox = document.getElementById("chat-box");

    // Append user message to chat box
    chatBox.innerHTML += `<div class="message user-message"><strong>You:</strong> ${userInput}</div>`;
    
    // Show loading message
    let loadingMsg = document.createElement("div");
    loadingMsg.className = "message ai-message loading";
    loadingMsg.innerHTML = "<strong>AI:</strong> Thinking...";
    chatBox.appendChild(loadingMsg);

    chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to bottom

    document.getElementById("user-input").value = ""; // Clear input

    try {
        let response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: userInput })
        });

        let data = await response.json();

        // Remove loading message
        loadingMsg.remove();

        // Append AI response
        let aiMessage = document.createElement("div");
        aiMessage.className = "message ai-message";
        aiMessage.innerHTML = `<strong>AI:</strong> ${formatResponse(data.answer)}`;
        chatBox.appendChild(aiMessage);

    } catch (error) {
        console.error("Error:", error);
        loadingMsg.innerHTML = "<strong>AI:</strong> Sorry, something went wrong.";
    }

    chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll
    fetchHistory(); // Refresh history
}

async function fetchHistory() {
    try {
        let response = await fetch("http://127.0.0.1:5000/history");
        let historyData = await response.json();

        let historyBox = document.getElementById("history-box");
        historyBox.innerHTML = "";

        historyData.reverse().forEach(entry => {
            let msgClass = entry.role === "user" ? "user-message" : "ai-message";
            historyBox.innerHTML += `<div class="message ${msgClass}"><strong>${entry.role === "user" ? "You" : "AI"}:</strong> ${formatResponse(entry.content)}</div>`;
        });

        historyBox.scrollTop = historyBox.scrollHeight; // Auto-scroll

    } catch (error) {
        console.error("Error fetching history:", error);
    }
}

function formatResponse(text) {
    return text.replace(/\n/g, "<br>"); // Preserve new lines
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
