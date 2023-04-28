const URL = "ws://" + location.host + "/websocket";

var inputLang = document.getElementById("translate_from").value;
var outputLang = document.getElementById("translate_to").value;

var mediaRecorder;

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/mp3" });
            mediaRecorder.start();
            document.getElementById("status").textContent = "Recording...";
        })
        .catch(error => console.log(error));
}

function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();
        document.getElementById("status").textContent = "Click the Record button to start recording.";
        mediaRecorder.addEventListener("dataavailable", event => {
            var socket = new WebSocket(URL);
            socket.addEventListener("open", event => {
                socket.send(JSON.stringify({ filename: "audio.mp3", data: event.data, inputLang: inputLang, outputLang: outputLang }));
            });
            socket.addEventListener("message", event => {
                document.getElementById("translation-result").textContent = event.data;
            });
        });
    }
}

document.getElementById("record-button").addEventListener("mousedown", startRecording);
document.getElementById("record-button").addEventListener("mouseup", stopRecording);

document.getElementById("input-lang").addEventListener("change", event => {
    inputLang = event.target.value;
});

document.getElementById("output-lang").addEventListener("change", event => {
    outputLang = event.target.value;
});

mediaRecorder.addEventListener("dataavailable", event => {
    var reader = new FileReader();
    reader.readAsArrayBuffer(event.data);
    reader.onloadend = function() {
        var audioBlob = new Blob([reader.result], { type: "audio/mp3" });
        var audioData = new Uint8Array(reader.result);
        var socket = new WebSocket(URL);
        socket.addEventListener("open", event => {
            socket.send(JSON.stringify({ filename: "audio.mp3", data: audioData, inputLang: inputLang, outputLang: outputLang }));
        });
        socket.addEventListener("message", event => {
            document.getElementById("translation-result").textContent = event.data;
        });
    }
});
