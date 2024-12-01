import React from 'react';

function TextMessageGuess({ text }) {
    return (
      <><p className="App-gwstt-label-text">Guess who sent the text...?</p>
      <div className="App-text-message">
        {text}
      </div></>
    );
  }

export default TextMessageGuess;