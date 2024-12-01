import React, { useState } from 'react';
import TextMessageGuess from '../Components/TextMessageGuess';

function GuessingPage({gameData, gameOver}) {
    const { originalTexts, userName, contactName } = gameData;

    // States related to text messages
    const [curTextIndex, setCurTextIndex] = useState(0);

    // States related to score
    const [numCorrect, setNumCorrect] = useState(0)
    const [numCompleted, setNumCompleted] = useState(0)

    // States related to option selection
    const [hasBeenGuessed, setHasBeenGuessed] = useState(false)
    const [correctlySelected, setCorrectlySelected] = useState(false)

    // States related to buttons
    const [userButtonColor, setUserButtonColor] = useState('white');
    const [contactButtonColor, setContactButtonColor] = useState('white');
  
    // You can only go to the next text if you have already made a guess.
    const handleNextText = () => {
      if (hasBeenGuessed) {
        if (curTextIndex === originalTexts.length - 1) {
          gameOver(score)  
        } else {
          // Go to the next text
          setCurTextIndex(curTextIndex + 1);

          // Reset all states
          setUserButtonColor('white');
          setContactButtonColor('white');
          setHasBeenGuessed(false)
          setCorrectlySelected(false)
        }
      }
    };

    // You cannot select another guess if you have already guessed correctly.
    const handleGuessSelected = (guess) => {
        if (!correctlySelected) {
          // Only update the completed value if a guess has not yet been made.  
          if (!hasBeenGuessed) {
            setNumCompleted(numCompleted + 1)
          }

          let textSender = originalTexts[curTextIndex]['sender']
          if (textSender === guess) {
            if (guess === userName) {
                setUserButtonColor('green')
            } else if (guess === contactName) {
                setContactButtonColor('green')
            }
            
            // Only update the correct value if a guess has not yet been made.
            if (!hasBeenGuessed) {
              setNumCorrect(numCorrect + 1)
            }

            setCorrectlySelected(true)
          } else if (textSender !== guess) {
            if (guess === userName) {
                setUserButtonColor('#ff3a3a')
            } else if (guess === contactName) {
                setContactButtonColor('#ff3a3a')
            }
          }

          // Update hasBeenGuessed to True
          setHasBeenGuessed(true)
        }
      };
  
    let score;
    if (numCompleted === 0) {
      score = '-'
    } else {
      score = (numCorrect / numCompleted * 100).toFixed(2) + '%'
    }
  
    return (
      <div className="App">
        <header className="App-header">
          <TextMessageGuess text={originalTexts[curTextIndex]['text']} />
          <div class="App-button-container">
            <button
                className="App-sender-button"
                onClick={() => handleGuessSelected(userName)}
                style={{ backgroundColor: userButtonColor }}
            >
                {userName}
            </button>
            <button
                className="App-sender-button"
                onClick={() => handleGuessSelected(contactName)}
                style={{ backgroundColor: contactButtonColor }}
            >
                {contactName}
            </button>
          </div>
          <button className="App-button" onClick={handleNextText}>NEXT</button>
          <p className="App-score">Completed: <span className='App-score-value'>{numCompleted}</span> | Score: <span className='App-score-value'>{score}</span></p>
        </header>
      </div>
    );
  }

  export default GuessingPage;