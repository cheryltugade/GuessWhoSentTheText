import random
import unittest
import sys
import os
from unittest.mock import call, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from imessage_fetcher import cur_game, get_20_messages, parse_messages, select_random_messages, fetch_all_messages, is_valid_text

# Replace with two different phone numbers that you have exchanged 20+ messages with
valid_phone_num = "+12345678910"
valid_phone_num2 = "+12345678910"
# Replace with a phone number that you have exchanged less than 20 messages with
less_than_twenty_messages_phone_num = "+12345678910"
invalid_phone_num = "invalid_phone_num"
user_name = 'Cheryl'
contact_name = 'Orrin'

MOCK_100_RAW_MESSAGES = []
MOCK_20_RAW_MESSAGES = []
MOCK_20_PARSED_MESSAGES = []

'''
This function checks whether an input of parsed messages are valid, returning False otherwise.
'''
def parsed_messages_are_valid(messages, user_name=user_name, contact_name=contact_name):
    for message in messages:
        text = message["text"]
        sender = message["sender"]
        if not (isinstance(text, str) or text != "" or not is_valid_text(text) or sender not in [user_name, contact_name]):
            return False
    return True
'''
This class checks that the select_random_messages function works correctly.
'''
class TestSelectRandomMessages(unittest.TestCase):
    def test_select_20_random_messages(self):
        all_messages = fetch_all_messages(valid_phone_num)

        # Call select_random_messages 5 times to check randomization works consistently
        for _ in range(5):
            messages = select_random_messages(all_messages, 20)

            # Check that select_random_messages returns exactly 20 messages 
            self.assertEqual(20, len(messages))

            # Check that messages does not contain any duplicates
            message_set = set()
            for message in messages:
                self.assertNotIn(message, message_set)
                message_set.add(message)

            # Check that all messages can be parsed and are valid
            parsed_messages = parse_messages(messages)
            self.assertEqual(20, len(parsed_messages))
    
    # TODO: Add test that has invalid messages
    # def test_select(self):
    #     #
        
    def test_select_0_random_messages(self):
        all_messages = fetch_all_messages(valid_phone_num)
        messages = select_random_messages(all_messages, 0)

        # Check that select_random_messages returns exactly 0 messages 
        self.assertEqual(0, len(messages))

'''
This class checks that the fetch_all_messages function works correctly.
'''
class TestFetchAllMessages(unittest.TestCase):
    def test_invalid_phone_num(self):
        with self.assertRaises(Exception) as context:
            _ = fetch_all_messages(invalid_phone_num)
        
        self.assertIn("No text messages have been sent between you and the phone number.", str(context.exception))
    
    def test_no_phone_num(self):
        with self.assertRaises(Exception) as context:
            _ = fetch_all_messages('')
        
        self.assertIn("No phone number has been provided.", str(context.exception))

    def test_not_enough_messages_with_phone_num(self):
        with self.assertRaises(Exception) as context:
            _ = fetch_all_messages(less_than_twenty_messages_phone_num)
        
        self.assertIn("Not enough (less than 20) text messages have been sent between you and this phone number.", str(context.exception))

    def test_fetch_all_messages_with_valid_phone_num(self):
        all_messages = fetch_all_messages(valid_phone_num)
        num_messages = len(all_messages)

        # Check that num_messages is >= 20 but <= 1000
        self.assertGreaterEqual(num_messages, 20)
        self.assertLessEqual(num_messages, 1000)

        # Check that data is formatted corectly
        for attributed_body, is_from_me in all_messages:
            # Check that attributed_body is a binary object
            self.assertIsInstance(attributed_body, (bytes, bytearray))
            # Check that is_from_me is equal to 0 or 1
            self.assertIn(is_from_me, [0, 1])

'''
This class checks that the parse_messages function works correctly.
'''        
class TestParseMessages(unittest.TestCase):
    def test_parse_messages(self):
        cur_game.update_game(valid_phone_num, user_name, contact_name)

        all_messages = fetch_all_messages(valid_phone_num)
        raw_messages_sample = random.sample(all_messages, 20)
        parsed_messages = parse_messages(raw_messages_sample)

        # Check that messages are valid
        self.assertTrue(parsed_messages_are_valid(parsed_messages))

'''
This class checks that the is_valid_text function works correctly.
'''
class TestIsValidText(unittest.TestCase):
    def test_valid_texts(self):
        self.assertTrue(is_valid_text("This is a valid text."))
        self.assertTrue(is_valid_text("Hello world!"))
        self.assertTrue(is_valid_text("123"))
        self.assertTrue(is_valid_text("Welcome123"))
    
    def test_none_text(self):
        self.assertFalse(is_valid_text(None))
    
    def test_invalid_contains_no_word_characters(self):
        self.assertFalse(is_valid_text(""))
        self.assertFalse(is_valid_text("   "))
        self.assertFalse(is_valid_text("!!!"))
        self.assertFalse(is_valid_text("###"))
        self.assertFalse(is_valid_text("..."))
        self.assertFalse(is_valid_text("?!@"))
        self.assertFalse(is_valid_text("\t\n"))
    
    def test_invalid_text_restricted_words_lowercase(self):
        self.assertFalse(is_valid_text("yes"))
        self.assertFalse(is_valid_text("ok"))
        self.assertFalse(is_valid_text("okay"))
        self.assertFalse(is_valid_text("yeah"))
        self.assertFalse(is_valid_text("hi"))
        self.assertFalse(is_valid_text("hello"))
        self.assertFalse(is_valid_text("oh"))
        self.assertFalse(is_valid_text("yes"))
        self.assertFalse(is_valid_text("NO"))
    
    def test_invalid_text_restricted_words_uppercase(self):
        self.assertFalse(is_valid_text("YES"))
        self.assertFalse(is_valid_text("OK"))
        self.assertFalse(is_valid_text("OKAY"))
        self.assertFalse(is_valid_text("YEAH"))
        self.assertFalse(is_valid_text("HI"))
        self.assertFalse(is_valid_text("HELLO"))
        self.assertFalse(is_valid_text("OH"))
        self.assertFalse(is_valid_text("NO"))
    
