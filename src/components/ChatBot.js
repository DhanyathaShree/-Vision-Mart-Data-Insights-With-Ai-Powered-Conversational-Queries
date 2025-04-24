import React, { useState } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import '../styles/ChatBot.css';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const ChatBot = () => {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      content: {
        title: "Welcome to Vision Mart!",
        text: "I'm here to help you make your work easier and faster. Not a techie? No problem! I'm here to assist you with your tasks by providing useful insights. And if you're a new joiner, I've got you covered! Any small or embarrassing doubt you have, just ask me, and I'll get it clarified.",
        examples: [
          "List the top-performing states by sales",
          "Which segment has the highest discounts?",
          "Which cities have the highest sales?"
        ]
      }
    }
  ]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim() === '' || isProcessing) return;

    // Add user message to the chat
    setMessages([...messages, { type: 'user', content: input }]);
    const userQuery = input;
    setInput('');
    setIsProcessing(true);

    try {
      // Send query to the backend
      const response = await fetch('http://127.0.0.1:3000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userQuery })
      });

      // Parse the response
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'An error occurred while processing your request.');
      }

      // Add bot response to the chat
      setMessages(prev => [...prev, {
        type: 'bot',
        content: {
          text: data.response.text,
          chartData: data.response.chart_data
        }
      }]);
    } catch (error) {
      console.error("Error details:", error);
      setMessages(prev => [...prev, {
        type: 'bot',
        content: { text: `I encountered an error: ${error.message}. Please try again.` }
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleExampleClick = (example) => {
    setInput(example);
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <div className="logo">Vision Mart</div>
        <div className="user-info">Hello, saleemployee</div>
      </div>

      <div className="messages-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.type}`}>
            {message.type === 'bot' && message.content.title && (
              <h2>{message.content.title}</h2>
            )}
            <p>{message.type === 'bot' ? message.content.text : message.content}</p>
            {message.type === 'bot' && message.content.examples && (
              <div className="examples">
                {message.content.examples.map((example, i) => (
                  <button
                    key={i}
                    className="example-button"
                    onClick={() => handleExampleClick(example)}
                  >
                    → {example}
                  </button>
                ))}
              </div>
            )}
            {message.type === 'bot' && message.content.chartData && (
              <div className="chart-container">
                <Bar
                  data={{
                    labels: message.content.chartData.x,
                    datasets: [{
                      label: message.content.chartData.title,
                      data: message.content.chartData.y,
                      backgroundColor: 'rgba(75,192,192,0.6)',
                    }]
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                  }}
                />
              </div>
            )}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="input-container">
        <button type="button" className="attach-button" disabled={isProcessing}>+</button>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Send a message..."
          className="message-input"
          disabled={isProcessing}
        />
        <button type="submit" className="send-button" disabled={isProcessing}>
          {isProcessing ? '...' : '➤'}
        </button>
      </form>
    </div>
  );
};

export default ChatBot;