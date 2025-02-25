# Basics

### Enabling Messaging

Before sending or receiving messages, you must enable messaging on your local participant’s side:

```python
await room.messaging.enable()
```

Optionally, you can provide a callback `on_stream_accept` if you also plan to use “streaming” messages. For basic text/binary messages, you can ignore streams.

### Sending a Message

To send a message, use:

```python
await room.messaging.send_message(
    to = some_remote_participant,
    type = "my_message_type",      # Arbitrary label for your message
    message = { "key": "value" },  # Arbitrary dict to represent your payload
    attachment = b"some data"      # (optional) Byte payload
)
```

Where:

- `participant` is a `Participant` (specifically a `RemoteParticipant` on the other end) to whom you are sending the message.
- `type` is a string label to help classify or route the message.
- `message` is a JSON-serializable dictionary included as part of your message.
- `attachment` is an optional bytes object for binary data.

### Receiving Messages

When you enable messaging, you can register an event handler for the `"message"` event to receive custom messages:

```python
def on_message(message: RoomMessage):
    print(f"Received message from {message.from_participant_id}")
    print(f"Message type: {message.type}")
    print(f"Message content (JSON): {message.message}")
    if message.attachment:
        print(f"Binary payload: {message.attachment}")

room.messaging.on("message", on_message)
```

The `RoomMessage` object includes:

- `from_participant_id`: the sender’s participant ID (string).
- `type`: the message type (e.g., `"my_message_type"`).
- `message`: a Python dictionary with the JSON payload.
- `attachment`: the raw bytes if a file or other binary data was attached.

### Broadcasting Messages

To send a message to **all** participants, call:

```python
await room.messaging.broadcast_message(
    type="my_broadcast_type",
    message={"hello": "everyone"},
    attachment=None
)
```

All participants with messaging enabled will receive this broadcast.

---

## Example With Two Agents

Below is a complete example showing **two separate participants** (we’ll call them “Alice” and “Bob”) who each connect to the same room. Then Alice sends a message to Bob, Bob replies, and each one prints the message.

> **Note**: This example starts both participants in the same Python script for demo purposes. In practice, each participant (or agent) can be in a separate process or even on a different machine, as long as they connect to the same room.

+++ Python
:::code source="/examples/python/messaging-send.py" :::
+++

### How This Example Works

1. **Two connections**: We create two separate `RoomClient` connections, one for “Alice” and one for “Bob.” Each uses a unique `ParticipantToken` but shares the same `room_name`.
2. **Enable messaging**: We call `room.messaging.enable()` in both so each can send and receive custom messages.
3. **Send message**: From “Alice”’s room, we look up “Bob” in `room.messaging.remote_participants`, then call `send_message(...)`.
4. **Receive message**: “Bob” receives the message in the event callback:

   ```python
   def on_message(message):
       print(f"[Bob] Received a message from {message.from_participant_id}: {message.message}")
   ```
   
5. **Reply**: “Bob” then sends a message back to “Alice” by looking up her participant object in his local list.

6. **Tear down**: We eventually close both connections.

---

## Additional Notes

- If you want to **broadcast** a message to all participants in the room, use:
  
  ```python
  await room.messaging.broadcast_message(
      type="global_announcement",
      message={"text":"Hello everyone!"}
  )
  ```

- You can also send **binary data** in the `attachment` argument if you need to transfer files or other binary payloads.
- For advanced use-cases such as streaming large data chunk-by-chunk, refer to the `MessageStreamReader` / `MessageStreamWriter` APIs (`create_stream`, etc.).

With this, you have all the essential building blocks to exchange messages (text or binary) among participants or agents using the MeshAgent client API.