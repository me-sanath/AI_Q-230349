import React from 'react';

function AskQuestionPage() {
  return (
    <div className="ask-question-page">
      <h1>Ask a Question</h1>
      <form>
        <label>
          Title:
          <input type="text" placeholder="Enter your question title" />
        </label>
        <br />
        <label>
          Details:
          <textarea placeholder="Describe your question in detail"></textarea>
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default AskQuestionPage;
