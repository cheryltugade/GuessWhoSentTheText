# Guess Who Sent The Text
**_NOTE: This game can only be run locally due to privacy reasons. Follow the instructions section to play this game on your local computer._**

This game fetches 20 random iMessage texts between you and a given phone number/email and displays them one by one. You have to guess who sent the text.

![gwstt](https://github.com/user-attachments/assets/7cf57348-89ac-4070-943d-ab8b12805732)

This game is most fun when played together with the person you have texted with!

## Instructions (takes <5 mins to set up) ##
**_NOTE: This game can only work if you have iMessage set up on your computer._**
1. Click on the green 'Code' button on the top right and then click 'Download ZIP' in the dropdown.
<img width="934" alt="Screenshot 2024-11-30 at 11 02 55 PM" src="https://github.com/user-attachments/assets/ae8e3df6-5a29-4b09-a9a0-8214178b0612">

2. Enable Full Disk Access for your Terminal (System Preferences < Privacy & Security < Full Disk Access < Turn it on for Terminal). This allows the game to access your text messages locally. <br /><br />It should look like this:<br /> <img width="300" alt="Screenshot 2024-11-24 at 2 21 22 AM" src="https://github.com/user-attachments/assets/b1677159-c0a7-4b93-931a-66c7c9aa33b7">

3. Open the downloaded zip file and `cd` into it on two different Terminal tabs. For example, if it's in your Downloads run `cd Downloads/GuessWhoSentTheText`.

4. Run the following on the first tab: `cd backend` followed by `python3 api.py`. Run the following on the second tab: `cd frontend` followed by `npm start`

5. The game should start running in `localhost:3000`. Happy guessing!

## Note on Privacy ##
This game does NOT store or process your data remotely. All the work is done through your local computer!
