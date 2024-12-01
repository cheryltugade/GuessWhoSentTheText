import React, { useState } from 'react';
import { getMessages } from '../services/api';

function GameOverPage({ startGuessing, gameData, score, handleRestart }) {
    const [playAgain, setPlayAgain] = useState(false);
    const { userName, contactName } = gameData;
    
    const handleStartGame = () => {
      setPlayAgain(true)
    };
  
    const handlePlayWithSameNum = async() => {
      let newMessages = await getMessages();
      let updatedGameData = {originalTexts: newMessages, userName: userName, contactName: contactName}
      startGuessing(updatedGameData)
    };
  
    const handlePlayWithNewNum = () => {
      setPlayAgain(false)
      handleRestart()
    };

    return (
      <div className="App">
        <header className="App-header">
          {!playAgain && (<><p className="App-game-over-text">GAME OVER</p>
          <p className='App-score'>Score: <span className='App-score-value'>{score}</span></p>
          <button className="App-button" onClick={handleStartGame}>PLAY AGAIN?</button></>)}
          {playAgain && (
            <>
              <button className="App-button" onClick={handlePlayWithSameNum}>PLAY AGAIN WITH SAME PHONE NO.?</button>
              <button className="App-button" onClick={handlePlayWithNewNum}>PLAY WITH NEW PHONE NO.?</button>
              </>
            )}
        </header>
      </div>
    );
  }

    export default GameOverPage;