import React, { useState, useEffect, useRef } from 'react';
import './ChatBotWindow.css';
import ChatBot from "react-chatbot-kit";
import {BiSolidUser} from 'react-icons/bi'
import axios from 'axios';
import { FaArrowCircleRight } from 'react-icons/fa'; // Import the send icon
import {RiRobot2Fill} from 'react-icons/ri'
import {BsFillSendFill} from 'react-icons/bs'
const ChatBotWindow = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState([
    { text: "Welcome to the MindMate. How can I assist you?", user: 'bot' },
  ]);
  const [inputText, setInputText] = useState('');
  const messagesContainerRef = useRef(null);

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSendMessage = async () => {
    if (inputText.trim() !== '') {
      // Send user message to the chatbot API
      const userMessage = inputText;
      setInputText('');

      try {
        const response = await axios.post('http://localhost:5000/chat', {
          message: userMessage,
        });
        // Add user and chatbot responses to the messages
        const botResponse = response.data.response;
        
        const newMessages = [...messages, { text: userMessage, user: 'user' }, { text: botResponse, user: 'bot' }];
        
        setMessages(newMessages);

        // Scroll to the bottom of the message container
        if (messagesContainerRef.current) {
          messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
        }
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  };

  const handleInputKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  }

  // Scroll to the bottom of the message container when messages change
  useEffect(() => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return isOpen ? (
    <div className="chat-bot-window">
      <div className="chat-messages" ref={messagesContainerRef}>
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.user === 'user' ? 'user' : 'bot'}`}
          >
            {message.user === 'user' ? (
              <>
              <div className="user-message">{message.text}</div>
                <div className="sender-icon">
                  {/* Use a React icon for the sender */}
                  <BiSolidUser />
                </div>
                
              </>
            ) : (
              <>
                <div className="receiver-icon">
                  {/* Use a React icon for the receiver */}
                  <RiRobot2Fill />
                </div>
                <div className="bot-message">{message.text}</div>
              </>
            )}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          placeholder="Type your message..."
          value={inputText}
          onChange={handleInputChange}
          onKeyPress={handleInputKeyPress}
        />
        <button onClick={handleSendMessage}>
          {/* Use a React icon for the send button */}
          <BsFillSendFill />
        </button>
      </div>
    </div>
  ) : null;
};

export default ChatBotWindow;
