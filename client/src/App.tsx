import './App.css';
import { useEffect, useRef, useState } from 'react';
import ProfileForm from './ProfileForm';
import Authentication from './Authentication';

// App creation
function App() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<string[]>([]);
  const chatBoxRef = useRef<HTMLDivElement>(null);
  const [signedInUser, setSignedInUser] = useState<string | null>(null);
  const [previousInput, setPreviousInput] = useState<string>('');
  const [previousOutput, setPreviousOutput] = useState<string>('');

  const handleSignIn = (username: string) => {
    setSignedInUser(username);
  };

  const handleSignOut = () => {
    setSignedInUser(null);
  };

  const handleSendMessage = () => {
    if (message.trim() === '' || !signedInUser) return;
    setMessages([...messages, `You: ${message}`]);
    setMessage('');

    // Make actual call to FastAPI backend
    fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_name: signedInUser,
        input_text: message,
        bot_name: "Max",     // Default or dynamic name
        style: "friendly",   // Can make this user-selectable later
        category: "general",
        previous_input: previousInput,
        previous_output: previousOutput
      })
    })
    .then((response) => response.json())
    .then((data) => {
      setMessages((prevMessages) => [...prevMessages, `Wingman: ${data.response}`]);
      setPreviousInput(message);
      setPreviousOutput(data.response);
    })
    .catch((error) => {
      console.error("Error talking to Wingman:", error);
      setMessages((prevMessages) => [...prevMessages, `Wingman: Oops, I had a moment. Try again later?`]);
    });
  };
  
  // When printing to output, scrolling the output text window automatically
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);


  // Actual web app container
  return (
    <div className="app-container">
      <header>
        <h1>Introly</h1>
        <p>Your AI-powered social wingman.</p>
        {signedInUser && (
          <p className="signed-in">Signed in as: <strong>{signedInUser}</strong></p>
        )}
        <Authentication
          signedInUser={signedInUser}
          onSignIn={handleSignIn}
          onSignOut={handleSignOut}
        />
        {!signedInUser && <ProfileForm />}
      </header>
      <main>
        <div className="chat-container">
          <div className="chat-box" ref={chatBoxRef}>
            {messages.map((msg, idx) => (
              <div key={idx} className="chat-message">
                {msg}
              </div>
            ))}
          </div>
          <div className="chat-input-area">
            <input
              type="text"
              placeholder={signedInUser ? "Type your message..." : "Sign in to chat..."}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              disabled={!signedInUser}
            />
            <button onClick={handleSendMessage} disabled={!signedInUser}>Send</button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
