from highrise import BaseBot
from highrise.models import SessionMetadata, User, Position
from highrise import __main__
from asyncio import run as arun


class Bot(BaseBot):
    
    async def on_start(self, session_metadata: SessionMetadata):
        print("hi im alive?")
    
    async def on_user_join(self, user: User) -> None:
        print(f"{user.username} a rejoint la salle")
        await self.highrise.chat(f"  {user.username} Abonnez vous à @rioota_sayen")
        
    async def on_user_move(self, user: User, pos: Position) -> None:
        print(pos)
    
    # **Usage:** `/tp <@user> <location> `
    # ```py
    async def on_whisper(self, user: User, message: str) -> None:
        if message.lstrip().startswith('/tp'):  # change the command name here
            if user.username.lower() in ["botrboy"]:  # to add specific users, make sure its lowercase "ihsein" and not "iHsein"
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]  # Extract the User objects
                usernames = [user.username.lower() for user in users]  # Extract the usernames
                parts = message[1:].split()
                args = parts[1:]

                if len(args) < 2:
                    await self.highrise.send_whisper(user.id, "Usage: /tp <@username> <position>")
                    return
                elif args[0][0] != "@":
                    await self.highrise.send_whisper(user.id, f"Invalid user format. Please use '@username'.")
                    return
                elif args[0][1:].lower() not in usernames:
                    await self.highrise.send_whisper(user.id, f"{args[0][1:]} is not in the room.")
                    return

                position_name = " ".join(args[1:])
                if position_name == 'vip':
                    dest = Position(17.5, 1.0, 12.5)
                elif position_name == 'pool':
                    dest = Position(1.5, 1, 7.5)
                # if you want to add more locations, use the same method elif etc .. 
                else:
                    return await self.highrise.send_whisper(user.id, f"Unknown location")
                
                user_id = next((u.id for u in users if u.username.lower() == args[0][1:].lower()), None)
                if not user_id:
                    await self.highrise.send_whisper(user.id, f"User {args[0][1:]} not found")
                    return
                await self.highrise.teleport(user_id, dest)
                await self.highrise.send_whisper(user.id, f"Teleported {args[0][1:]} to ({dest.x}, {dest.y}, {dest.z})")
            else:
                await self.highrise.send_whisper(user.id, "You can't use this command")
        else:
            pass
    async def on_start(self, SessionMetadata: SessionMetadata) -> None:
    	await self.highrise.walk_to(Position(16.0, 0.0, 3.5))
    
    async def on_chat(self, user: User, message: str):
        print(f"{user.username} said: {message}")
    
    async def run(self, room_id, token):
        await __main__.main(self, room_id, token)


if __name__ == "__main__":
    room_id = "645199f7df9a59cf85802e88"
    token = "81fb12cbd5ae040cf72fc90fd33967ccd11706faa102e15b45e1f372d35cf6d9"
    arun(Bot().run(room_id, token))
