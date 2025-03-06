from fastapi import WebSocket, status
from fastapi.exceptions import WebSocketException
from scripts.logger import Logging
from typing import Dict
from scripts.auth import Auth
from scripts.database import Database
from models.validation_models import User

logger = Logging.getLogger()
db = Database()

class WebSocketConnection:
    def __init__(self):
        self.active_users = []


    async def ws_connect(self, websocket: WebSocket) -> User | None:
        '''Open a web socket connection and check the validity of the access token.'''
        await websocket.accept()

        data = await websocket.receive_json()

        if not data['access_token']:
            await websocket.close()
            return None
        
        try:
            user = await Auth.get_current_user(data['access_token'])
        except ValueError as e:
            logger.info(f"INVALID TOKEN BY %s:")
            raise WebSocketException(status.WS_1002_PROTOCOL_ERROR, str(e))
        
        user_details = User(user, websocket)

        self.active_users.append(user_details)
        await self.send_chat_history(websocket)

        logger.info(f"USER ADDED TO THE CONNECTION POOL. {self.active_users}")

        return user_details
    
    
    async def send_chat_history(self, websocket: WebSocket):
        'Fetch chat history from the database and send it to the user.'
        chat_history = db.get_message_history()
        try:
            await websocket.send_json(chat_history)
        except Exception as e:
            logger.warning(f"ERROR FETCHING CHAT HISTORY: {e}")

        logger.info(f"CHAT HISTORY SENT TO THE USER.")


    async def broadcast(self, current_user: User, message_details: Dict[str, str]):
        '''Broadcast the message to active users.'''
        logger.info(f"BROADCASTING MESSAGE: {message_details}")

        message_content = message_details['message']
        current_user_id = current_user.id
        sender_name = current_user.name

        db.save_message(current_user_id, message_content)

        for user in self.active_users:
            try: 
                await user.websocket_client.send_json({
                    "name": sender_name,
                    "message": message_content
                })
            except Exception as e:
                logger.warning(f"ERROR SENDING MESSAGE TO {user}: {e}")

    
    def ws_disconnect(self, current_user: User):
        '''Close the websocket connection of the user.'''
        self.active_users.remove(current_user)
        logger.info(f"USER REMOVED FROM THE CONNECTION POOL. {self.active_users}")