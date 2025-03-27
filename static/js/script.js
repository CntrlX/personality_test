document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const resultContainer = document.getElementById('result-container');
    const mbtiTitle = document.getElementById('mbti-title');
    const mbtiOverview = document.getElementById('mbti-overview');
    const roastContainer = document.getElementById('roast-container');
    const roastToggle = document.getElementById('roast-toggle');
    const recommendations = document.getElementById('recommendations');
    const doppelgangers = document.getElementById('doppelgangers');
    const relationshipInsights = document.getElementById('relationship-insights');
    const careerInsights = document.getElementById('career-insights');
    const voiceToggle = document.getElementById('voice-toggle');
    const voiceIndicator = document.getElementById('voice-indicator');
    
    // Voice state
    let isVoiceActive = false;
    
    // Connect to Socket.IO server
    const socket = io();
    
    // Initialize chat
    init();
    
    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    voiceToggle.addEventListener('click', toggleVoice);
    roastToggle.addEventListener('click', toggleRoast);
    
    // Functions
    function init() {
        // Send empty message to get initial greeting
        socket.emit('message', { message: '' });
    }
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        // Add user message to chat
        addMessageToChat('user', message);
        
        // Clear input field
        userInput.value = '';
        
        // Disable input temporarily
        setInputState(false);
        
        // Send message to server
        socket.emit('message', { message });
    }
    
    function addMessageToChat(sender, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
        
        // Handle markdown-like formatting for bot messages
        if (sender === 'bot' && content.includes('\n')) {
            content = formatBotMessage(content);
        }
        
        messageDiv.innerHTML = content;
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom of chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function formatBotMessage(content) {
        // Convert markdown-like syntax to HTML
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
            .replace(/\n\n/g, '<br><br>') // Double line breaks
            .replace(/\n-\s(.*)/g, '<br>• $1') // List items
            .replace(/\n/g, '<br>'); // Single line breaks
    }
    
    function setInputState(enabled) {
        userInput.disabled = !enabled;
        sendButton.disabled = !enabled;
        if (enabled) {
            userInput.focus();
        }
    }
    
    function showResults(resultContent) {
        // Hide chat container and show results
        document.querySelector('.chat-container').classList.add('hidden');
        resultContainer.classList.remove('hidden');
        
        // Extract MBTI type and title
        const mbtiTypeMatch = resultContent.match(/🎉 Your MBTI Personality Type: (\w{4})/);
        if (mbtiTypeMatch) {
            const mbtiType = mbtiTypeMatch[1];
            const mbtiTypeTitle = getMbtiTypeTitle(mbtiType);
            mbtiTitle.innerHTML = `${mbtiType}: ${mbtiTypeTitle}`;
        }
        
        // Extract overview
        const overviewMatch = resultContent.match(/📝 Overview\s*([\s\S]*?)(?=\n\n🔥 Roast|\n\n🎯)/i);
        if (overviewMatch) {
            mbtiOverview.innerHTML = formatBotMessage(overviewMatch[1]);
        }
        
        // Extract roast
        const roastMatch = resultContent.match(/🔥 Roast\s*([\s\S]*?)(?=\n\n🎯)/i);
        if (roastMatch) {
            roastContainer.innerHTML = formatBotMessage(roastMatch[1]);
        }
        
        // Extract recommendations
        const recommendationsMatch = resultContent.match(/🎯.*?recommendations.*?\s*([\s\S]*?)(?=\n\nWho are your celebrity|\n\nRemember)/i);
        if (recommendationsMatch) {
            displayRecommendations(recommendationsMatch[1]);
        }
        
        // Extract doppelgangers
        const doppelgangersMatch = resultContent.match(/Who are your celebrity doppelgangers\?\s*([\s\S]*?)(?=\n\nRelationship|\n\nRemember)/i);
        if (doppelgangersMatch) {
            displayDoppelgangers(doppelgangersMatch[1]);
        }
        
        // Extract relationship insights
        const relationshipMatch = resultContent.match(/Relationship\s*([\s\S]*?)(?=\n\nCareer insights|\n\nRemember)/i);
        if (relationshipMatch) {
            relationshipInsights.innerHTML = formatBotMessage(relationshipMatch[1]);
        }
        
        // Extract career insights
        const careerMatch = resultContent.match(/Career insights\s*([\s\S]*?)(?=\n\nRemember|$)/i);
        if (careerMatch) {
            careerInsights.innerHTML = formatBotMessage(careerMatch[1]);
        }
    }
    
    function getMbtiTypeTitle(mbtiType) {
        const mbtiTitles = {
            "ISTJ": "The Inspector",
            "ISFJ": "The Protector",
            "INFJ": "The Counselor",
            "INTJ": "The Mastermind",
            "ISTP": "The Craftsman",
            "ISFP": "The Composer",
            "INFP": "The Healer",
            "INTP": "The Architect",
            "ESTP": "The Dynamo",
            "ESFP": "The Performer",
            "ENFP": "The Champion",
            "ENTP": "The Visionary",
            "ESTJ": "The Supervisor",
            "ESFJ": "The Provider",
            "ENFJ": "The Teacher",
            "ENTJ": "The Commander"
        };
        return mbtiTitles[mbtiType] || "The Personality";
    }
    
    function toggleRoast() {
        if (roastContainer.classList.contains('hidden')) {
            // Show roast
            roastContainer.classList.remove('hidden');
            roastToggle.textContent = 'Hide Roast';
        } else {
            // Hide roast
            roastContainer.classList.add('hidden');
            roastToggle.textContent = 'Roast Me';
        }
    }

    function displayRecommendations(content) {
        // Clear previous recommendations
        recommendations.innerHTML = '';
        
        // Create categories
        const categories = ['Music', 'Books', 'Movies'];
        categories.forEach(category => {
            const categoryMatch = content.match(new RegExp(`${category}:([\\s\\S]*?)(?=\\n\\n|$)`));
            if (categoryMatch) {
                const categoryContent = categoryMatch[1];
                
                const categoryDiv = document.createElement('div');
                categoryDiv.className = 'recommendation-category';
                categoryDiv.innerHTML = `
                    <h4>${category}</h4>
                    <div class="recommendation-list">
                        ${formatRecommendationItems(categoryContent)}
                    </div>
                `;
                
                recommendations.appendChild(categoryDiv);
            }
        });
    }
    
    function formatRecommendationItems(content) {
        return content
            .split('\n')
            .filter(item => item.trim().match(/^\d+\.|^-/)) // Match lines starting with number and dot or dash
            .map(item => `
                <div class="recommendation-item">
                    <p>${item.trim()}</p>
                </div>
            `)
            .join('');
    }
    
    function displayDoppelgangers(content) {
        // Clear previous doppelgangers
        doppelgangers.innerHTML = '';
        
        // Format content for display
        const doppelgangerItems = content
            .split('\n')
            .filter(item => item.trim())
            .map(item => {
                const itemText = item.trim();
                if (itemText.match(/^\d+\.|^-/)) {
                    const parts = itemText.replace(/^\d+\.|^-/, '').trim().split(':');
                    if (parts.length > 1) {
                        const name = parts[0].trim();
                        const description = parts.slice(1).join(':').trim();
                        
                        return `
                            <div class="doppelganger-item">
                                <h4>${name}</h4>
                                <p>${description}</p>
                            </div>
                        `;
                    }
                }
                return '';
            })
            .join('');
        
        doppelgangers.innerHTML = doppelgangerItems;
    }
    
    function toggleVoice() {
        if (isVoiceActive) {
            stopVoice();
        } else {
            startVoice();
        }
    }
    
    function startVoice() {
        socket.emit('start_voice');
    }
    
    function stopVoice() {
        socket.emit('stop_voice');
    }
    
    function updateVoiceUI(isActive) {
        isVoiceActive = isActive;
        voiceToggle.classList.toggle('active', isActive);
        voiceIndicator.classList.toggle('listening', isActive);
        voiceToggle.querySelector('.voice-status').textContent = isActive ? 'Stop Voice' : 'Start Voice';
    }
    
    // Socket.IO Event Handlers
    socket.on('connect', () => {
        console.log('Connected to server');
    });
    
    socket.on('response', (data) => {
        if (data.voice_input) {
            // Add the transcribed voice input to chat
            addMessageToChat('user', data.voice_input);
        }
        
        if (data.is_complete && data.mbti_result) {
            // Test is complete, show results
            addMessageToChat('bot', 'Great! Your test is now complete. Here are your results...');
            showResults(data.message);
            
            // Stop voice input when test is complete
            if (isVoiceActive) {
                stopVoice();
            }
        } else {
            // Regular message, add to chat
            addMessageToChat('bot', data.message);
            
            // Re-enable input
            setInputState(true);
        }
    });
    
    socket.on('voice_status', (data) => {
        if (data.status === 'started') {
            updateVoiceUI(true);
        } else if (data.status === 'stopped' || data.status === 'error') {
            updateVoiceUI(false);
        }
    });
    
    socket.on('connect_error', (error) => {
        console.error('Connection Error:', error);
        addMessageToChat('bot', 'Sorry, there was an error connecting to the server. Please refresh the page and try again.');
        updateVoiceUI(false);
    });
    
    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        addMessageToChat('bot', 'Disconnected from server. Please refresh the page to reconnect.');
        updateVoiceUI(false);
    });
});