document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('overlay');
    const ctx = canvas.getContext('2d');
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
    const detectedObjectSpan = document.getElementById('detected-object');
    const translationSpan = document.getElementById('translation');
    const pronounceButton = document.getElementById('pronounceButton');

    let stream;
    let objectDetectionInterval;

    startButton.addEventListener('click', startAR);
    stopButton.addEventListener('click', stopAR);
    pronounceButton.addEventListener('click', pronounceWord);

    async function startAR() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            objectDetectionInterval = setInterval(detectObjects, 1000);
        } catch (error) {
            console.error('Error accessing the webcam:', error);
        }
    }

    function stopAR() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        clearInterval(objectDetectionInterval);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        detectedObjectSpan.textContent = '';
        translationSpan.textContent = '';
    }

    async function detectObjects() {
        // Here we'll use a placeholder function for object detection
        // In a real implementation, you'd use TensorFlow.js or a similar library
        const detectedObject = await simulateObjectDetection();
        detectedObjectSpan.textContent = detectedObject;
        
        // Simulate translation (replace with actual API call in production)
        const translation = await simulateTranslation(detectedObject);
        translationSpan.textContent = translation;

        // Draw bounding box (simplified)
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 3;
        ctx.strokeRect(50, 50, 100, 100);
    }

    async function simulateObjectDetection() {
        const objects = ['cup', 'book', 'chair', 'computer', 'phone'];
        return objects[Math.floor(Math.random() * objects.length)];
    }

    async function simulateTranslation(word) {
        const translations = {
            'cup': 'tasse',
            'book': 'livre',
            'chair': 'chaise',
            'computer': 'ordinateur',
            'phone': 'téléphone'
        };
        return translations[word] || 'unknown';
    }

    function pronounceWord() {
        const word = translationSpan.textContent;
        if (word) {
            const utterance = new SpeechSynthesisUtterance(word);
            utterance.lang = 'fr-FR'; // Set to French for this example
            speechSynthesis.speak(utterance);
        }
    }
});