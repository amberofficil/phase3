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

  const handleSend = async () => {
    if (!input.trim()) return;

    // show user message
    setMessages(prev => [...prev, { sender: 'user', text: input }]);

    try {
      const res = await fetch(
  `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/ai/todo/process`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: 'amber@example.com', // logged-in user
      user_input: input,            // user message
    }),
  }
);


      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();

      setMessages(prev => [
        ...prev,
        { sender: 'ai', text: data.message || 'AI did not respond' },
      ]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [
        ...prev,
        { sender: 'ai', text: 'Server error, please try again!' },
      ]);
    }

    setInput('');
  };

  return (
    <>
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
            cursor: 'pointer',
            zIndex: 1000,
          }}
        >
          💬
        </button>
      )}

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
          <div
            style={{
              padding: 10,
              borderBottom: '1px solid #eee',
              display: 'flex',
              justifyContent: 'space-between',
              fontWeight: 'bold',
            }}
          >
            Todo Chatbot
            <button onClick={() => setIsOpen(false)}>✖️</button>
          </div>

          <div style={{ padding: 10, flex: 1, overflowY: 'auto' }}>
            {messages.length === 0
              ? 'Welcome! Type a command like "add buy groceries".'
              : messages.map((msg, i) => (
                  <div
                    key={i}
                    style={{
                      textAlign: msg.sender === 'user' ? 'right' : 'left',
                      margin: '6px 0',
                      background:
                        msg.sender === 'user' ? '#DCF8C6' : '#F1F0F0',
                      padding: '6px 10px',
                      borderRadius: 8,
                      maxWidth: '80%',
                    }}
                  >
                    <b>{msg.sender === 'user' ? 'You' : 'AI'}:</b> {msg.text}
                  </div>
                ))}
          </div>

          <div style={{ display: 'flex', borderTop: '1px solid #eee' }}>
            <input
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
