data_to_write = b"Hello, Storage!"

if not await room.storage.exists(path="example.txt"):
    await room.storage.upload(
        path="example.txt",
        data=data_to_write,
        overwrite=True,
    )

response = await room.storage.download(path="example.txt")
print("Downloaded content:", response.data)

await room.storage.delete(path="example.txt")
