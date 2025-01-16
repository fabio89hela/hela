let recorder, audioBlob;
const transcriptionBox = document.getElementById('transcription');
const startButton = document.getElementById('start');
const pauseButton = document.getElementById('pause');
const resumeButton = document.getElementById('resume');
const stopButton = document.getElementById('stop');

// Recorder setup
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const chunks = [];
    recorder = new MediaRecorder(stream);

    recorder.ondataavailable = e => chunks.push(e.data);

    recorder.onstop = async () => {
      audioBlob = new Blob(chunks, { type: 'audio/webm' });

      // Convert audioBlob to FormData
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.webm');

      // Send audio to the Netlify Function
      try {
        const response = await fetch('/.netlify/functions/transcribe', {
          method: 'POST',
          body: formData,
        });

        const result = await response.json();
        if (result.transcription) {
          transcriptionBox.value = result.transcription;
        } else {
          console.error('No transcription received:', result);
        }
      } catch (error) {
        console.error('Error calling transcription function:', error);
      }
    };
  });

startButton.addEventListener('click', () => {
  recorder.start();
  startButton.disabled = true;
  pauseButton.disabled = false;
  stopButton.disabled = false;
});

pauseButton.addEventListener('click', () => {
  recorder.pause();
  pauseButton.disabled = true;
  resumeButton.disabled = false;
});

resumeButton.addEventListener('click', () => {
  recorder.resume();
  pauseButton.disabled = false;
  resumeButton.disabled = true;
});

stopButton.addEventListener('click', () => {
  recorder.stop();
  startButton.disabled = false;
  pauseButton.disabled = true;
  resumeButton.disabled = true;
  stopButton.disabled = true;
});
