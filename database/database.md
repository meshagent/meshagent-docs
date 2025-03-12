# Database

The database client serves as a high-level interface for interacting with a relational-like database. 

---

## Overview

The database interface is designed to simplify common database operations in a room-based system. Each method in database client corresponds to a particular request sent to the server, handling tasks like table creation, updates, deletions, and searches. The client leverages `JsonResponse` objects and typed parameters to streamline the process.

---

## API Methods

Below is a summary of the primary methods. Each method is asynchronous, so you should `await` the call.

### 1. List Tables
**Description**
Retrieves a list of all table names currently present in the database.

**Returns**:
- A promise that resolves to an array of table name strings.

+++ Python
``` python
tables = await room.database.list_tables()

print(tables)  # ["users", "orders", "products", ...]
```

+++ JavaScript
```javascript
const tables = await room.database.listTables();

console.log(tables); // ["users", "orders", "products", ...]
```

+++ TypeScript
```typescript
const tables = await room.database.listTables();

console.log(tables); // ["users", "orders", "products", ...]
```

+++ Dart
```dart
final tables = await room.database.listTables();

print(tables); // ["users", "orders", "products", ...]
```
+++


---

### 2. Create Table with Schema
- **Description**: Creates a new table with an optional schema and initial data. You can specify how the table should be created through the `mode` parameter.
  - **modes**:
    - `"create"`: Creates the table; fails if it already exists.
    - `"overwrite"`: Drops the existing table (if any) and creates a new one.
    - `"create_if_not_exists"`: Creates the table only if it does not already exist.
- **Parameters**:
  - **name**: The name of the new table.
  - **schema**: An optional record defining column names and their data types.
  - **data**: An optional array of initial records to populate the table.
  - **mode**: The creation mode (default is `"create"`).
- **Returns**: A promise that resolves once the table is created.

**Example**:
+++ Python
```python
await room.database.create_table_with_schema({
  "name": "users",
  "schema": {
    "id": IntDataType(),
    "username": TextDataType(),
    "email": TextDataType(),
  },
  "data": [
    {"id": 1, "username": "alice", "email": "alice@example.com" },
    {"id": 2, "username": "bob", "email": "bob@example.com" }
  ],
  "mode": "create"
})
```
+++ JavaScript
```ts
await room.database..createTableWithSchema({
  name: "users",
  schema: {
    id: new IntDataType(),
    username: new TextDataType(),
    email: new TextDataType(),
  },
  data: [
    { id: 1, username: "alice", email: "alice@example.com" },
    { id: 2, username: "bob", email: "bob@example.com" }
  ],
  mode: "create",
});
```
+++ TypeScript
```ts
await room.database.createTableWithSchema({
  name: "users",
  schema: {
    id: new IntDataType(),
    username: new TextDataType(),
    email: new TextDataType(),
  },
  data: [
    { id: 1, username: "alice", email: "alice@example.com" },
    { id: 2, username: "bob", email: "bob@example.com" }
  ],
  mode: "create",
});
```
+++ Dart
```dart
await room.database.createTableWithSchema({
  "name": "users",
  "schema": {
    "id": IntDataType(),
    "username": TextDataType(),
    "email": TextDataType(),
  },
  "data": [
    {"id": 1, "username": "alice", "email": "alice@example.com" },
    {"id": 2, "username": "bob", "email": "bob@example.com" }
  ],
  mode: "create"
});
```
+++

---

### 3. Create Table from Data
- **Description**: Creates a table using only data and an optional mode.
- **Parameters**:
  - **name**: The table name to create.
  - **data**: An array of records to initialize the table with.
  - **mode**: Table creation mode (default `"create"`).
- **Returns**: A promise that resolves once the table is created.

**Example**:
+++ Python
```python
await room.database.create_table_from_data({
  "name": "orders",
  "data": [
    {"id": 1, "product": "Laptop", "quantity": 2},
    {"id": 2, "product": "Phone", "quantity": 5},
  ],
  "mode": "overwrite"
})
```
+++ JavaScript
```js
await room.database.createTableFromData({
  name: "orders",
  data: [
    { id: 1, product: "Laptop", quantity: 2 },
    { id: 2, product: "Phone", quantity: 5 },
  ],
  mode: "overwrite",
});
```
+++ TypeScript
```ts
await room.database.createTableFromData({
  name: "orders",
  data: [
    { id: 1, product: "Laptop", quantity: 2 },
    { id: 2, product: "Phone", quantity: 5 },
  ],
  mode: "overwrite",
});
```
+++ Dart
```dart
await room.database.createTableFromData({
  "name": "orders",
  "data": [
    {"id": 1, "product": "Laptop", "quantity": 2},
    {"id": 2, "product": "Phone", "quantity": 5},
  ],
  mode: "overwrite"
});
```
+++

