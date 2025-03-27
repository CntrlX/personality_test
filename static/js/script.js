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
        // For debugging - log the raw result content
        console.log("Raw result content:", resultContent);
        
        // Hide chat container and show results
        document.querySelector('.chat-container').classList.add('hidden');
        resultContainer.classList.remove('hidden');
        
        // Extract MBTI type and title
        const mbtiTypeMatch = resultContent.match(/🎉 Your MBTI Personality Type: (\w{4})/);
        if (mbtiTypeMatch) {
            const mbtiType = mbtiTypeMatch[1];
            const mbtiTypeTitle = getMbtiTypeTitle(mbtiType);
            mbtiTitle.innerHTML = `${mbtiType}: ${mbtiTypeTitle}`;
            console.log("Found MBTI type:", mbtiType);
        } else {
            console.error("Failed to match MBTI type");
            // Fallback to display something
            mbtiTitle.innerHTML = "Your Personality Type";
        }
        
        // Extract overview - updated regex to be more flexible
        const overviewMatch = resultContent.match(/📝\s*Overview([\s\S]*?)(?=🔥\s*Roast|🎯)/i);
        if (overviewMatch) {
            mbtiOverview.innerHTML = formatBotMessage(overviewMatch[1]);
            console.log("Found overview");
        } else {
            console.error("Failed to match overview section");
            // Fallback for overview
            const descriptionMatch = resultContent.match(/🎉.*?(\w{4})\s*([\s\S]*?)(?=📝|🔥|🎯)/i);
            if (descriptionMatch) {
                mbtiOverview.innerHTML = formatBotMessage(descriptionMatch[2]);
                console.log("Found description as fallback for overview");
            } else {
                mbtiOverview.innerHTML = "<p>No overview available</p>";
            }
        }
        
        // Extract roast - updated regex to be more flexible
        const roastMatch = resultContent.match(/🔥\s*Roast([\s\S]*?)(?=🎯)/i);
        if (roastMatch) {
            roastContainer.innerHTML = formatBotMessage(roastMatch[1]);
            console.log("Found roast");
        } else {
            console.error("Failed to match roast section");
            roastContainer.innerHTML = "<p>No roast available</p>";
        }
        
        // Extract recommendations - updated regex to be more flexible
        const recommendationsMatch = resultContent.match(/🎯[\s\S]*?recommendations([\s\S]*?)(?=Who are your celebrity|Remember|Career|Relationship)/i);
        if (recommendationsMatch) {
            displayRecommendations(recommendationsMatch[1]);
            console.log("Found recommendations");
        } else {
            console.error("Failed to match recommendations section");
            recommendations.innerHTML = "<p>No recommendations available</p>";
        }
        
        // Extract doppelgangers - updated regex to be more flexible
        const doppelgangersMatch = resultContent.match(/Who are your celebrity doppelgangers\?([\s\S]*?)(?=Relationship|Career|Remember)/i);
        if (doppelgangersMatch) {
            displayDoppelgangers(doppelgangersMatch[1]);
            console.log("Found doppelgangers");
        } else {
            console.error("Failed to match doppelgangers section");
            doppelgangers.innerHTML = "<p>No celebrity doppelgangers available</p>";
        }
        
        // Extract relationship insights - updated regex to be more flexible
        const relationshipMatch = resultContent.match(/Relationship([\s\S]*?)(?=Career|Remember)/i);
        if (relationshipMatch) {
            relationshipInsights.innerHTML = formatBotMessage(relationshipMatch[1]);
            console.log("Found relationship insights");
        } else {
            console.error("Failed to match relationship section");
            relationshipInsights.innerHTML = "<p>No relationship insights available</p>";
        }
        
        // Extract career insights - updated regex to be more flexible
        const careerMatch = resultContent.match(/Career insights?([\s\S]*?)(?=Remember|$)/i);
        if (careerMatch) {
            careerInsights.innerHTML = formatBotMessage(careerMatch[1]);
            console.log("Found career insights");
        } else {
            console.error("Failed to match career section");
            careerInsights.innerHTML = "<p>No career insights available</p>";
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
        console.log("Raw recommendations content:", content);
        // Clear previous recommendations
        recommendations.innerHTML = '';
        
        // If content is empty or doesn't contain categories, display a message
        if (!content || !content.trim()) {
            recommendations.innerHTML = "<p>No recommendations available</p>";
            return;
        }
        
        // Create categories
        const categories = ['Music', 'Books', 'Movies'];
        let anyCategories = false;
        
        categories.forEach(category => {
            // More flexible regex to match category sections
            const categoryMatch = content.match(new RegExp(`${category}:?([\\s\\S]*?)(?=(?:Music|Books|Movies):?|$)`, 'i'));
            if (categoryMatch && categoryMatch[1].trim()) {
                anyCategories = true;
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
        
        // If no categories were found, display the content directly
        if (!anyCategories) {
            recommendations.innerHTML = `<div class="recommendation-content">${formatBotMessage(content)}</div>`;
        }
    }
    
    function formatRecommendationItems(content) {
        const items = content
            .split('\n')
            .filter(item => item.trim())
            .map(item => {
                const trimmedItem = item.trim();
                // More flexible pattern to match recommendations
                if (trimmedItem.match(/^\d+[\.\):]|^-|^\*/)) {
                    return `
                        <div class="recommendation-item">
                            <p>${trimmedItem}</p>
                        </div>
                    `;
                }
                return '';
            })
            .join('');
            
        return items || `<p>${content.trim()}</p>`;
    }
    
    function displayDoppelgangers(content) {
        console.log("Raw doppelgangers content:", content);
        // Clear previous doppelgangers
        doppelgangers.innerHTML = '';
        
        // If content is empty, display a message
        if (!content || !content.trim()) {
            doppelgangers.innerHTML = "<p>No celebrity doppelgangers available</p>";
            return;
        }
        
        // Split by lines and try to extract doppelgangers
        const lines = content.split('\n').filter(line => line.trim());
        
        // If there are no lines, display the raw content
        if (lines.length === 0) {
            doppelgangers.innerHTML = formatBotMessage(content);
            return;
        }
        
        // Process each line
        const doppelgangerItems = lines
            .map(line => {
                const trimmedLine = line.trim();
                // Try to match a numbered or bulleted item
                const itemMatch = trimmedLine.match(/^(\d+[\.\):]|[-*])\s*(.*)/);
                if (itemMatch) {
                    // Try to split into name and description
                    const itemContent = itemMatch[2];
                    const parts = itemContent.split(/:\s*(.+)/);
                    
                    if (parts.length > 1) {
                        // We have a name and description
                        return `
                            <div class="doppelganger-item">
                                <h4>${parts[0].trim()}</h4>
                                <p>${parts[1].trim()}</p>
                            </div>
                        `;
                    } else {
                        // No colon separation, treat whole line as content
                        return `
                            <div class="doppelganger-item">
                                <p>${itemContent}</p>
                            </div>
                        `;
                    }
                } else if (trimmedLine) {
                    // Not a list item but has content
                    return `
                        <div class="doppelganger-item">
                            <p>${trimmedLine}</p>
                        </div>
                    `;
                }
                return '';
            })
            .join('');
            
        doppelgangers.innerHTML = doppelgangerItems || formatBotMessage(content);
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
        console.log('Socket response received:', data);
        
        if (data.voice_input) {
            // Add the transcribed voice input to chat
            addMessageToChat('user', data.voice_input);
        }
        
        if (data.is_complete && data.mbti_result) {
            // Test is complete, show results
            addMessageToChat('bot', 'Great! Your test is now complete. Here are your results...');
            
            // Log the raw message for debugging
            console.log('Complete MBTI result received:', {
                mbtiType: data.mbti_result,
                messageLength: data.message ? data.message.length : 0,
                messagePreview: data.message ? data.message.substring(0, 100) + '...' : 'No message'
            });
            
            // Process the results
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