'''
This file fetches iMessage texts exchanged between a user and a phone number
by querying Library/Messages/chat.db.
'''
import re
import sqlite3
import os
import random

DB_PATH = f"/Users/{os.getlogin()}/Library/Messages/chat.db"

'''
This function fetches the 1000 most recent text messages exchanged between
the user and a given phone number.

This function is only called when a new phone number is inputted by the user.
'''
def fetch_all_messages(phone_number):
    if phone_number == '':
        raise ValueError("No phone number has been provided.")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ROWID FROM handle WHERE id = ?", (phone_number,))
    handles = cursor.fetchall()

    if not handles:
        raise RuntimeError("No text messages have been sent between you and the phone number.")

    handle_ids = [handle[0] for handle in handles]
    handle_ids_placeholder = ', '.join(['?'] * len(handle_ids))

    # Query for 1000 most recent messages sent to or from the phone number
    # where the text is not empty and it is not a reaction/other message type
    cursor.execute(f"""
        SELECT attributedBody, is_from_me FROM message
        JOIN handle ON handle.ROWID = message.handle_id
        WHERE (
            handle.ROWID IN ({handle_ids_placeholder})
            OR message.handle_id IN ({handle_ids_placeholder})
        )
        AND attributedBody is NOT NULL
        AND associated_message_type = 0
        ORDER BY date DESC
        LIMIT 1000
    """, handle_ids + handle_ids)

    messages = cursor.fetchall()

    if len(messages) < 20:
        raise RuntimeError("Not enough (less than 20) text messages have been sent between you and this phone number.")

    conn.close()

    return messages

'''
This function returns a list of num_messages length of valid random unique messages given an array all_messages.
'''
def select_random_messages(all_messages, num_messages):
    if num_messages == 0:
        return []
    
    message_set = set()
    attempts = 0

    while len(message_set) < num_messages and attempts < len(all_messages) * 2:
        message_sample = random.sample(all_messages, 1)[0]
        attributed_body = message_sample[0]
        text = parse_attributed_body(attributed_body)

        if is_valid_text(text) and message_sample not in message_set:
            message_set.add(message_sample)
        attempts += 1

    return list(message_set)[:num_messages]
            
'''
This function parses the attributed_body property of a message in chat.db.
This code was taken from the following GitHub repo: https://github.com/my-other-github-account/imessage_tools/
'''
def parse_attributed_body(attributed_body):
    attributed_body = attributed_body.decode('utf-8', errors='replace')

    if "NSNumber" in str(attributed_body):
        attributed_body = str(attributed_body).split("NSNumber")[0]
        if "NSString" in attributed_body:
            attributed_body = str(attributed_body).split("NSString")[1]
            if "NSDictionary" in attributed_body:
                attributed_body = str(attributed_body).split("NSDictionary")[0]
                attributed_body = attributed_body[6:-12]
                text = attributed_body
    
    return text

'''
This function parses raw messages from chat.db into a list of maps with properties "text" and "sender".
'''
def parse_messages(raw_messages):
    messages = []
    for attributed_body, is_from_me in raw_messages:
        sender = cur_game.user_name if is_from_me else cur_game.contact_name
        
        text = parse_attributed_body(attributed_body)

        if is_valid_text(text):
            messages.append({"text": text, "sender": sender})

    return messages

def is_valid_text(text):
    if text and re.search(r'\w', text) and not re.fullmatch(r'(yes|ok|okay|yeah|hi|hello|oh|no)', text, re.IGNORECASE):
        return True
    return False

'''
This function returns 20 random parsed messages from cur_game.all_messages.
'''
def get_20_messages():
    all_messages = cur_game.all_messages
    raw_messages_sample = select_random_messages(all_messages, 20)
    messages = parse_messages(raw_messages_sample)
    return messages

'''
This class is for Message objects with properties text and sender.
'''
class Message:
    def __init__(self, text, sender):
        self.text = text
        self.sender = sender

'''
This class is for Game objects with properties phone_number, user_name, contact_name, and all_messages.
'''
class Game:
    def __init__(self):
        self.phone_number = ''
        self.user_name = ''
        self.contact_name = ''
        self.all_messages = []
    
    def update_game(self, phone_number, user_name, contact_name):
        self.phone_number = phone_number
        self.user_name = user_name
        self.contact_name = contact_name
        self.all_messages = fetch_all_messages(phone_number)

cur_game = Game()