---

### 4. Drop Table
- **Description**: Drops (deletes) a table by name, optionally ignoring if it does not exist.
- **Parameters**:
  - **name**: The name of the table to drop.
  - **ignoreMissing**: If `true`, no error is thrown if the table does not exist.
- **Returns**: A promise that resolves once the table is dropped.

**Example**:
+++ Python
```python
await room.database.drop_table({
  "name": "temp_table",
  "ignoreMissing": True
})
```
+++ JavaScript
```js
await room.database.dropTable({
  name: "temp_table",
  ignoreMissing: true,
});
```
+++ TypeScript
```ts
await room.database.dropTable({
  name: "temp_table",
  ignoreMissing: true,
});
```
+++ Dart
```dart
await room.database.dropTable({
  "name": "temp_table",
  "ignoreMissing": true,
});
```
+++

---

### 5. Add Columns
- **Description**: Adds one or more columns to an existing table, specifying default value expressions.
- **Parameters**:
  - **table**: Name of the target table.
  - **newColumns**: A record mapping column names to default value expressions (SQL or literal).
- **Returns**: A promise that resolves once the columns are added.

**Example**:
+++ Python
```python
await room.database.add_columns({
  "table": "users",
  "newColumns": {
    "isActive": "true",
    "createdAt": "CURRENT_TIMESTAMP",
  }
})
```
+++ JavaScript
```js
await room.database..addColumns({
  table: "users",
  newColumns: {
    isActive: "true",
    createdAt: "CURRENT_TIMESTAMP",
  },
});
```
+++ TypeScript
```ts
await room.database.addColumns({
  table: "users",
  newColumns: {
    isActive: "true",
    createdAt: "CURRENT_TIMESTAMP",
  },
});
```
+++ Dart
```dart
await room.database.addColumns({
  "table": "users",
  "newColumns": {
    "isActive": "true",
    "createdAt": "CURRENT_TIMESTAMP",
  },
});
```
+++

---

### 6. Drop Columns
- **Description**: Drops (removes) one or more columns from an existing table.
- **Parameters**:
  - **table**: Name of the target table.
  - **columns**: An array of column names to remove.
- **Returns**: A promise that resolves once the columns are dropped.

**Example**:
+++ Python
```python
await room.database.drop_columns({
  "table": "users",
  "columns": ["deprecatedColumn1", "deprecatedColumn2"]
})
```
+++ JavaScript
```js
await room.database.dropColumns({
  table: "users",
  columns: ["deprecatedColumn1", "deprecatedColumn2"],
});
```
+++ TypeScript
```ts
await room.database.dropColumns({
  table: "users",
  columns: ["deprecatedColumn1", "deprecatedColumn2"],
});
```
+++ Dart
```dart
await room.database.dropColumns({
  "table": "users",
  "columns": ["deprecatedColumn1", "deprecatedColumn2"],
});
```
+++

---

### 7. Insert
- **Description**: Inserts one or more new records into a table.
- **Parameters**:
  - **table**: The name of the table to insert into.
  - **records**: An array of objects, each containing column-value pairs.
- **Returns**: A promise that resolves once the records are inserted.

**Example**:
+++ Python
```python
await room.database.insert({
  "table": "users",
  "records": [
    { "id": 3, "username": "charlie", "email": "charlie@example.com" },
    { "id": 4, "username": "dana", "email": "data@example.com" },
  ],
})
```
+++ JavaScript
```js
await room.database.insert({
  table: "users",
  records: [
    { id: 3, username: "charlie", email: "charlie@example.com" },
    { id: 4, username: "dana", email: "data@example.com" },
  ],
});
```
+++ TypeScript
```ts
await room.database.insert({
  table: "users",
  records: [
    { id: 3, username: "charlie", email: "charlie@example.com" },
    { id: 4, username: "dana", email: "dana@example.com" },
  ],
});
```
+++ Dart
```dart
await room.database.insert({
  "table": "users",
  "records": [
    { "id": 3, "username": "charlie", "email": "charlie@example.com" },
    { "id": 4, "username": "dana", "email": "data@example.com" },
  ],
});
```
+++

---

### 8. Update
- **Description**: Updates existing records in a table.
- **Parameters**:
  - **table**: Name of the table to update.
  - **where**: A SQL `WHERE` clause specifying which records to update (e.g. `"id = 123"`).
  - **values**: A record of key-value pairs for direct assignment (e.g. `{ age: 30 }`).
  - **valuesSql**: A record of key-value pairs for SQL expressions (e.g. `{ age: "age + 1" }`).
