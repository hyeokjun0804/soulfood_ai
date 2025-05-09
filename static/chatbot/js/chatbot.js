// chatbot.js
function sendMessage(event) {
    event.preventDefault(); // 기본 제출 동작 방지

    const userInput = document.getElementById('user-input');
    const userMessage = userInput.value;

    // 사용자 메시지를 채팅 박스에 추가
    addMessage(userMessage, 'user');

    // AJAX 요청을 통해 챗봇 응답 받기
    fetch('/chatbot/chatbot-response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken') // CSRF 토큰 추가
        },
        body: new URLSearchParams({
            'message': userMessage
        })
    })
    .then(response => response.json())
    .then(data => {
        // 챗봇의 응답을 채팅 박스에 추가
        addMessage(data.response, 'bot');
        userInput.value = ''; // 입력 필드 초기화
        scrollToBottom(); // 스크롤 하단으로 이동
    })
    .catch(error => console.error('Error:', error));
}

// 메시지를 채팅 박스에 추가하는 함수
function addMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
}

// 스크롤을 하단으로 이동하는 함수
function scrollToBottom() {
    const chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}

// CSRF 토큰을 가져오는 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // 특정 쿠키의 값 가져오기
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
