using System;
using System.Threading.Tasks;
using Meshagent.Api;
using Meshagent.Api.Room;
using Meshagent.Api.Protocol;
using Meshagent.Api.Tokens;

class Program
{
    static string Env(string name)
    {
        var value = Environment.GetEnvironmentVariable(name);
        if (string.IsNullOrEmpty(value))
        {
            throw new Exception($"Missing required environment variable: {name}.");
        }
        return value;
    }

    static async Task Main()
    {
        var roomName = "my-room";
        var meshagentApiKey = Env("MESHAGENT_API_KEY");
        var parsedApiKey = ApiKey.Parse(meshagentApiKey);

        var token = new ParticipantToken(
            name: "participant",
            projectId: parsedApiKey.ProjectId,
            apiKeyId: parsedApiKey.Id
        );
        token.AddRoomGrant(roomName);
        token.AddRoleGrant("agent");
        token.AddApiGrant(ApiScope.AgentDefault());

        var protocol = new WebSocketClientProtocol(
            url: Helpers.WebSocketRoomUrl(roomName),
            token: token.ToJwt(parsedApiKey.Secret)
        );

        await using var room = new RoomClient(protocol);
        await room.ConnectAsync();

        Console.WriteLine($"Connected to room: {room.RoomName}");
    }
}