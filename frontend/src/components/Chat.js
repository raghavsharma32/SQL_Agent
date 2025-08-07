// import React, { useState, useRef, useEffect } from 'react';
// import axios from 'axios';
// import { FaUser, FaRobot } from 'react-icons/fa';

// const Chat = () => {
//   const [messages, setMessages] = useState([
//     { sender: 'bot', text: 'Hello! How can I assist you today?', timestamp: Date.now() }
//   ]);
//   const [inputValue, setInputValue] = useState('');
//   const [isSending, setIsSending] = useState(false);
//   const chatRef = useRef(null);
//   const inputRef = useRef(null);

//   useEffect(() => {
//     if (chatRef.current) {
//       chatRef.current.scrollTop = chatRef.current.scrollHeight;
//     }
//   }, [messages, isSending]);

//   useEffect(() => {
//     inputRef.current.focus();
//   }, []);

//   const sendMessage = async () => {
//     if (inputValue.trim() === '' || isSending) return;
//     const userMessage = { sender: 'user', text: inputValue, timestamp: Date.now() };
//     setMessages(prev => [...prev, userMessage]);
//     setInputValue('');
//     setIsSending(true);

//     try {
//       const response = await axios.post('http://localhost:8000/prompt', { prompt: inputValue });
//       const result = response.data.response; // Updated to match backend response
//       const botResponse = {
//         sender: 'bot',
//         text: result.success ? (result.data || 'No data returned') : `Error: ${result.error}`,
//         timestamp: Date.now()
//       };
//       setMessages(prev => [...prev, botResponse]);
//     } catch (error) {
//       const errorMessage = {
//         sender: 'system',
//         text: `Error: ${error.response?.data?.error || error.message}`,
//         timestamp: Date.now()
//       };
//       setMessages(prev => [...prev, errorMessage]);
//     } finally {
//       setIsSending(false);
//       inputRef.current.focus();
//     }
//   };

//   return (
//     <div className="chat-container">
//       <div className="header">AI Assistant</div>
//       <div className="chat-window" ref={chatRef}>
//         {messages.map((msg) => (
//           <Message key={msg.timestamp} message={msg} />
//         ))}
//         {isSending && (
//           <div className="typing-indicator">
//             <span></span><span></span><span></span>
//           </div>
//         )}
//       </div>
//       <div className="input-area">
//         <input
//           type="text"
//           value={inputValue}
//           onChange={e => setInputValue(e.target.value)}
//           onKeyPress={e => e.key === 'Enter' && sendMessage()}
//           placeholder="Type your message..."
//           disabled={isSending}
//           ref={inputRef}
//         />
//         <button onClick={sendMessage} disabled={isSending}>Send</button>
//       </div>
//     </div>
//   );
// };

// const Message = ({ message }) => {
//   const { sender, text, timestamp } = message;
//   const time = new Date(timestamp).toLocaleTimeString();

//   return (
//     <div className={`message ${sender}`}>
//       {sender === 'user' ? <FaUser className="avatar" /> : <FaRobot className="avatar" />}
//       <div className="message-content">
//         <p>{text}</p>
//         <span className="timestamp">{time}</span>
//       </div>
//     </div>
//   );
// };

// export default Chat;


import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { FaUser, FaRobot } from 'react-icons/fa';

const Chat = () => {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! How can I assist you today?', timestamp: Date.now() }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isSending, setIsSending] = useState(false);
  const chatRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const sendMessage = async () => {
    if (!inputValue.trim() || isSending) return;

    const userMessage = {
      sender: 'user',
      text: inputValue.trim(),
      timestamp: Date.now()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsSending(true);

    try {
      const res = await axios.post('http://localhost:8000/prompt', {
        prompt: inputValue.trim()
      });

      const result = res.data?.response;
      const botText = result?.success
        ? (result.data || 'No response provided.')
        : `Error: ${result?.error || 'Unknown error.'}`;

      const botMessage = {
        sender: 'bot',
        text: botText,
        timestamp: Date.now()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      const errorMessage = {
        sender: 'system',
        text: `Request failed: ${err.response?.data?.error || err.message}`,
        timestamp: Date.now()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsSending(false);
      inputRef.current?.focus();
    }
  };

  return (
    <div className="chat-container">
      <div className="header">AI Assistant</div>

      <div className="chat-window" ref={chatRef}>
        {messages.map((msg, index) => (
          <Message key={index} message={msg} />
        ))}
        {isSending && (
          <div className="typing-indicator">
            <span></span><span></span><span></span>
          </div>
        )}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="Type your message..."
          disabled={isSending}
          ref={inputRef}
        />
        <button onClick={sendMessage} disabled={isSending}>
          {isSending ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

const Message = ({ message }) => {
  const { sender, text, timestamp } = message;
  const time = new Date(timestamp).toLocaleTimeString();

  return (
    <div className={`message ${sender}`}>
      {sender === 'user' ? <FaUser className="avatar" /> : <FaRobot className="avatar" />}
      <div className="message-content">
        <p>{text}</p>
        <span className="timestamp">{time}</span>
      </div>
    </div>
  );
};

export default Chat;
