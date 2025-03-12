# Define a unique room name
room_name = 'my-room'
participant_name = 'my-participant'

# Create the WebSocket channel 
channel = websocket_protocol(participant_name=participant_name, room_name=room_name)

# Initialize the communication protocol
protocol = Protocol(channel)

# Instantiate a new RoomClient for interacting with the room
room = RoomClient(protocol)

# Connect to the room
await room.start()
