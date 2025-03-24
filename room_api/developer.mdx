# Developer

`DeveloperClient` enables inspection and debugging `RoomClient` through message logs. It listens for `developer.log` messages from the server and emits them locally as `RoomLogEvent` objects.

---

## Overview

- **`DeveloperClient`** – A high-level client that listens for `developer.log` events and provides methods to watch, unwatch, and send developer logs.

## API Methods

Below is an example of how you might use the `DeveloperClient` in your code:

+++ Python
```python
# Instantiate a RoomClient (not shown here).
# Suppose you already have a RoomClient instance named `room_client`.

# Create the DeveloperClient
dev_client = DeveloperClient(room=room_client)

# Enable developer logs
await dev_client.enable()

# Send a developer log
await dev_client.log("info", {"message": "Hello from Python!"})

# Disable developer logs
await dev_client.disable()
```
+++ JavaScript
```js
// Instantiate a RoomClient (not shown here).
// Suppose you already have a RoomClient instance named `roomClient`.

// Create the DeveloperClient
const devClient = new DeveloperClient({ room: roomClient });

// Enable developer logs
await devClient.enable();

// Send a developer log
await devClient.log("info", { message: "Hello from JavaScript!" });

// Disable developer logs
await devClient.disable();
```
+++ TypeScript
```ts
// Instantiate a RoomClient (not shown here).
// Suppose you already have a RoomClient instance named `roomClient`.

// Create the DeveloperClient
const devClient = new DeveloperClient({ room: roomClient });

// Enable developer logs
await devClient.enable();

// Send a developer log
await devClient.log("info", { message: "Hello from TypeScript!" });

// Disable developer logs
await devClient.disable();
```
+++ Dart
```dart
// Instantiate a RoomClient (not shown here).
// Suppose you already have a RoomClient instance named `roomClient`.

// Create the DeveloperClient
final devClient = DeveloperClient(room: roomClient);

// Enable developer logs
await devClient.enable();

// Send a developer log
await devClient.log("info", {"message": "Hello from Dart!"});

// Disable developer logs
await devClient.disable();
```
+++

---

### `DeveloperClient`

A client that listens for `developer.log` events and provides methods to enable, disable, and log custom developer messages.

- **`room: RoomClient`**  
  An instance of `RoomClient`, which handles the underlying communication with the server.

#### Constructor

**`new DeveloperClient({ room })`**

+++ Python
```python
dev_client = DeveloperClient(room=room_client)
```
+++ JavaScript
```js
const devClient = new DeveloperClient({ room: roomClient });
```
+++ TypeScript
```ts
const devClient = new DeveloperClient({ room: roomClient });
```
+++ Dart
```dart
final devClient = DeveloperClient(room: roomClient);
```
+++

- **Parameters**:
  - `room` – A `RoomClient` instance to route requests and handle incoming events.

- **Description**  
  Creates a new `DeveloperClient`. Internally, it sets up a protocol handler for `"developer.log"` messages, parsing incoming messages and emitting them locally as `RoomLogEvent` objects.  

---

#### `log(type: string, data: Record<string, any>)`

Sends a `developer.log` message to the server with the specified type and data. This can be used to track custom logs, diagnostics, or other developer-related messages in your application.

+++ Python
```python
await dev_client.log("warn", {"status": "Something might be wrong"})
```
+++ JavaScript
```js
await devClient.log("warn", { status: "Something might be wrong" });
```
+++ TypeScript
```ts
await devClient.log("warn", { status: "Something might be wrong" });
```
+++ Dart
```dart
await devClient.log("warn", {"status": "Something might be wrong"});
```
+++

- **Parameters**:
  - `type` – A string identifying the log level or category, such as `"info"`, `"warn"`, or `"debug"`.
  - `data` – A JSON-serializable object containing additional details for the log entry.

- **Description**  
  Encodes the `type` and `data` into a message, then sends it to the server. This message is typically consumed by developers or other backend listeners for debugging or monitoring purposes.

---

#### `enable()`

Watches developer messages on the server, effectively enabling the reception of `developer.log` events.

+++ Python
```python
await dev_client.enable()
```
+++ JavaScript
```js
await devClient.enable();
```
+++ TypeScript
```ts
await devClient.enable();
```
+++ Dart
```dart
await devClient.enable();
```
+++

- **Description**  
  Sends a `developer.watch` message to the server to start receiving `developer.log` events. If the server is configured to honor these watch requests, it will begin sending any future developer logs to this client.

---

#### `disable()`

Unwatches developer messages on the server, stopping the reception of `developer.log` events.

+++ Python
```python
await dev_client.disable()
```
+++ JavaScript
```js
await devClient.disable();
```
+++ TypeScript
```ts
await devClient.disable();
```
+++ Dart
```dart
await devClient.disable();
```
+++

- **Description**  
  Sends a `developer.unwatch` message to the server to stop receiving `developer.log` events. Further developer logs from the server will be ignored until `enable()` is called again.

---

## Additional Notes

- **Event Emission**  
  The `DeveloperClient` extends an `EventEmitter<RoomLogEvent>`. It emits a `"log"` event whenever a `developer.log` message is received from the server. You can listen to these events as follows:
  
  +++ JavaScript
  ```js
  devClient.on("log", (event) => {
    console.log("Developer log event:", event);
  });
  ```
  +++

- **Integration with `RoomClient`**  
  Internally, `DeveloperClient` uses the same `Protocol` instance attached to `RoomClient` to send and receive developer-related messages. If `RoomClient` is disconnected, messages will not be delivered.

- **Error Handling**  
  If a request fails or the server returns an error, the underlying `RoomClient` may throw an exception (e.g., `RoomServerException`). Handle it accordingly in your code:

  +++ TypeScript
  ```ts
  try {
    await devClient.enable();
  } catch (err) {
    console.error("Failed to enable developer logs:", err);
  }
  ```
  +++

- **Extensibility**  
  You can extend or wrap `DeveloperClient` to include additional developer-oriented features, such as profiling, advanced filtering, or forwarding logs to other services.
