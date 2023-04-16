// content_script.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.message === 'get_video_id') {
      const videoId = extractVideoId();
      sendResponse({ video_id: videoId });
    }
  });
  
  function extractVideoId() {
    const videoIdParam = new URLSearchParams(window.location.search).get('v');
    return videoIdParam;
  }

  async function getTranscript(videoId, startTime, endTime) {
    const response = await fetch('/get_transcript', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ video_id: videoId, start_time: startTime, end_time: endTime }),
    });

    const data = await response.json();
    return data.transcript;
  }
  
  async function generateQuiz(transcript) {
    const response = await fetch('/generate_quiz', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: transcript }),
    });

    const data = await response.json();
    return data.questions;
  }

  function displayQuiz(quizQuestions) {
    const quizContainer = document.getElementById('quiz-container');
    quizContainer.innerHTML = '';
  
    quizQuestions.forEach((question, index) => {
      const questionElement = document.createElement('div');
      questionElement.className = 'question';
      questionElement.innerHTML = `
        <h3>Question ${index + 1}: ${question.question}</h3>
        <ul>
          ${question.answers.map((answer) => `<li>${answer}</li>`).join('')}
        </ul>
      `;
      quizContainer.appendChild(questionElement);
    });
  }