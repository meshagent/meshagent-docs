# Queues

This module provides a client for interacting with server-managed queues. It contains two primary exports:

---

## Overview

- **`Queue`** – A simple class that represents a queue instance, holding its name and current size.
- **`QueuesClient`** – A high-level client that sends requests through a provided `RoomClient` to list, open, drain, close, send messages to, and receive messages from queues.

## API Methods

Below is an example of how you might use the `QueuesClient` in your code:

+++ Python
```python
# List existing Queues
queues = await room.queues.list()
print("Queues:", queues)

# Open a Queues
await room.queues.open("my-queue")

# Send a messages
await room.queues.send("my-queue", {"payload": "Hello World!"})

# Receive a message
message = await room.queues.receive("my-queue")
print("Received message:", message)

# Drain a queue
await room.queues.drain("my-queue")

# Close the queue
await room.queues.close("my-queue")
```
+++ JavaScript
```js
// List existing queues
const queues = await room.queues.list();
console.log("Queues:", queues);

// Open a queue
await room.queues.open("my-queue");

// Send a message
await room.queues.send("my-queue", { payload: "Hello World!" });

// Receive a message
const message = await room.queues.receive("my-queue");
console.log("Received message:", message);

// Drain a queue
await room.queues.drain("my-queue");

// Close the queue
await room.queues.close("my-queue");
```
+++ TypeScript
```ts
// List existing queues
const queues = await room.queues.list();
console.log("Queues:", queues);

// Open a queue
await room.queues.open("my-queue");

// Send a message
await room.queues.send("my-queue", { payload: "Hello World!" });

// Receive a message
const message = await room.queues.receive("my-queue");
console.log("Received message:", message);

// Drain a queue
await room.queues.drain("my-queue");

// Close the queue
await room.queues.close("my-queue");
```
+++ Dart
```dart
// List existing Queues
final queues = await room.queues.list();
print("Queues: $queues");

// Open a queue
await room.queues.open("my-queue");

// Send a message
await room.queues.send("my-queue", {"payload": "Hello World!"});

// Receive a message
final message = await room.queues.receive("my-queue");
print("Received message: $message");

// Drain a queue
await room.queues.drain("my-queue");

// Close the queue
await room.queues.close("my-queue");
```
+++

---

### `Queue`

A basic representation of a queue, holding a name and its current size.

+++ Python
```python
queue = Queue(name="my-queue", size=0)
```
+++ JavaScript
```js
const queue = new Queue({ name: "my-queue", size: 0 });
```
+++ TypeScript
```ts
const queue = new Queue({ name: "my-queue", size: 0 });
```
+++ Dart
```dart
final queue = Queue(name: "my-queue", size: 0);
```
+++

- **`name: string`**  
  The name of the queue.
- **`size: number`**  
  The size (or length) of the queue at the time of retrieval.


---

### `QueuesClient`

The `QueuesClient` is responsible for sending requests through a `RoomClient` to perform various operations on queues.

- **`room: RoomClient`**  
  An instance of `RoomClient`, which handles the low-level communication with the server or service.


#### `list()`

+++ Python
```python
queues = await room.queues.list()
```
+++ JavaScript
```js
const queues = await room.queues.list();
```
+++ TypeScript
```ts
const queues = await room.queues.list();
```
+++ Dart
```dart
final queues = await room.queues.list();
```
+++

- **Returns**  
  An array of [`Queue`](#queue) objects containing the name and size of each queue found on the server.


#### `open(name: string)`

+++ Python
```python
await room.queues.open("my-queue")
```
+++ JavaScript
```js
await room.queues.open("my-queue");
```
+++ TypeScript
```ts
await room.queues.open("my-queue");
```
+++ Dart
```dart
await room.queues.open("my-queue");
```
+++

- **Parameters**:
  - `name` – The name of the queue to open.
- **Description**  
  Sends a request to the server to open a queue with the specified name. If the queue already exists and is closed, it will be reopened. If it does not exist, it will be created and opened.


#### `drain(name: string)`

+++ Python
```python
await room.queues.drain("my-queue")
```
+++ JavaScript
```js
await room.queues.drain("my-queue");
```
+++ TypeScript
```ts
await room.queues.drain("my-queue");
```
+++ Dart
```dart
await room.queues.drain("my-queue");
```
+++

- **Parameters**:
  - `name` – The name of the queue to drain.
- **Description**  
  Removes all messages from the specified queue, effectively resetting its size to zero.


#### `close(name: string)`

+++ Python
```python
await room.queues.close("my-queue")
```
+++ JavaScript
```js
await room.queues.close("my-queue");
```
+++ TypeScript
```ts
await room.queues.close("my-queue");
```
+++ Dart
```dart
await room.queues.close("my-queue");
```
+++

- **Parameters**:
  - `name` – The name of the queue to close.
- **Description**  
  Closes the specified queue so that no further messages can be sent or received until it is reopened.


#### `send(name, message, create)`

+++ Python
```python
await room.queues.send("my-queue", {"foo": "bar"}, create=True)
```
+++ JavaScript
```js
await room.queues.send("my-queue", { foo: "bar" }, { create: true });
```
+++ TypeScript
```ts
await room.queues.send("my-queue", { foo: "bar" }, { create: true });
```
+++ Dart
```dart
await room.queues.send("my-queue", {"foo": "bar"}, create: true);
```
+++


- **Parameters**:
  - `name` – The name of the queue to send a message to.
  - `message` – A JSON-serializable object containing the data you want to send.
  - `create` – (Optional) Whether to create the queue if it does not exist. Defaults to `true`.
- **Description**  
  Sends a message to the specified queue. If `create` is true, the queue will be created automatically if it doesn’t exist.


#### `receive(name, create, wait)`

+++ Python
```python
message = await room.queues.receive("my-queue", create=True, wait=True)
```
+++ JavaScript
```js
const message = await room.queues.receive("my-queue", { create: true, wait: true });
```
+++ TypeScript
```ts
const message = await room.queues.receive("my-queue", { create: true, wait: true });
```
+++ Dart
```dart
final message = await room.queues.receive("my-queue", create: true, wait: true);
```
+++

- **Parameters**:
  - `name` – The name of the queue to receive a message from.
  - `create` – (Optional) Whether to create the queue if it does not exist. Defaults to `true`.
  - `wait` – (Optional) Whether to wait (block) until a message is available. Defaults to `true`. Behavior may vary based on server-side configuration.
- **Returns**  
  A JSON-serializable object if a message is received, or `null` if the queue was empty (represented by an `EmptyResponse`).

- **Description**  
  Tries to receive one message from the specified queue. If the response from the server is `EmptyResponse`, the method returns `null`. Otherwise, it returns the JSON object from the `JsonResponse`.

---

## Additional Notes

- **Error Handling**  
  When a request fails or the server returns an error response, the underlying `RoomClient` may throw errors. Make sure to wrap calls in `try/catch` if you need to handle them gracefully.

- **Concurrency and Performance**  
  - For high-throughput scenarios, ensure that your server and `RoomClient` configuration is optimized for concurrency.
  - The `receive` method’s `wait` parameter may affect your application’s design. If `wait` is `true`, the call might block until a message is available (depending on the server’s capabilities).

- **Extensibility**  
  You can add additional queue-related functionality (e.g., message peek, dead-letter queues, etc.) by extending `QueuesClient` or creating related classes that also use `RoomClient`.
