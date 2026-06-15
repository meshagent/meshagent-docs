using System;
using System.Threading.Tasks;
using Meshagent.Api.Room;

// Run with:
// meshagent room connect --room=gettingstarted --identity=sample-participant -- dotnet run

class Program
{
    static async Task Main()
    {
        await using var room = new RoomClient();
        await room.ConnectAsync();

        var toolkits = await room.Agents.ListToolkits();

        Console.WriteLine("The tools connected to our room are:");
        foreach (var toolkit in toolkits)
        {
            Console.WriteLine($"\n Toolkit: {toolkit.Name}: {toolkit.Title} - {toolkit.Description}");
            foreach (var tool in toolkit.Tools)
            {
                Console.WriteLine($" Tool: {tool.Name}: {tool.Title} - {tool.Description}");
            }
        }
    }
}
