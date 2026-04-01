final data = Uint8List.fromList(utf8.encode("Hello, Storage!"));
if (!await room.storage.exists("example.txt")) {
    await room.storage.upload("example.txt", data, overwrite: true);
}

final response = await room.storage.download("example.txt");
print("Downloaded content: ${utf8.decode(response.data)}");

await room.storage.delete("example.txt");
