import React from 'react';
import ChatBotWindow from './ChatBotWindow';

const ChatBotApp = () => {

  return (
    <div className="chat-bot-app">
      <h1>MindMate</h1>
      <p style={{ color: 'red' }}>
        Please note that MindMate-Mental Health ChatBot is a trained model and not a specialist in mental health.
      </p>
      <ChatBotWindow isOpen={true}   />
    </div>
  );
};

export default ChatBotApp;
