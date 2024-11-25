import React from 'react';

function HomePage() {
  return (
    <div className="homepage">
      <h1>Welcome back, Sanath!!</h1>
      <p>Discover solutions and assist others for all your technical queries.</p>
      <div className="stats">
        <div>
          <h3>Analytics</h3>
          <p>Questions Asked: 20</p>
          <p>Answers Submitted: 10</p>
        </div>
        <div>
          <h3>Reputation</h3>
          <p>76</p>
        </div>
      </div>
      <h2>Recommended Questions:</h2>
      <ul>
        <li>What’s the most frustrating bug you’ve encountered in Python?</li>
        <li>How do you balance academic projects with skill-building?</li>
        <li>What skills are most important for a job in tech?</li>
      </ul>
    </div>
  );
}

export default HomePage;
