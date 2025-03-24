# Sync

`SyncClient` module provides a client for interacting with server-managed documents (such as `MeshDocument`) and synchronizing local changes with a remote server through a `RoomClient`. It contains two primary exports:

---

## Overview

- **`QueuedSync`** – A simple class that represents a queued message of changes for a given document path.
- **`SyncClient`** – A high-level client that sends requests through a provided `RoomClient` to open, create, synchronize, and close documents.

## API Methods

Below is an example of how you might use the `SyncClient` in your code:

+++ Python
```python
# Create a SyncClient instance
sync_client = SyncClient(room=my_room_client)

# Start listening for local changes to sync
sync_client.start()

# Create a MeshDocument on the server
await sync_client.createMeshDocumentWithMeshSchema(
    "my/path",
    schema=my_schema,
    json={"initial": "data"}
)

# Open a document (creates if not found)
doc = await sync_client.open("my/path", create=True)

# Perform some changes on `doc` here.
# The local changes will automatically be queued for syncing.

# Close the document
await sync_client.close("my/path")

# Dispose of the SyncClient to clean up resources
sync_client.dispose()
```
+++ JavaScript
```js
// Create a SyncClient instance
const syncClient = new SyncClient({ room: myRoomClient });

// Start listening for local changes to sync
syncClient.start();

// Create a MeshDocument on the server
await syncClient.createMeshDocumentWithMeshSchema("my/path", mySchema, { initial: "data" });

// Open a document (creates if not found)
const doc = await syncClient.open("my/path", { create: true });

// Perform some changes on `doc` here.
// The local changes will automatically be queued for syncing.

// Close the document
await syncClient.close("my/path");

// Dispose of the SyncClient to clean up resources
syncClient.dispose();
```
+++ TypeScript
```ts
// Create a SyncClient instance
const syncClient = new SyncClient({ room: myRoomClient });

// Start listening for local changes to sync
syncClient.start();

// Create a MeshDocument on the server
await syncClient.createMeshDocumentWithMeshSchema("my/path", mySchema, { initial: "data" });

// Open a document (creates if not found)
const doc = await syncClient.open("my/path", { create: true });

// Perform some changes on `doc` here.
// The local changes will automatically be queued for syncing.

// Close the document
await syncClient.close("my/path");

// Dispose of the SyncClient to clean up resources
syncClient.dispose();
```
+++ Dart
```dart
// Create a SyncClient instance
final syncClient = SyncClient(room: myRoomClient);

// Start listening for local changes to sync
syncClient.start();

// Create a MeshDocument on the server
await syncClient.createMeshDocumentWithMeshSchema(
  "my/path",
  mySchema,
  json: {"initial": "data"}
);

// Open a document (creates if not found)
final doc = await syncClient.open("my/path", create: true);

// Perform some changes on `doc` here.
// The local changes will automatically be queued for syncing.

// Close the document
await syncClient.close("my/path");

// Dispose of the SyncClient to clean up resources
syncClient.dispose();
```
+++

---

### `QueuedSync`

A simple helper class representing a single queued message of changes for a specific document path.

+++ Python
```python
queued_sync = QueuedSync(path="my/path", base64="encoded-changes")
```
+++ JavaScript
```js
const queuedSync = new QueuedSync({ path: "my/path", base64: "encoded-changes" });
```
+++ TypeScript
```ts
const queuedSync = new QueuedSync({ path: "my/path", base64: "encoded-changes" });
```
+++ Dart
```dart
final queuedSync = QueuedSync(path: "my/path", base64: "encoded-changes");
```
+++

- **`path: string`**  
  The unique path identifying the document on the server.

- **`base64: string`**  
  A base64-encoded string that represents a serialized set of changes to be synced to the backend.

---

### `SyncClient`

The `SyncClient` class is responsible for coordinating document synchronization through a `RoomClient`. It automatically listens for local changes on `MeshDocument` instances and forwards them to the remote server, while also applying remote changes as they are received.

- **`room: RoomClient`**  
  An instance of `RoomClient`, which handles the underlying communication with the server.

#### `start()`

+++ Python
```python
sync_client.start()
```
+++ JavaScript
```js
syncClient.start();
```
+++ TypeScript
```ts
syncClient.start();
```
+++ Dart
```dart
syncClient.start();
```
+++

- **Description**  
  Begins listening for local changes to any opened documents and queues them for synchronization.  
  You typically call this method once, shortly after instantiating the `SyncClient`.

#### `dispose()`

+++ Python
```python
sync_client.dispose()
```
+++ JavaScript
```js
syncClient.dispose();
```
+++ TypeScript
```ts
syncClient.dispose();
```
+++ Dart
```dart
syncClient.dispose();
```
+++

- **Description**  
  Cleans up internal resources used by the client, stops listening for changes, and closes any internal streams.

#### `createMeshDocumentWithMeshSchema(path, schema, json?)`

