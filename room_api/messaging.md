# Messaging

`MessagingClient` enables sending messages between participants and agents in a room, as well as handling streaming messages (`MessageStreamWriter` and `MessageStreamReader`).

---

## Overview

- **`MessagingClient`** – A high-level client that:
  - Sends and receives messages between room participants
  - Manages stream-based messages via `createStream()`
  - Tracks remote participants and their attributes
  - Can enable or disable the messaging subsystem
- **`MessageStreamChunk`** – Represents a single chunk in a stream, containing a header and optional binary data.
- **`MessageStreamWriter`** – A writer for sending streaming data (chunks) to a remote participant.
- **`MessageStreamReader`** – A reader that receives streaming data (chunks) from a remote participant.

## Example Usage

Below are some examples demonstrating how to use `MessagingClient` for basic messaging and streaming use cases.

### Basic Example: Sending and Receiving Messages

+++ Python
```python
# Suppose you already have a RoomClient instance named `room_client`
messaging_client = MessagingClient(room=room_client)

# Enable messaging (allows receiving participant and stream events)
await messaging_client.enable()

# Acquire a participant instance from somewhere; you might discover it via events
my_participant = ... # type: RemoteParticipant

# Send a simple message
await messaging_client.sendMessage({
    "to": my_participant,
    "type": "chat",
    "message": {"text": "Hello from Python!"}
})

# Broadcast a message to all participants
await messaging_client.broadcastMessage({
    "type": "announcement",
    "message": {"content": "Hello everyone!"}
})

# Disable messaging
await messaging_client.disable()
```
+++ JavaScript
```js
// Suppose you already have a RoomClient instance named `roomClient`
const messagingClient = new MessagingClient({ room: roomClient });

// Enable messaging
await messagingClient.enable();

// Acquire a participant instance from somewhere
const myParticipant = /* ...some RemoteParticipant... */;

// Send a simple message
await messagingClient.sendMessage({
  to: myParticipant,
  type: "chat",
  message: { text: "Hello from JavaScript!" },
});

// Broadcast a message
await messagingClient.broadcastMessage({
  type: "announcement",
  message: { content: "Hello everyone!" },
});

// Disable messaging
await messagingClient.disable();
```
+++ TypeScript
```ts
// Suppose you already have a RoomClient instance named `roomClient`
const messagingClient = new MessagingClient({ room: roomClient });

// Enable messaging
await messagingClient.enable();

// Acquire a participant instance from somewhere
const myParticipant: RemoteParticipant = /* ...some RemoteParticipant... */;

// Send a simple message
await messagingClient.sendMessage({
  to: myParticipant,
  type: "chat",
  message: { text: "Hello from TypeScript!" },
});

// Broadcast a message
await messagingClient.broadcastMessage({
  type: "announcement",
  message: { content: "Hello everyone!" },
});

// Disable messaging
await messagingClient.disable();
```
+++ Dart
```dart
// Suppose you already have a RoomClient instance named `roomClient`
final messagingClient = MessagingClient(room: roomClient);

// Enable messaging
await messagingClient.enable();

// Acquire a participant instance from somewhere
final myParticipant = /* ...some RemoteParticipant... */;

// Send a simple message
await messagingClient.sendMessage(
  to: myParticipant,
  type: "chat",
  message: {"text": "Hello from Dart!"},
);

// Broadcast a message
await messagingClient.broadcastMessage(
  type: "announcement",
  message: {"content": "Hello everyone!"},
);

// Disable messaging
await messagingClient.disable();
```
+++

### Example: Creating and Handling Streams

+++ Python
```python
# Create a new stream
stream_writer = await messaging_client.createStream(
    to=my_participant,
    header={"streamPurpose": "file-transfer"}
)

# Write chunks
await stream_writer.write(MessageStreamChunk(
    header={"chunkNumber": 1},
    data=b"some binary data"
))

# Close the stream
await stream_writer.close()
```
+++ JavaScript
```js
// Create a new stream
const streamWriter = await messagingClient.createStream({
  to: myParticipant,
  header: { streamPurpose: "file-transfer" },
});

// Write chunks
await streamWriter.write(
  new MessageStreamChunk({
    header: { chunkNumber: 1 },
    data: new Uint8Array([/* binary data */]),
  })
);

// Close the stream
await streamWriter.close();
```
+++ TypeScript
```ts
// Create a new stream
const streamWriter = await messagingClient.createStream({
  to: myParticipant,
  header: { streamPurpose: "file-transfer" },
});

// Write chunks
await streamWriter.write(
  new MessageStreamChunk({
    header: { chunkNumber: 1 },
    data: new Uint8Array([/* binary data */]),
  })
);

// Close the stream
await streamWriter.close();
```
+++ Dart
```dart
// Create a new stream
final streamWriter = await messagingClient.createStream(
  to: myParticipant,
  header: {"streamPurpose": "file-transfer"},
);

// Write chunks
await streamWriter.write(MessageStreamChunk(
  header: {"chunkNumber": 1},
  data: Uint8List.fromList([/* some binary data */]),
));

// Close the stream
await streamWriter.close();
```
+++

---

## Classes and Methods

### `MessagingClient`

A high-level client class for sending and receiving messages, enabling/disabling the messaging subsystem, handling participants, and managing streaming operations.

```ts
constructor({ room }: { room: RoomClient })
```
**Parameters**:
- `room` – A `RoomClient` instance through which requests and events are sent or received.

---

#### `enable(onStreamAccept?: (reader: MessageStreamReader) => void): Promise<void>`

Enables the messaging subsystem on the server. Optionally provides a callback that is triggered whenever an incoming stream is opened by a remote participant.

