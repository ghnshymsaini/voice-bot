function startConversation() {
    fetch("/voice", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("⚠️ Could not understand speech. Try again!");
        } else {
            document.getElementById("botResponse").innerText = "🤖 " + data.response;
            document.getElementById("audioPlayer").src = data.audio;
            document.getElementById("audioPlayer").play();
        }
    })
    .catch(error => console.error("Error:", error));
}
