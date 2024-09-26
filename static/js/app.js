// Global sessionId variable to store the session ID
let sessionId = "";

// Function to append messages to the chat window
function appendMessage(message, className) {
    const chatWindow = document.getElementById("chat-window");
    const messageDiv = document.createElement("div");
    messageDiv.textContent = message;
    messageDiv.classList.add("message", className);
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;  // Auto-scroll to the bottom
}

// Start a new session when the user loads the page
async function startNewSession() {
    try {
        const response = await fetch("/start_session", { method: "POST" });
        const data = await response.json();
        
        if (data.session_id) {
            sessionId = data.session_id;
            console.log("New session started: " + sessionId);
        } else {
            console.error("Failed to start session: ", data.error);
            appendMessage("Error: Could not start session.", "system");
        }
    } catch (error) {
        console.error("Error starting session: ", error);
        appendMessage("Error: Could not start session.", "system");
    }
}

// Send user input to the backend
async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const modelChoice = document.getElementById("model-choice").value;

    if (!userInput || !modelChoice || !sessionId) {
        appendMessage("Please enter a message, choose a model, and make sure the session is active.", "system");
        return;
    }

    appendMessage(`You: ${userInput}`, "user");
    document.getElementById("user-input").value = "";  // Clear input field

    // Show loader during request
    document.getElementById("loader").style.display = "block";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_input: userInput,
                model_choice: modelChoice,
                session_id: sessionId
            })
        });

        const data = await response.json();
        document.getElementById("loader").style.display = "none";  // Hide loader

        if (data.error) {
            appendMessage(`Error: ${data.error}`, "system");
        } else {
            appendMessage(`AI: ${data.response}`, "ai");
        }
    } catch (error) {
        document.getElementById("loader").style.display = "none";  // Hide loader
        console.error("Error sending message: ", error);
        appendMessage("Error: Could not send message.", "system");
    }
}

// End session and delete files
async function endSession() {
    if (!sessionId) {
        appendMessage("No active session to end.", "system");
        return;
    }

    try {
        const response = await fetch("/end_session", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId })
        });

        const data = await response.json();
        appendMessage(`System: ${data.message}`, "system");
        sessionId = "";  // Reset session ID
    } catch (error) {
        console.error("Error ending session: ", error);
        appendMessage("Error: Could not end session.", "system");
    }
}

// Upload file to Google Drive
async function uploadToGDrive() {
    const modelChoice = document.getElementById("model-choice").value;

    if (!sessionId || !modelChoice) {
        appendMessage("No active session or invalid model choice.", "system");
        return;
    }

    // Show loader during upload
    document.getElementById("loader").style.display = "block";

    try {
        const response = await fetch("/upload_to_gdrive", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ model_choice: modelChoice, session_id: sessionId })
        });

        const data = await response.json();
        document.getElementById("loader").style.display = "none";  // Hide loader

        if (data.error) {
            appendMessage(`Error: ${data.error}`, "system");
        } else {
            document.getElementById("gdrive-link").innerHTML = 
                `Google Docs link: <a href="${data.google_docs_link}" target="_blank">${data.google_docs_link}</a>`;
        }
    } catch (error) {
        document.getElementById("loader").style.display = "none";  // Hide loader
        console.error("Error uploading to Google Drive: ", error);
        appendMessage("Error: Could not upload file.", "system");
    }
}

// Download the latest file
function downloadFile() {
    const modelChoice = document.getElementById("model-choice").value;
    if (!sessionId || !modelChoice) {
        appendMessage("No active session or invalid model choice.", "system");
        return;
    }
    window.location.href = `/download/${modelChoice}?session_id=${sessionId}`;
}

// Attach event listeners to the buttons after DOM is loaded
window.onload = function() {
    document.getElementById("send-btn").addEventListener("click", sendMessage);
    document.getElementById("end-session-btn").addEventListener("click", endSession);
    document.getElementById("upload-btn").addEventListener("click", uploadToGDrive);
    document.getElementById("download-btn").addEventListener("click", downloadFile);

    // Start a new session when the page loads
    startNewSession();
};
