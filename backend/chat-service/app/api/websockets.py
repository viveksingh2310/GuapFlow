from fastapi import APIRouter, WebSocket, WebSocketDisconnect,Depends
from typing import Dict, List
from app.schemas.schemas import CurrentUser
from app.utils.security import websocket_get_current_user
from sqlalchemy.orm import Session
from app.services.services import validate_conversation,validate_message,create_message
from app.db.db import get_db
ws_router = APIRouter()
# print("heloooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
rooms: Dict[str, List[WebSocket]] = {}

@ws_router.websocket("/ws/{conversation_id}")
async def chat_socket(websocket: WebSocket,conversation_id: str,db: Session = Depends(get_db),):
    current_user = await websocket_get_current_user(websocket)
    conversation = await validate_conversation(db,conversation_id,current_user.user_id)
    print('here is the user id and the consultant is of the specified conversation that you have requested to us')
    print(conversation.user_id)
    consultant_id=conversation.consultant_id
    messages=await validate_message(db,conversation_id)
    print('here are the messages from the given conversation id that i have')
    for msg in messages:
        print(msg.content+' from '+msg.sender_type)
    await websocket.accept()
    if conversation_id not in rooms:
        rooms[conversation_id] = []
    rooms[conversation_id].append(websocket)
    try:
        while True:
            message = await websocket.receive_json()
            message["type"]="user"
            if message["sender_id"]==str(consultant_id):
                message["type"]="consultant"
            result=await create_message(conversation_id,message["sender_id"], message["type"],message["content"],db)
            for client in rooms[conversation_id]:
                await client.send_json(message)

    except WebSocketDisconnect:
        rooms[conversation_id].remove(websocket)
        # print('here is the data in the rooms, this is just to check that the converation id is removed succefully or not ')
        # print(rooms)
