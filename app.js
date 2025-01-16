let recorder, audioBlob;
const audioElement = document.getElementById('audio');
const transcriptionBox = document.getElementById('transcription');
const startButton = document.getElementById('start');
const pauseButton = document.getElementById('pause');
const resumeButton = document.getElementById('resume');
const stopButton = document.getElementById('stop');
const downloadButton = document.getElementById('download');
const shareButton = document.getElementById('share');

// Setup waveform visualization
const canvas = document.createElement('canvas');
document.getElementById('waveform').appendChild(canvas);
const canvasCtx = canvas.getContext('2d');

// Recorder setup
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const audioContext = new AudioContext();
    const source = audioContext.createMediaStreamSource(stream);
    const analyser = audioContext.createAnalyser();
    source.connect(analyser);

    const dataArray = new Uint8Array(analyser.frequencyBinCount);
    canvas.width = 600;
    canvas.height = 100;

    function drawWaveform() {
      requestAnimationFrame(drawWaveform);
      analyser.getByteTimeDomainData(dataArray);
      canvasCtx.fillStyle = 'white';
      canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
      canvasCtx.lineWidth = 2;
      canvasCtx.strokeStyle = 'black';
      canvasCtx.beginPath();

      const sliceWidth = canvas.width / dataArray.length;
      let x = 0;

      for (let i = 0; i < dataArray.length; i++) {
        const v = dataArray[i] / 128.0;
        const y = (v * canvas.height) / 2;

        if (i === 0) {
          canvasCtx.moveTo(x, y);
        } else {
          canvasCtx.lineTo(x, y);
        }

        x += sliceWidth;
      }
      canvasCtx.lineTo(canvas.width, canvas.height / 2);
      canvasCtx.stroke();
    }

    drawWaveform();

    recorder = new MediaRecorder(stream);
    const chunks = [];

    recorder.ondataavailable = e => chunks.push(e.data);
    recorder.onstop = () => {
      audioBlob = new Blob(chunks, { type: 'audio/webm' });
      const audioURL = URL.createObjectURL(audioBlob);
      audioElement.src = audioURL;
      downloadButton.disabled = false;
      shareButton.disabled = false;
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

// Download and share functionality
downloadButton.addEventListener('click', () => {
  const link = document.createElement('a');
  link.href = URL.createObjectURL(audioBlob);
  link.download = 'recording.webm';
  link.click();
});

shareButton.addEventListener('click', () => {
  if (navigator.share) {
    navigator.share({
      title: 'Recording',
      files: [new File([audioBlob], 'recording.webm', { type: 'audio/webm' })],
    });
  } else {
    alert('Condivisione non supportata.');
  }
});
