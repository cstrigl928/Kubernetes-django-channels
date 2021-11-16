
import json
from channels.generic.websocket import AsyncWebsocketConsumer
# Routes:
# rooms/
class GameRoomConsumer( AsyncWebsocketConsumer ):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        print("USER: ", str(self.user))
        print("Room-Name: ", str(self.room_name))
        print("Group-Name: ", str(self.room_group_name))
        # Channel_layer instructs THIS.GROUP to use
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name  # Contains A pointer to the Ch. Layer instance and Ch. Name that will reach Consumer (i.e. we Created a New Group)
        )

        self.accept()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'tester_message',
                'tester': 'Hello World!',
            }
        )

    async def tester_message(self, event):
        '''IMPORTANT!
            > This method corresponds to the K,V async - await from self.connect.channel_layer.group_send( 'type'='MY_FUNC_NAME" )
            > We've now received the ws and are collecting the data send in the message and sending to templates/myapp/HTML - via JSON
        '''
        event_data_serializid = event['tester']

        # This is the <k,v> we send to our TEMPLATEs. E.G. Similar to our CONTEXT in Views
        await self.send( text_data=json.dumps({ 
            'tester': event_data_serializid
        }))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            # What Group we want to Discard (whatever is in the WS.Connect):
            self.room_group_name,
            self.channel_name
        )
        # self.disconnect()



    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads( text_data )
        message = text_data_json['message']
        username = text_data_json['username']

        await self.channel_layer.group_send( 
            self.room_group_name,
            {
                'type' : 'chatroom_message',
                'message' : message,
                'username' : username, 
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({ 
            'message': message,
            'username' : username, 
        }))

    # async def