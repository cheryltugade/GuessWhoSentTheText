'''
This file is a Flask API used to communicate game and message data
between the React FE and the iMessageFetcher BE.
'''

import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from imessage_fetcher import cur_game, get_20_messages

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
logging.basicConfig(level=logging.INFO)

'''
This endpoint takes in a phone number, user name, and contact name from the FE
and updates the game with those values in the BE.
'''
@app.route('/api/update_game', methods=['PUT'])
def update_game():
    try:
        request_data = request.json
        
        if not all(key in request_data for key in ("phone_number", "user_name", "contact_name")):
            return jsonify({"error": "Missing required fields"}), 400

        phone_number = request_data["phone_number"]
        user_name = request_data["user_name"]
        contact_name = request_data["contact_name"]

        cur_game.update_game(phone_number, user_name, contact_name)
        app.logger.info(f"Succesfully updated game with phone number {phone_number}, user name {user_name}, contact name {contact_name}.")
        
        return jsonify({"message": "Game updated successfully!"}), 200

    except Exception as e:
        app.logger.error(f"Failed to update game: {str(e)}")
        return jsonify({"error": str(e)}), 500

'''
This endpoint gets 20 random text message from the BE to send to the FE.
'''
@app.route('/api/messages', methods=['GET'])
def get_messages():
    try:
        messages = get_20_messages()
        app.logger.info(f"Successfully returned {len(messages)} messages: {messages}")
        return jsonify(messages), 200

    except Exception as e:
        app.logger.error(f"Failed to return messages: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)