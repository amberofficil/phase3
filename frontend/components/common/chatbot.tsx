
'use client';
import { useState } from 'react';

interface Message {
  sender: 'user' | 'ai';
  text: string;
}

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');

  const user_id = 'amber@example.com'; // Replace with logged-in user

  const handleSend = async () => {
    if (!input.trim()) return;

    // Show user message
    setMessages(prev => [...prev, { sender: 'user', text: input }]);

    try {
      // Call backend API
      const res = await fetch('http://172.25.112.1:8000/api/v1/ai/todo/process', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ user_id, user_input: input }),
});

      const data = await res.json();

      // Show AI response
      setMessages(prev => [
        ...prev,
        { sender: 'ai', text: data.message || 'AI did not respond' },
      ]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { sender: 'ai', text: 'Server error, please try again!' },
      ]);
    }

    setInput('');
  };

  return (
    <>
      {/* Chatbot Icon */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          style={{
            position: 'fixed',
            bottom: 20,
            right: 20,
            background: '#000',
            color: '#fff',
            borderRadius: '50%',
            width: 50,
            height: 50,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            zIndex: 1000,
          }}
        >
          💬
        </button>
      )}

      {/* Chatbox */}
      {isOpen && (
        <div
          style={{
            position: 'fixed',
            bottom: 20,
            right: 20,
            width: 320,
            height: 400,
            border: '1px solid #ccc',
            borderRadius: 8,
            background: '#fff',
            display: 'flex',
            flexDirection: 'column',
            zIndex: 1000,
          }}
        >
          {/* Header with close button */}
          <div
            style={{
              padding: 10,
              borderBottom: '1px solid #eee',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              fontWeight: 'bold',
            }}
          >
            Todo Chatbot
            <button onClick={() => setIsOpen(false)}>✖️</button>
          </div>

          {/* Messages */}
          <div style={{ padding: 10, flex: 1, overflowY: 'auto' }}>
            {messages.length === 0
              ? 'Welcome! Type a command like "add buy groceries".'
              : messages.map((msg, i) => (
                  <div
                    key={i}
                    style={{
                      textAlign: msg.sender === 'user' ? 'right' : 'left',
                      margin: '4px 0',
                      background: msg.sender === 'user' ? '#DCF8C6' : '#F1F0F0',
                      padding: '6px 10px',
                      borderRadius: '8px',
                      maxWidth: '80%',
                    }}
                  >
                    <b>{msg.sender === 'user' ? 'You' : 'AI'}:</b> {msg.text}
                  </div>
                ))}
          </div>

          {/* Input */}
          <div style={{ display: 'flex', borderTop: '1px solid #eee' }}>
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSend()}
              placeholder="Type a message..."
              style={{ flex: 1, padding: 8, border: 'none', outline: 'none' }}
            />
            <button
              onClick={handleSend}
              style={{
                padding: '0 12px',
                background: '#000',
                color: '#fff',
                border: 'none',
                cursor: 'pointer',
              }}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
}

