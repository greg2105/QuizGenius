document.addEventListener('DOMContentLoaded', () => {
  const videoIdInput = document.getElementById('video_id');
  const startTimeInput = document.getElementById('start_time');
  const endTimeInput = document.getElementById('end_time');
  const generateQuizButton = document.getElementById('generate_quiz');

  // Get the video ID from the content script
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, { message: 'get_video_id' }, (response) => {
      if (response && response.video_id) {
        videoIdInput.value = response.video_id;
      }
    });
  });

  // Add event listener for the "Generate Quiz" button
  generateQuizButton.addEventListener('click', () => {
    const videoId = videoIdInput.value;
    const startTime = startTimeInput.value;
    const endTime = endTimeInput.value;

    // Validate the input values and call the function to generate the quiz
    if (videoId && startTime && endTime) {
      generateQuiz(videoId, startTime, endTime);
    } else {
      alert('Please fill in all the fields.');
    }
  });
});

async function generateQuiz(videoId, startTime, endTime) {
  const apiUrl = '<YOUR_BACKEND_API_URL>/generate_quiz';
  const transcript = await getTranscript(videoId, startTime, endTime);

  if (transcript) {
    const requestBody = { text: transcript };

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (response.ok) {
        const quizData = await response.json();
        displayQuiz(quizData.questions);
      } else {
        alert('Error generating quiz. Please try again.');
      }
    } catch (error) {
      console.error('Error generating quiz:', error);
      alert('Error generating quiz. Please try again.');
    }
  } else {
    alert('Error fetching the transcript. Please try again.');
  }
}