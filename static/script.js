const languageSelect = document.getElementById("language-select");
const translateToSelect = document.getElementById("translate-to-select");
const recognition = new webkitSpeechRecognition();

function startRecognition() {
  recognition.continuous = true;
  recognition.interimResults = false;
  recognition.lang = languageSelect.value;

  recognition.start();

  recognition.onresult = function (event) {
    const speechResult = event.results[event.results.length - 1][0].transcript;
    console.log("Speech Result:", speechResult);
    translate(speechResult);
  };

  recognition.onerror = function (event) {
    console.error(event);
    alert("Error occurred. Please try again.");
  };
}

function stopRecognition() {
  recognition.stop();
}

async function translate(text) {
  const translateTo = translateToSelect.value;

  const response = await fetch(`/translate?text=${text}&to=${translateTo}`, {
    method: "GET",
  });

  const data = await response.json();
  console.log("Translated Text:", data.translated_text);

  const audio = new Audio(data.audio_url);
  audio.play();

  const translatedTextElement = document.getElementById("translated-text");
  translatedTextElement.textContent = data.translated_text;
}

const startButton = document.getElementById("start-button");
const stopButton = document.getElementById("stop-button");

startButton.addEventListener("click", startRecognition);
stopButton.addEventListener("click", stopRecognition);
