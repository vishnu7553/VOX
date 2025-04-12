document.getElementById('recordButton').addEventListener('click', async function() {
    const button = this;
    const status = document.getElementById('recordingStatus');
    
    if (button.textContent.includes('Start')) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            let audioChunks = [];
            
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                const filename = `recording_${Date.now()}.wav`;
                formData.append('audio', audioBlob, filename);
                
                try {
                    status.textContent = "Saving recording...";
                    const response = await fetch('/save-recording', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        status.textContent = `Recording saved as ${filename}`;
                        // Optional: auto-refresh or update file list
                    } else {
                        status.textContent = "Error saving recording";
                    }
                } catch (error) {
                    console.error('Error:', error);
                    status.textContent = "Error saving recording";
                }
            };
            
            mediaRecorder.start();
            button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M5 3.5h6A1.5 1.5 0 0 1 12.5 5v6a1.5 1.5 0 0 1-1.5 1.5H5A1.5 1.5 0 0 1 3.5 11V5A1.5 1.5 0 0 1 5 3.5z"/></svg> Stop Recording';
            status.textContent = "Recording... Click again to stop";
            
            button.onclick = () => {
                mediaRecorder.stop();
                stream.getTracks().forEach(track => track.stop());
                button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M3.5 6.5A.5.5 0 0 1 4 7v1a4 4 0 0 0 8 0V7a.5.5 0 0 1 1 0v1a5 5 0 0 1-4.5 4.975V15h3a.5.5 0 0 1 0 1h-7a.5.5 0 0 1 0-1h3v-2.025A5 5 0 0 1 3 8V7a.5.5 0 0 1 .5-.5z"/><path d="M10 8a2 2 0 1 1-4 0V3a2 2 0 1 1 4 0v5zM8 0a3 3 0 0 0-3 3v5a3 3 0 0 0 6 0V3a3 3 0 0 0-3-3z"/></svg> Start Recording';
                button.onclick = arguments.callee;
            };
        } catch (error) {
            console.error('Error:', error);
            status.textContent = "Error accessing microphone";
        }
    }
});