+++ Python
```python
await sync_client.createMeshDocumentWithMeshSchema("my/path", my_schema, json={"key": "value"})
```
+++ JavaScript
```js
await syncClient.createMeshDocumentWithMeshSchema("my/path", mySchema, { key: "value" });
```
+++ TypeScript
```ts
await syncClient.createMeshDocumentWithMeshSchema("my/path", mySchema, { key: "value" });
```
+++ Dart
```dart
await syncClient.createMeshDocumentWithMeshSchema("my/path", mySchema, json: {"key": "value"});
```
+++

- **Parameters**:
  - `path` – The path where the document will be created on the server.
  - `schema` – A `MeshSchema` describing the structure of the document.
  - `json` – (Optional) Initial data or metadata to send along with the creation request.
- **Description**  
  Sends a request to create a new `MeshDocument` at the given path with a specified schema.

#### `createMeshDocumentWithFormat(path, format, json?)`

+++ Python
```python
await sync_client.createMeshDocumentWithFormat("my/path", "json", json={"key": "value"})
```
+++ JavaScript
```js
await syncClient.createMeshDocumentWithFormat("my/path", "json", { key: "value" });
```
+++ TypeScript
```ts
await syncClient.createMeshDocumentWithFormat("my/path", "json", { key: "value" });
```
+++ Dart
```dart
await syncClient.createMeshDocumentWithFormat("my/path", "json", json: {"key": "value"});
```
+++

- **Parameters**:
  - `path` – The path where the document will be created on the server.
  - `format` – A string representing a schema format (e.g., `"json"`, `"yaml"`, etc.).
  - `json` – (Optional) Initial data or metadata to send along with the creation request.
- **Description**  
  Similar to the method above, but you specify a textual format rather than providing a `MeshSchema` object.

#### `open(path, { create = true })`

+++ Python
```python
doc = await sync_client.open("my/path", create=True)
```
+++ JavaScript
```js
const doc = await syncClient.open("my/path", { create: true });
```
+++ TypeScript
```ts
const doc = await syncClient.open("my/path", { create: true });
```
+++ Dart
```dart
final doc = await syncClient.open("my/path", create: true);
```
+++

- **Parameters**:
  - `path` – The path identifying the document to open.
  - `create` – (Optional) Whether to create the document if it doesn’t exist. Defaults to `true`.
- **Returns**  
  A `MeshDocument` instance tied to the specified path.
- **Description**  
  Sends a request to connect to (and possibly create) the document at the given path. If successful, returns a reference-counted `MeshDocument` that automatically sends local changes to the backend.

#### `close(path)`

+++ Python
```python
await sync_client.close("my/path")
```
+++ JavaScript
```js
await syncClient.close("my/path");
```
+++ TypeScript
```ts
await syncClient.close("my/path");
```
+++ Dart
```dart
await syncClient.close("my/path");
```
+++

- **Parameters**:
  - `path` – The path of the document to close.
- **Description**  
  Decrements the internal reference count for the document. If it reaches zero, the document is unregistered locally, and a request is sent to the server to disconnect. No further changes will be synced once closed.

#### `sync(path, data)`

+++ Python
```python
await sync_client.sync("my/path", b"some bytes")
```
+++ JavaScript
```js
await syncClient.sync("my/path", new Uint8Array([/*...bytes...*/]));
```
+++ TypeScript
```ts
await syncClient.sync("my/path", new Uint8Array([/*...bytes...*/]));
```
+++ Dart
```dart
// In Dart, you might have a ByteData or Uint8List
await syncClient.sync("my/path", Uint8List.fromList([/*...bytes...*/]));
```
+++

- **Parameters**:
  - `path` – The path of the document to synchronize.
  - `data` – A `Uint8Array` (or equivalent) containing serialized changes.
- **Description**  
  Immediately sends sync data to the server. This method is useful if you have already encoded your changes and want to bypass the typical queued flow.

---

## Additional Notes

- **Synchronized Changes**  
  Once a document is opened, any local changes you make in the associated `MeshDocument` are automatically queued for sending, thanks to `sendChangesToBackend`. You rarely need to call `sync()` manually unless you want to send raw data yourself.

- **Reference Counting**  
  The `SyncClient` internally tracks how many times a document is opened via the same path. Calling `open` multiple times for the same path returns the same underlying document. Only when all references are closed (via `close()`) will the client actually disconnect.

- **Error Handling**  
  If a request fails, the `RoomClient` may throw an error (like `RoomServerException`). Wrap calls in `try/catch` (or use `.catch(...)`) to handle them gracefully.

- **Concurrency and Performance**  
  - For high throughput, ensure that your `RoomClient` and server are configured for concurrent operations.
  - The `SyncClient` uses a `StreamController` internally to manage queued updates, sending them asynchronously to the server.

- **Extensibility**  
  You can extend the `SyncClient` for specialized document operations—such as partial updates, conflict resolution logic, or customized schema handling—by adding new methods or composing it with other classes that also use `RoomClient`.
