import React from 'react';
import { createRoot } from 'react-dom/client';
import WelcomeCard from './components/WelcomeCard.jsx';
import './style.css';

function App() {
  return (
    <main className="page">
      <WelcomeCard name="Ada" role="React components" isOnline={true} />
      <WelcomeCard name="" />
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
