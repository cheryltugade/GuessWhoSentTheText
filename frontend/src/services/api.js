const API_URL = 'http://127.0.0.1:5000/api';

/**
 * This function calls the API update_game PUT endpoint to update the game's
 * phoneNumber, userName, and contactName.
 * 
 * @param {*} phoneNumber 
 * @param {*} userName 
 * @param {*} contactName 
 * @returns 
 */
export const updateGame = async (phoneNumber, userName, contactName) => {
    if (phoneNumber == "" || userName == "" || contactName == "") {
        alert("All fields are required. Please ensure that all fields are filled out before submitting.");
        throw new Error("Missing required fields");
    }
    try {
        const response = await fetch(`${API_URL}/update_game`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              phone_number: phoneNumber,
              user_name: userName,
              contact_name: contactName
            }),
        });
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }
        const result = await response.json();
        console.log('Update game successful:', result);  
        return result;
    } catch (error) {
        console.error('Update game failed:', error);
        alert(
            "Unable to retrieve messages. Please check the following:\n\n" +
            "1. Ensure the phone number or email is correct.\n" +
            "2. If you are using a phone number, ensure that it includes the country code (e.g. +1).\n" +
            "3. Ensure that you have have exchanged at least 20 messages with this contact, otherwise there are not enough messages to play."
        );        
        throw error;
    }
};

/**
 * This function calls the API messages GET endpoint to get 20 random messsages
 * that have been exchanged between the user and the contact.
 * 
 * @returns 
 */
export const getMessages = async () => {
    try {
        const response = await fetch(`${API_URL}/messages`);
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }
        const result = await response.json();
        console.log('Get messages successful', result)
        return result;
    } catch (error) {
        console.error('Get messsages failed:', error);
        throw error;
    }
};