# chat/consumers.py
import json
from asgiref.sync import async_to_sync # New, Added for handling ChannelLayer 

from channels.generic.websocket import WebsocketConsumer

class ChatConsumer( WebsocketConsumer ):
    '''When a User posts a Message, A JavaScript Function will transmit the message over Websocket to a ChatConsumer Instance
    
        The ChatConsumer will Receive that message and Forward it to the Group corresponding to that ROOM_NAME.
        Every ChatConsumer in the same Group (and thus in the same room) will then recieve the message from the GROUP and forward it over WEBSOCKET back to our Javascript Function, where it will be appended back to the Chat-LOG.
    '''
    def connect(self):
        '''Connect the WS
        
                self.scope: Obtains the 'room_name' param fro the URL route in chat/routing.py that opened the WS connection to the consumer. 
                            Every Consumer has a <scope> that contains information about its connection, including in particular ANY 
                            positional ARGs fro the URL route and the currently <AUTHENTICATED> user
        

                > self.room_group_name = 'chat_%s' % self.room_name:
                                                                    Constucts a <Channels Group name> directly from the user-specified room-name, without any quoting or escaping.
                                                                    <Group names> may only contain letters, digits, hyphens, and periods. Therefore this example code will FAIL on room names that have other Characters.

                > async_to_sync(self.channel_layer.group_add)( ... ):
                                                                    - Joins a Group.
                                                                    - The  'async_to_sync( ... )' wrapper is REQUIRED becuase ChatConsumer is a SYNCHRONOUS WebSocketConsumer but it is calling an ASYNC <channel_layer.method>. (* All channel layer methods are ASYNC)
                                                                    - Group names are restricted to ASCII alphanumerics, hyphens, and periods ONLY. 
                                                                        * Since this code constructs a <Group.Name> directly from the <room_name>, it will FAIL if the room name contains any characters contain any characters that aren't valid in the <group_name>
                > self.accept():
                                - Accepts the WS connection
                                - If you do not call 'self.accept()' within the 'ChatConumser.connect()' method, then the connection will be REJECTED and CLOSED.
                                    * For example: You may want to REJECT a connection if the Requesting User was not Authorized to perform the requested action (Django Auth)
                                - It is recommended that self.accept() be called as the *LAST* operation in ChatConsumer.connect() if you choose to 'accept()' connecition.
                > async_to_sync( self.channel_layer.GROUP_DISCARD )( ... ):
                                                                        - Leaves a Group

                > async_to_sync( self.channel_layer.GROUP_SEND )( ... ):
                                                                        - Sends an Event to a GROUP.
                                                                        - An <EVENT> has a special 'type' key that corresponds to the Name of the Method that should be invoked on CONSUMERS that recieve the EVENT-Type. 
        
        '''
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join the Room Group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept() # Accept the incoming Socket connection

    def disconnect(self, close_code):
        # Leave Room Group on Disconnect:
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        '''Receive the Chat-Message From WebSocket:'''
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        '''Receive Message From Room Group'''
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         print("\n\nChat COnsumer Connecting...")
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         # print("\nRecieving Message...")
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         print(f'Recieved Message:\t {message} ')

#         self.send(text_data=json.dumps({
#             'message': message
#         }))
