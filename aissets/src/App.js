import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import QuestionsPage from './pages/QuestionsPage';
import AskQuestionPage from './pages/AskQuestionPage';
import SummaryPage from './pages/SummaryPage';

function App() {
  return (
    <Router>
      <div className="app">
        <nav>
          <Link to="/">Home</Link>
          <Link to="/questions">Questions</Link>
          <Link to="/ask">Ask Question</Link>
          <Link to="/summary">Summary</Link>
        </nav>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/questions" element={<QuestionsPage />} />
          <Route path="/ask" element={<AskQuestionPage />} />
          <Route path="/summary" element={<SummaryPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
