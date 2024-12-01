/**
 * This file has the main app router
 */
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import './App.css';
import GuessingPage from './Pages/GuessingPage.js';
import InputPage from './Pages/InputPage.js';
import GameOverPage from './Pages/GameOverPage.js';

/**
 * This function renders the starting page.
 *  */ 
function StartPage() {
  const navigate = useNavigate();

  const handleStartGame = () => {
    navigate('/game');
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="App-logo">Guess who sent the text...?</div>
        <button className="App-button" onClick={handleStartGame}>START GAME</button>
      </header>
    </div>
  );
}

/**
 * This function renders most of the game including the page asking for user input,
 * guessing pages, and the game over page.
 */
function Game() {
  const [curPage, setCurPage] = useState('inputPage');
  const [gameData, setGameData] = useState({});
  const [score, setScore] = useState('-');

  const startGuessing = (data) => {
    setGameData(data);
    setCurPage('guessingPage');
  };

  const handleGameOver = (score) => {
    setScore(score);
    setCurPage('gameOver')
  }

  const handleRestart = () => {
    setCurPage('inputPage');
  }

  const renderPage = () => {
    switch (curPage) {
      case 'inputPage':
        return <InputPage startGuessing={startGuessing} />;
      case 'guessingPage':
        return <GuessingPage gameData={gameData} gameOver={handleGameOver}/>;
      case 'gameOver':
        return <GameOverPage startGuessing={startGuessing} gameData={gameData} score={score} handleRestart={handleRestart}/>;
      default:
        return <InputPage />;
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        {renderPage()}
      </header>
    </div>
  );
}

/**
 * This function is used solely for testing purposes.
 */
function TestPage() {
  return (
    <div>
      <p>Test</p>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<StartPage />} />
        <Route path="/game" element={<Game />} />
        <Route path="/testpage" element={<TestPage />} />
      </Routes>
    </Router>
  );
}

export default App;
