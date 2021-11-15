# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("\n\nChat COnsumer Connecting...")
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # print("\nRecieving Message...")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(f'Recieved Message:\t {message} ')

        self.send(text_data=json.dumps({
            'message': message
        }))