+++ TypeScript
```ts
await messagingClient.enable((reader) => {
  console.log("New stream opened:", reader._streamId);
});
```
+++

---

#### `disable(): Promise<void>`

Disables the messaging subsystem on the server.

+++ TypeScript
```ts
await messagingClient.disable();
```
+++

---

#### `sendMessage({ to, type, message, attachment? }): Promise<void>`

Sends a message to a specific participant, optionally including a binary `attachment`.

**Parameters**:
- `to` – The participant to receive the message.
- `type` – A string that categorizes or labels the message.
- `message` – A JSON-serializable object containing message data.
- `attachment` – (Optional) A `Uint8Array` of binary data to attach.

+++ TypeScript
```ts
await messagingClient.sendMessage({
  to: myParticipant,
  type: "chat",
  message: { text: "Hey!" },
  attachment: new Uint8Array([1,2,3]),
});
```
+++

---

#### `broadcastMessage({ type, message, attachment? }): Promise<void>`

Broadcasts a message to **all** participants in the room.

**Parameters**:
- `type` – A string that categorizes or labels the message.
- `message` – A JSON-serializable object containing message data.
- `attachment` – (Optional) A `Uint8Array` of binary data to attach.

+++ TypeScript
```ts
await messagingClient.broadcastMessage({
  type: "announcement",
  message: { title: "Server Maintenance", content: "We will be down tonight." },
});
```
+++

---

#### `createStream({ to, header }): Promise<MessageStreamWriter>`

Creates a new stream directed at a single participant. Returns a `MessageStreamWriter` once the remote participant accepts the stream.

**Parameters**:
- `to` – The participant to receive the stream.
- `header` – A JSON-serializable object describing the stream.

**Returns**  
A `Promise<MessageStreamWriter>` that resolves once the remote participant accepts the stream.

+++ TypeScript
```ts
const writer = await messagingClient.createStream({
  to: myParticipant,
  header: { purpose: "video-stream" },
});
```
+++

---

#### `remoteParticipants: Iterable<RemoteParticipant>`

Provides an iterable collection of all known remote participants. 

+++ TypeScript
```ts
for (const participant of messagingClient.remoteParticipants) {
  console.log(`Participant: ${participant.id}, role: ${participant.role}`);
}
```
+++

---

#### `dispose(): void`

Removes the `"messaging.send"` handler from the internal `Protocol` and disposes the event emitter.

```ts
messagingClient.dispose();
```

---

### `MessageStreamChunk`

Represents a chunk of data in a stream, consisting of a header and optional binary data.

```ts
constructor({ header, data }: { header: Record<string, any>; data?: Uint8Array })
```

- **`header: Record<string, any>`** – A JSON-serializable object holding metadata about the chunk (e.g., a chunk index or content type).
- **`data?: Uint8Array`** – An optional binary payload.

+++ TypeScript
```ts
const chunk = new MessageStreamChunk({
  header: { chunkIndex: 1 },
  data: new Uint8Array([0x48, 0x65, 0x6C, 0x6C, 0x6F]),
});
```
+++

---

### `MessageStreamWriter`

A writer for sending streaming data to a remote participant, created via `MessagingClient.createStream()`.

- **`write(chunk: MessageStreamChunk): Promise<void>`**  
  Sends a chunk of data in the ongoing stream.
  
- **`close(): Promise<void>`**  
  Closes the stream, signaling to the remote participant that no more chunks will be sent.

+++ TypeScript
```ts
// Example usage after acquiring a MessageStreamWriter
await streamWriter.write(
  new MessageStreamChunk({ header: { part: 1 }, data: new Uint8Array([1, 2, 3]) })
);
await streamWriter.close();
```
+++

---

### `MessageStreamReader`

A reader for consuming streaming data from a remote participant. Typically constructed internally when the remote participant invokes `createStream()` on their side and the local client `accept`s it.

- **`_controller: StreamController<MessageStreamChunk>`**  
  An internal controller for managing incoming `MessageStreamChunk` objects. In many implementations, you can iterate over `_controller.stream` (if you have such a concept) to read chunked data.

+++ TypeScript
```ts
messagingClient.enable((reader) => {
  console.log("New stream from:", reader._to.id);
  
  (async () => {
    for await (const chunk of reader._controller.stream) {
      console.log("Received chunk:", chunk.header, chunk.data);
    }
    console.log("Stream closed.");
  })();
});
```
+++

---

## Additional Notes

1. **Event Emission**  
   `MessagingClient` extends `EventEmitter<RoomMessageEvent>`. It emits events whenever messages are received or streams are opened/closed. You can listen for the `"message"` event or for custom events like `"participant_added"`, `"participant_removed"`, etc.:

   +++ TypeScript
   ```ts
   messagingClient.on("message", ({ message }) => {
     console.log("Received a message of type:", message.type);
   });

   messagingClient.on("participant_added", (evt) => {
     console.log("A new participant joined:", evt.message.message);
   });
   ```
   +++

2. **Remote Participants**  
   `MessagingClient` automatically keeps track of participants joining or leaving when the messaging subsystem is enabled. You can access them via `remoteParticipants`.

3. **Error Handling**  
   - If a request fails or the server returns an error, the underlying `RoomClient` may throw an exception.
   - Stream operations (`createStream`, `write`, etc.) may also fail if the remote participant rejects or if the connection is lost.

4. **Extensibility**  
   You can add additional features—like chunk-level encryption, compression, or custom handshake logic—by extending `MessagingClient` or by wrapping the provided stream objects (`MessageStreamWriter` / `MessageStreamReader`).

5. **Performance**  
   For large or frequent streams, consider buffering or batching chunk writes in your client logic. The streaming mechanism in `MessagingClient` is designed to handle incremental data transfer, but network considerations remain important for efficient performance.