- **Returns**: A promise that resolves once the update is complete.

**Example**:
+++ Python
```python
await room.database.update({
  "table": "users",
  "where": "id = 3",
  "values": { "email": "newcharlie@example.com" },
  "valuesSql": { "loginCount": "loginCount + 1" },
})
```
+++ JavaScript
```js
await room.database.update({
  table: "users",
  where: "id = 3",
  values: { email: "newcharlie@example.com" },
  valuesSql: { loginCount: "loginCount + 1" },
});
```
+++ TypeScript
```ts
await room.database.update({
  table: "users",
  where: "id = 3",
  values: { email: "newcharlie@example.com" },
  valuesSql: { loginCount: "loginCount + 1" },
});
```
+++ Dart
```dart
await room.database.update({
  "table": "users",
  "where": "id = 3",
  "values": { "email": "newcharlie@example.com" },
  "valuesSql": { "loginCount": "loginCount + 1" },
})
```
+++

---

### 9. Delete
- **Description**: Deletes records from a table that match a specified condition.
- **Parameters**:
  - **table**: The target table.
  - **where**: A SQL `WHERE` clause for filtering which records to delete.
- **Returns**: A promise that resolves once the records are deleted.

**Example**:
+++ Python
```python
await room.database.delete({
  "table": "users",
  "where": "id = 4"
})
```
+++ JavaScript
```js
await room.database.delete({
  table: "users",
  where: "id = 4",
});
```
+++ TypeScript
```ts
await room.database.delete({
  table: "users",
  where: "id = 4",
});
```
+++ Dart
```dart
await room.database.delete({
  "table": "users",
  "where": "id = 4"
})
```
+++

---

### 10. Merge
- **Description**: Performs an **upsert** (update/insert) by merging incoming records into an existing table. Records matching the `on` column are updated; otherwise, new rows are inserted.
- **Parameters**:
  - **table**: The target table.
  - **on**: The column name used to match existing records.
  - **records**: The record(s) to merge/upsert.
- **Returns**: A promise that resolves once the operation is complete.

**Example**:
+++ Python
```python
await room.database.merge({
  "table": "users",
  "on": "id",
  "records": [
    { "id": 1, "username": "alice", "email": "alice_new@example.com" },
    { "id": 5, "username": "eric", "email": "eric@example.com" },
  ],
})
```
+++ JavaScript
```js
await room.database.merge({
  table: "users",
  on: "id",
  records: [
    { id: 1, username: "alice", email: "alice_new@example.com" },
    { id: 5, username: "eric", email: "eric@example.com" },
  ],
});
```
+++ TypeScript
```ts
await room.database.merge({
  table: "users",
  on: "id",
  records: [
    { id: 1, username: "alice", email: "alice_new@example.com" },
    { id: 5, username: "eric", email: "eric@example.com" },
  ],
});
```
+++ Dart
```dart
await room.database.merge({
  "table": "users",
  "on": "id",
  "records": [
    { "id": 1, "username": "alice", "email": "alice_new@example.com" },
    { "id": 5, "username": "eric", "email": "eric@example.com" },
  ],
})
```
+++

---

### 11. Search
- **Description**: Searches for records in a table. This can be used for plain text search, vector similarity search, or simple SQL filtering.
- **Parameters**:
  - **table**: The target table name.
  - **text**: An optional search string (if using full-text indexes).
  - **vector**: An optional numeric array for vector-based similarity queries.
  - **where**: Either an SQL `WHERE` clause string or an object representing key-value equals conditions.
  - **limit**: Maximum number of matching records to return.
  - **select**: An array of column names to be returned.
- **Returns**: An array of matching records.

**Example**:
+++ Python
```python
results = await room.database.search({
  "table": "users",
  "where": { "username": "alice" },
  "limit": 1
})

print(results)  # [{"id": 1, "username": "alice", "email": "alice@example.com"}]
```
+++ JavaScript
```js
const results = await room.database.search({
  table: "users",
  where: { username: "alice" },
  limit: 1,
});

console.log(results); // [{ id: 1, username: "alice", email: "alice@example.com" }]
```
+++ TypeScript
```ts
const results = await room.database.search({
  table: "users",
  where: { username: "alice" },
  limit: 1,
});

console.log(results); // [{ id: 1, username: "alice", email: "alice@example.com" }]
```
+++ Dart
```dart
final results = await room.database.search({
  "table": "users",
  "where": { "username": "alice" },
  "limit": 1,
});

print(results); // [{"id": 1, "username": "alice", "email": "alice@example.com"}]
```
+++

