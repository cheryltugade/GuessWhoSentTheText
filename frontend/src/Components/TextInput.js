import React, { useState } from 'react';

function TextInput({ onChange, placeholderText }) {
    const [inputValue, setInputValue] = useState('');

    const handleChange = (event) => {
        const value = event.target.value;
        setInputValue(value);
        onChange(value);
    };

    return (
        <div className="input-container">
        <input
            type="text"
            className="imessage-input"
            value={inputValue}
            onChange={handleChange}
            placeholder={placeholderText}
        />
        </div>
    );
}

export default TextInput;