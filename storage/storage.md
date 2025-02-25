# Storage

The storage API manages files and folders within a room’s remote storage. All interactions are asynchronous (using `await`) and return promises/futures. The storage system can notify clients when files are created, updated, or deleted via events, enabling real-time synchronization or UI updates.

---

## Overview

The storage functionality provides a straightforward way to check if files exist, create or overwrite them, append data in multiple writes, download or get a direct URL to a file, list folder contents, and finally delete files when they are no longer needed.

Key concepts include:

- **Async Methods**: All I/O methods are asynchronous and return futures/promises.
- **Handles**: Opening a file returns an object you can use for writing data and eventually closing.
- **Events**: The storage system can emit events whenever a file is updated or deleted.

---

## Events

The storage system emits two types of events:

1. **`file_updated`**  
   Triggered when a file is created or updated. Handlers receive a `path` argument identifying the file's location in storage.
   
   ```python
   def on_file_updated(path: str):
       print(f"File updated: {path}")

   room.storage.on("file_updated", on_file_updated)
   ```

2. **`file_deleted`**  
   Triggered when a file is deleted. Handlers receive a `path` argument identifying the file's location in storage.
   
   ```python
   def on_file_deleted(path: str):
       print(f"File deleted: {path}")

   room.storage.on("file_deleted", on_file_deleted)
   ```

You can remove an event handler with:
```python
room.storage.off("file_updated", on_file_updated)
room.storage.off("file_deleted", on_file_deleted)
```

---

## API Methods

Below is a summary of the primary methods. Each method is asynchronous, so you should `await` the call.

### 1. `exists(path)`

**Description**  
Checks if a file or folder exists at the given path.

**Parameters**  
- `path` *(str)*: The path to check.

**Returns**  
- *(bool)*: `True` if the file or folder exists; `False` otherwise.

**Example**:
```python
if await room.storage.exists(path="folder/data.json"):
    print("Data file exists!")
else:
    print("Data file does not exist.")
```

---

### 2. `open(path, overwrite=False)`

**Description**  
Opens a file for writing. Returns a handle used for subsequent write calls and closing.  
If `overwrite` is `True`, an existing file at this path will be truncated.

**Parameters**  
- `path` *(str)*: The file path to open or create.
- `overwrite` *(bool, optional)*: Whether to overwrite if the file already exists. Defaults to `False`.

**Returns**  
- *Handle Object*: An object representing an open file, usable with `write` and `close`.

**Example**:
```python
handle = await room.storage.open(path="files/new.txt", overwrite=True)
```

---

### 3. `write(handle, data)`

**Description**  
Writes binary data to an open file handle.

**Parameters**  
- `handle` *(file handle)*: The handle returned by `open`.
- `data` *(bytes)*: The data to write.

**Returns**  
- `None`

**Example**:
```python
data_to_write = b"Sample data"
await room.storage.write(handle=my_handle, data=data_to_write)
```

---

### 4. `close(handle)`

**Description**  
Closes an open file handle, ensuring all data has been written.

**Parameters**  
- `handle` *(file handle)*: The handle to close.

**Returns**  
- `None`

**Example**:
```python
await room.storage.close(handle=my_handle)
```

---

### 5. `download(path)`

**Description**  
Retrieves the content of a file from the remote storage.  

**Parameters**  
- `path` *(str)*: The file path to download.

**Returns**  
- *File-like Response*: Contains the file's raw data, typically accessible through a `.data` property.

**Example**:
```python
file_response = await room.storage.download(path="files/data.bin")
print(file_response.data)  # raw bytes
```

---

### 6. `download_url(path)`

**Description**  
Requests a downloadable URL for the specified file path, which can be used to fetch the file directly (e.g., via HTTP). The exact protocol or format of the returned URL may vary.

**Parameters**  
- `path` *(str)*: The file path to retrieve a download URL for.

**Returns**  
- *(str)*: A URL string you can fetch with your own HTTP or other suitable client.

**Example**:
```python
url = await room.storage.download_url(path="files/report.pdf")
print("Download the file from:", url)
```

---

### 7. `list(path)`

**Description**  
Lists the contents of a folder, returning file and subfolder names along with a flag indicating if each entry is a folder.

**Parameters**  
- `path` *(str)*: The folder path to list.

**Returns**  
- *(list)*: A list of entries, each containing a `name` and `is_folder` property.

**Example**:
```python
entries = await room.storage.list(path="some_folder")
for e in entries:
    print(e.name, "is folder?" if e.is_folder else "is file?")
```

---

### 8. `delete(path)`

**Description**  
Deletes a file at the given path. A `file_deleted` event is typically emitted afterward.

**Parameters**  
- `path` *(str)*: The file path to delete.

**Returns**  
- `None`

**Example**:
```python
await room.storage.delete("folder/old_file.txt")
print("File deleted.")
```

---

## Example Workflow

A common use case:

1. Check if a file exists.  
2. Create and write data if it doesn’t exist.  
3. Later, download the file to verify or use the data.  
4. Delete the file when it’s no longer needed, reacting to the `file_deleted` event.

```python
# Check existence
exists = await room.storage.exists(path="example.txt")
if not exists:
    # Create it
    handle = await room.storage.open(path="example.txt")
    await room.storage.write(handle=handle, data=b"Hello, Storage!")
    await room.storage.close(handle=handle)

# Download content
response = await room.storage.download(path="example.txt")
print("Downloaded content:", response.data)

# Delete it
await room.storage.delete("example.txt")
```

This sequence demonstrates basic creation, reading, and deletion flows within a single session.  

---

## Conclusion

The storage interface offers asynchronous file operations, suitable for real-time collaboration scenarios. You can track file updates or deletions through event handlers and immediately sync or update your application. This design makes it easy to build experiences around shared data that are robust, flexible, and user-friendly.