# MeshAgent Quickstart: Mailbot

Create a simple mail agent that responds to emails. You can run it locally or deploy it as a persistent service in MeshAgent Studio. Before using the mailbot you will need to provision an email for the agent. You can do this in [MeshAgent Studio](https://studio.meshagent.com) by clicking on the **Mail** tab, then creating a mailbox and assigning it to the room you want to use the agent in. 

## Prerequisites
- MeshAgent account, sign up at [www.meshagent.com](https://www.meshagent.com)
- MeshAgent CLI installed (`uv add "meshagent[all]"`)

## What's included
- `meshagent.yaml` for deploying the agent as a MeshAgent service (uses a public image)


## Option 1: Run Locally
Run the mailbot on your local machine (mailbot stops as soon as you end the command or close your terminal). Before starting the container you **must** provision a mailbox (queue + email address) for the room first! In [MeshAgent Studio](https://studio.meshagent.com) open the **Mail** tab, create a mailbox, and assign it to your room.  


Start the CLI mailbot and call it into the room:
```bash
meshagent setup
export EMAIL_ADDRESS=<your_email>@mail.meshagent.com
export EMAIL_QUEUE=<your_email_queue>
meshagent mailbot join --agent-name=mailbot --room=myroom --queue="$EMAIL_QUEUE" --email-address="$EMAIL_ADDRESS"
```

You will see logs printed to the terminal that the mailbot has joined the room, now you can email the agent and wait for it's response. You will see additional logs printed to the terminal as the agent receives and sends messages. 

You will not see the agent in the participants tab of the room in [MeshAgent Studio](https://studio.meshagent.com)because mailbots are not enabled with messaging, they are designed specifically for email. From the "Developer Console" in the logs section you will see that the mailbot has joined the room. You can also check the new "emails" folder in the Files tab to verify that your email was received. 

## Option 2: Deploy the agent as a service in MeshAgent Studio
Use this when you want the agent to be always available in a room or project. No Dockerfile needed; the YAML points to a maintained public image. You will need to update the service template first with your email and queue name in the environment section. 

```
meshagent service create --file=meshagent.yaml --room=myroom 
```

Now your mailbot will be available in the room! 

---
## For more information see: 

**Website**: www.meshagent.com(https://www.meshagent.com)
**Documentation**: docs.meshagent.com(https://docs.meshagent.com/)
