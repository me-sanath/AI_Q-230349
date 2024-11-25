import React from 'react';

function QuestionsPage() {
  return (
    <div className="questions-page">
      <h1>All Questions</h1>
      <ul>
        <li>
          <p>Question 1: How to debug React errors effectively?</p>
          <button>Answer</button>
        </li>
        <li>
          <p>Question 2: Best practices for optimizing Python code?</p>
          <button>Answer</button>
        </li>
        <li>
          <p>Question 3: How to integrate APIs in a Node.js project?</p>
          <button>Answer</button>
        </li>
      </ul>
    </div>
  );
}

export default QuestionsPage;
