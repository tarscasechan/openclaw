import React from 'react';

export default function WelcomeCard({ name, role, isOnline = false }) {
  const displayName = name?.trim() || 'friend';
  const lesson = role || 'React components';

  return (
    <article className="card">
      <h2>Hello, {displayName}!</h2>
      <p>You are learning {lesson}.</p>
      <p aria-label="status">
        {isOnline ? '🟢 Ready to build' : '⚪ Taking it step by step'}
      </p>
    </article>
  );
}
