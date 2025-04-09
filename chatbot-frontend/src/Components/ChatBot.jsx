import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Chatbot.css'; 
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';       // Dark theme
import { prism } from 'react-syntax-highlighter/dist/esm/styles/prism';         // Light theme

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [userId, setUserId] = useState('');
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    // Generate a unique user ID if not present
    let storedId = localStorage.getItem('user_id');
    if (!storedId) {
      storedId = `user-${Date.now()}`;
      localStorage.setItem('user_id', storedId);
    }
    setUserId(storedId);
  }, []);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/chat', {
        user_id: userId,
        user_input: input
      });

      const botReply = { sender: 'bot', text: response.data.response };
      setMessages(prev => [...prev, botReply]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  const fetchHistory = async () => {
    if (!userId) {
      alert("User ID is required to fetch history.");
      return;
    }
  
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/chat/history/${userId}`);
      const history = response.data.history;
  
      setMessages(history);  // history is already in [{sender, text}] format
    } catch (error) {
      console.error("Error fetching chat history:", error);
      alert("Failed to fetch chat history.");
    } finally {
      setLoading(false);
    }
  };
  

  const clearConversation = () => {
    const confirmClear = window.confirm("Are you sure you want to clear the conversation?");
    if (confirmClear) {
      setMessages([]); // Clears messages from the state
    }
  };
  
  const toggleDarkMode = () => {
    setDarkMode(prev => !prev);
  };

  return (
    <div className={`chat-container ${darkMode ? 'dark' : ''}`}>
      <header>
        <h2>LangGraph Chatbot</h2>
        <div className="controls">
          <button onClick={toggleDarkMode}>
            {darkMode ? ' Light Mode' : ' Dark Mode'}
          </button>
          <button onClick={fetchHistory}> Chat History</button>
          <button onClick={clearConversation}> Clear Chat</button>
        </div>
      </header>

<div className="chat-box">
  {messages.map((msg, i) => (
    <div key={i} className={`message ${msg.sender}`}>
      <img
        src={msg.sender === 'user' ? '/user.png' : '/bot.png'}
        alt={msg.sender}
        className="avatar"
      />
      <div className="markdown">
      <ReactMarkdown
  children={msg.text}
  components={{
    a: ({ node, ...props }) => (
      <a {...props} target="_blank" rel="noopener noreferrer" />
    ),
    code({ node, inline, className, children, ...props }) {
      const match = /language-(\w+)/.exec(className || '');
      return !inline && match ? (
        <SyntaxHighlighter
          style={darkMode ? oneDark : prism}
          language={match[1]}
          PreTag="div"
          {...props}
        >
          {String(children).replace(/\n$/, '')}
        </SyntaxHighlighter>
      ) : (
        <code className={className} {...props}>
          {children}
        </code>
      );
    },
  }}
/>
 </div>
    </div>
  ))}
  {loading && <div className="message bot"><p>Typing...</p></div>}
</div>


      <div className="input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyDown={e => e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend} disabled={loading}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;