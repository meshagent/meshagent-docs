using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Threading.Tasks;
using Meshagent.Api.Room;

// Run with:
// meshagent room connect --room=toolsroom --identity=sample-participant -- <your dotnet command>

class Program
{
    static async Task Main()
    {
        await using var room = new RoomClient();
        await room.ConnectAsync();

        var arguments = new Dictionary<string, object> { ["a"] = 1, ["b"] = 2 };
        var addResult = await room.Agents.InvokeTool("math-toolkit", "add", arguments);
        Console.WriteLine($"The result from adding the numbers is: {JsonSerializer.Serialize(addResult.ToJson())}");

        var subtractResult = await room.Agents.InvokeTool("math-toolkit", "subtract", arguments);
        Console.WriteLine($"The result from subtracting the numbers is: {JsonSerializer.Serialize(subtractResult.ToJson())}");
    }
}
