import TextInput from "../Components/TextInput";
import { getMessages, updateGame } from "../services/api";
import React, { useState } from 'react';


function InputPage({ startGuessing }) {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [userName, setUserName] = useState('');
  const [contactName, setContactName] = useState('');

  const handlePhoneNumberChange = (value) => {
    setPhoneNumber(value);
  };
  const handleUserNameChange = (value) => {
    setUserName(value)
  };
  const handleContactNameChange = (value) => {
    setContactName(value);
  };

  const handleSubmit = async() => {
    try {
      await updateGame(phoneNumber, userName, contactName)
    } catch (error) {
      console.error("Error when calling updateGame:", error);
      return
    }
    const originalTexts = await getMessages()
    startGuessing({originalTexts: originalTexts, userName: userName, contactName: contactName})
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="input-container">
            <p className="App-input-label-text">What's your contact's phone no. (with country code) or email in iMessage?</p>
            <TextInput onChange={handlePhoneNumberChange} placeholderText={"Ex.: +12345678910"}></TextInput>
        </div>
        <div className="input-container">
            <p className="App-input-label-text">What's your name?</p>
            <TextInput onChange={handleUserNameChange} placeholderText={"Ex.: Cheryl"}></TextInput>
        </div>
        <div className="input-container">
            <p className="App-input-label-text">What's your contact's name?</p>
            <TextInput onChange={handleContactNameChange} placeholderText={"Ex.: Orrin"}></TextInput> 
        </div>
        <button className="App-button" onClick={handleSubmit}>SUBMIT</button>
      </header>
    </div>
  );
}

export default InputPage;
