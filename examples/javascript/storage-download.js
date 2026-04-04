const data = new TextEncoder().encode("Hello, Storage!");

if (!(await room.storage.exists("example.txt"))) {
    await room.storage.upload("example.txt", data, { overwrite: true });
}

const response = await room.storage.download("example.txt");
console.log("Downloaded content:", new TextDecoder().decode(response.data));

await room.storage.delete("example.txt");