'''
This class checks that the get_20_messages function works correctly.
'''
class TestGet20Messages(unittest.TestCase):

    @patch('imessage_fetcher.select_random_messages')
    @patch('imessage_fetcher.parse_messages')
    def test_get_20_messages(self, mock_parse_messages, mock_select_random_messages):
        mock_messages = [
            {"attributed_body": bytes("Hello!", "utf-8"), "is_from_me": 1},
            {"attributed_body": bytes("How are you?", "utf-8"), "is_from_me": 0},
        ] * 10
        mock_select_random_messages.return_value = mock_messages

        mock_parsed_messages = [
            {"text": "Hello!", "sender": user_name},
            {"text": "How are you?", "sender": contact_name},
        ] * 10
        mock_parse_messages.return_value = mock_parsed_messages

        messages = get_20_messages()

        # Check that select_random_messages was called with correct arguments
        mock_select_random_messages.assert_called_once_with(cur_game.all_messages, 20)

        # Check that parse_messages was called with correct arguments
        mock_parse_messages.assert_called_once_with(mock_messages)

        # Check that the messages returned are the output of parse_messages
        self.assertEqual(messages, mock_parsed_messages)

        # Check that messages output is of length 20 and messages are valid
        self.assertEqual(len(messages), 20)
        self.assertTrue(parsed_messages_are_valid(messages))

class TestUpdateGameAndGet20Messages(unittest.TestCase):
    def test_update_game_and_get_20_messages(self):
        cur_game.update_game(valid_phone_num, user_name, contact_name)
        all_messages = fetch_all_messages(valid_phone_num)

        # Check that update_game updated properties correctly
        self.assertEqual(valid_phone_num, cur_game.phone_number)
        self.assertEqual(user_name, cur_game.user_name)
        self.assertEqual(contact_name, cur_game.contact_name)
        self.assertEqual(all_messages, cur_game.all_messages)

        messages = get_20_messages()
        self.assertEqual(len(messages), 20)
        self.assertTrue(parsed_messages_are_valid(messages))
    
    def test_update_game_with_changing_inputs(self):
        cur_game.update_game(valid_phone_num, user_name, contact_name)
        all_messages = fetch_all_messages(valid_phone_num)

        # Check that update_game updated properties correctly
        self.assertEqual(valid_phone_num, cur_game.phone_number)
        self.assertEqual(user_name, cur_game.user_name)
        self.assertEqual(contact_name, cur_game.contact_name)
        self.assertEqual(all_messages, cur_game.all_messages)

        messages = get_20_messages()
        self.assertEqual(len(messages), 20)
        self.assertTrue(parsed_messages_are_valid(messages))

        # Update game with different inputs
        cur_game.update_game(valid_phone_num2, "Jack", "John")
        all_messages = fetch_all_messages(valid_phone_num2)

        # Check that update_game updated properties correctly
        self.assertEqual(valid_phone_num2, cur_game.phone_number)
        self.assertEqual("Jack", cur_game.user_name)
        self.assertEqual("John", cur_game.contact_name)
        self.assertEqual(all_messages, cur_game.all_messages)

        messages = get_20_messages()
        self.assertEqual(len(messages), 20)
        self.assertTrue(parsed_messages_are_valid(messages, "Jack", "John"))
    
    @patch('imessage_fetcher.fetch_all_messages')
    def test_fetch_messages_only_called_once_for_update_game(self, mock_fetch_all_messages):
        cur_game.update_game(valid_phone_num, user_name, contact_name)

        # Check that update_game calls fetch_all_messages once
        mock_fetch_all_messages.assert_called_once_with(valid_phone_num)

        # Check that calling get_20_messages multiple times never calls fetch_all_messages
        for _ in range(5):
            get_20_messages()
            mock_fetch_all_messages.assert_called_once_with(valid_phone_num)

        # Check that calling update_game again calls fetch_all_messages again
        cur_game.update_game(valid_phone_num2, "Jack", "John")
        self.assertEqual(mock_fetch_all_messages.call_count, 2)
        self.assertEqual(mock_fetch_all_messages.call_args_list, [call(valid_phone_num), call(valid_phone_num2)])

        # Check that calling get_20_messages multiple times never calls fetch_all_messages
        for _ in range(5):
            get_20_messages()
            self.assertEqual(mock_fetch_all_messages.call_count, 2)

if __name__ == '__main__':
    unittest.main()