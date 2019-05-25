from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    GROUP = 'chat'
    MAX_REPEATED_MESSAGES = 3

    message = ''
    amount = 0

    async def connect(self):
        self.username = self.scope["user"].login
        await self.channel_layer.group_add(self.GROUP, self.channel_name)
        await self.channel_layer.group_send(
            self.GROUP,
            {
                'type': 'connected',
                'username': self.username,
            }
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.GROUP, self.channel_name)

    async def receive(self, text_data):
        message = json.loads(text_data)['message']
        if (self.message == message):
            self.amount += 1
        else:
            self.message = message
            self.amount = 0
        if (self.amount < self.MAX_REPEATED_MESSAGES):
            await self.channel_layer.group_send(
                self.GROUP,
                {
                    'type': 'chat_message',
                    'username': self.username,
                    'message': message
                }
            )
        else:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'error': 'You can not sent the same message more than ' +
                         str(self.MAX_REPEATED_MESSAGES) +
                         ' times in a row.'
            }))


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'username': event['username'],
            'message': event['message']
        }))

    async def connected(self, event):
        await self.send(text_data=json.dumps({
            'type': 'connected',
            'username': event['username'],
        }))
