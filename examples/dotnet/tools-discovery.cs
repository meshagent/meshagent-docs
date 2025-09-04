using System;
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
            throw new Exception($"Missing required environment variable: {name}. Try running meshagent env in the terminal to export the required environment variables.");
        }
        return value;
    }

    static async Task Main()
    {
        var roomName = "toolsroom";
        var token = new ParticipantToken(
            name: "participant",
            projectId: Env("MESHAGENT_PROJECT_ID"),
            apiKeyId: Env("MESHAGENT_KEY_ID")
        );
        token.AddRoomGrant(roomName);
        token.AddRoleGrant("agent");
        token.AddApiGrant(ApiScope.AgentDefault());

        var protocol = new WebSocketClientProtocol(
            url: Helpers.WebSocketRoomUrl(roomName),
            token: token.ToJwt(Env("MESHAGENT_SECRET"))
        );

        await using var room = new RoomClient(protocol);
        await room.ConnectAsync();

        var toolkits = await room.Agents.ListToolkits();

        LogProvider.GetLogger().LogInformation("The tools connected to our room are:");
        foreach (var toolkit in toolkits)
        {
            LogProvider.GetLogger().LogInformation($"\n Toolkit: {toolkit.Name}: {toolkit.Title} - {toolkit.Description}");
            foreach (var tool in toolkit.Tools)
            {
                LogProvider.GetLogger().LogInformation($" Tool: {tool.Name}: {tool.Title} - {tool.Description}");
            }
        }

        var agents = await room.Agents.ListAgents();
        LogProvider.GetLogger().LogInformation("The agents in the room are:");
        foreach (var agent in agents)
        {
            LogProvider.GetLogger().LogInformation($"Agent: {agent.Name}");
        }
    }
}