---

#### 12. Optimize
- **Description**: Optimizes a table (e.g., compacts its storage or rebuilds indexes if required).
- **Parameters**:
  - **table**: Name of the table to optimize.
- **Returns**: A promise that resolves once the operation is complete.

**Example**:
+++ Python
```python
await room.database.optimize("users")
```
+++ JavaScript
```js
await room.database.optimize("users");
```
+++ TypeScript
```ts
await room.database.optimize("users");
```
+++ Dart
```dart
await room.database.optimize("users");
```
+++

---

### 13. Create Vector Index
- **Description**: Creates a vector index on a specified column for vector similarity searches.
- **Parameters**:
  - **table**: The target table name.
  - **column**: The column that holds vector data.
- **Returns**: A promise that resolves once the index is created.

**Example**:
+++ Python
```python
await room.database.create_vector_index({
  "table": "documents",
  "column": "embedding",
})
```
+++ JavaScript
```js
await room.database.createVectorIndex({
  table: "documents",
  column: "embedding",
});
```
+++ TypeScript
```ts
await room.database.createVectorIndex({
  table: "documents",
  column: "embedding",
});
```
+++ Dart
```dart
await room.database.createVectorIndex({
  "table": "documents",
  "column": "embedding",
});
```
+++

---

### 14. Create Scalar Index
- **Description**: Creates a scalar index (typical database index) on a specified column.
- **Parameters**:
  - **table**: The target table name.
  - **column**: The column for which to create the scalar index.
- **Returns**: A promise that resolves once the scalar index is created.

**Example**:
+++ Python
```python
await room.database.create_scalar_index({
  "table": "users",
  "column": "email",
})
```
+++ JavaScript
```js
await room.database.createScalarIndex({
  table: "users",
  column: "email",
});
```
+++ TypeScript
```ts
await room.database.createScalarIndex({
  table: "users",
  column: "email",
});
```
+++ Dart
```dart
await room.database.createScalarIndex({
  "table": "users",
  "column": "email",
});
```
+++

---

### 15. Create Full Text Search Index
- **Description**: Creates a full-text search index on a text column, useful for text-based queries.
- **Parameters**:
  - **table**: The table name.
  - **column**: The text column to index.
- **Returns**: A promise that resolves once the index is created.

**Example**:
+++ Python
```python
await room.database.create_full_text_search_index({
  "table": "articles",
  "column": "content",
})
```
+++ JavaScript
```js
await room.database.createFullTextSearchIndex({
  table: "articles",
  column: "content",
});
```
+++ TypeScript
```ts
await room.database.createFullTextSearchIndex({
  table: "articles",
  column: "content",
});
```
+++ Dart
```dart
await room.database.createFullTextSearchIndex({
  "table": "articles",
  "column": "content",
});
```
+++

---

### 16. List Indexes
- **Description**: Lists the indexes currently defined on a table.
- **Parameters**:
  - **table**: The name of the table for which to list indexes.
- **Returns**: A record object containing index information.

**Example**:
+++ Python
```python
indexes = await room.database.list_indexes({"table": "users"})

print(indexes)
# Example output:
# {
#   "scalarIndexes": ["email"],
#   "fullTextIndexes": ["username"],
#   "vectorIndexes": ["profile_embedding"]
# }
```
+++ JavaScript
```js
const indexes = await room.database.listIndexes({ table: "users" });

console.log(indexes);
// Example output:
// {
//   scalarIndexes: ["email"],
//   fullTextIndexes: ["username"],
//   vectorIndexes: ["profile_embedding"]
// }
```
+++ TypeScript
```ts
const indexes = await room.database.listIndexes({ table: "users" });

console.log(indexes); 
// Example output:
// {
//   scalarIndexes: ["email"],
//   fullTextIndexes: ["username"],
//   vectorIndexes: ["profile_embedding"]
// }
```
+++ Dart
```dart
final indexes = await room.database.listIndexes({"table": "users"});

print(indexes);
// Example output:
// {
//   "scalarIndexes": ["email"],
//   "fullTextIndexes": ["username"],
//   "vectorIndexes": ["profile_embedding"]
// }
```
+++

---

## Conclusion

The database interface provides a convenient abstraction for managing a database within a room server environment. It covers a broad set of operations—ranging from table creation and schema management to complex operations like vector-based and full-text searches. By handling the request/response flow through `RoomClient`, it keeps your database interactions modular and maintainable.
