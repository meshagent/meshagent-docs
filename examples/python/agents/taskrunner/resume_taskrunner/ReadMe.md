# Resume Processing Example

This sample wires up a resume-processing workflow inside a MeshAgent room. It creates tables in the room database to track candidates, open roles, and candidate role scores. It also uses a MailWorker agent for resume processing. Candidates email the MailWorker who stores their resume and candidate details in the room. 

Once the candidate information is stored, another agent compares the candidates background to open roles and suggests matches. 

## Table setup (`setup_tables.py`)
- Reads your API key from `MESHAGENT_API_KEY` and the API base from `MESHAGENT_API_URL` (defaults to ).
- Connects to the room over WebSocket and creates three tables if they don’t exist: `candidates`, `open_roles`, and `candidate_role_scores`.
- Run it with a room of your choice (defaults to `resume`): `python3 setup_tables.py --room <room-name>` or set `ROOM_NAME` in your env.

## Steps

1. Create an email address for the agent (in MeshAgent Studio and assign it to a room and queue. For example email=jobs@mail.meshagent.com, queue=jobs_email)

2. Create the required tables for resume processing (run once when creating a new room for resume processing).  `python3 setup_tables.py --room resume` 

Now we can test the agent out locally before deploying: 

1. Run the remote toolkit in the resume_runner file. We will give this toolkit to the mail agent so it can update the `candidates` table in the database with information about each candidate.

    `meshagent service run main.py --room resume`

2. Next, call the mailbot into the room. As long as our toolkit is running locally, we can pass it to the mailbot for use. We'll also give the agent access to the storage toolkit so it can read/write files in the room and the web search toolkit so it can research the candidates. We will also pass the room-rules flag so a recruiter or hiring manager can tailor the criteria for how the mailworker should process and score resumes. 

`meshagent mailbot join --room resume --agent-name jobs --queue resume_email --email-address jobs@mail.meshagent.life --toolkit-name mailbot.mail --toolkit mailbot-toolkit --room-rules=agents/resume_mailbot/rules.txt`


3. Now let's email the agent a resume!

4. Ask about the candidates who we've recieved resume's from. For example: 
`meshagent agents ask --room=resume --agent=meshagent.runner --input '{"prompt":"Do we have any applications from Parsa","model":"gpt-5.2","tools":[{"name":"database", "tables":["candidates"], "read_only": false}]}'`

From UI: 
{
  "prompt": "Add all of the jobs in the jobdescriptions folder to the open_roles table and mark Jesse Ezell as the hiring manager for each role.",$
  "tools": [
    {
      "name":"storage"
    },
    {
      "name":"database",
      "tables":["open_roles"],
      "read_only": false
    }
  ],
  "model":"gpt-5.2"
}


{
  "prompt": "Create a new record in the candidate_role_scores for how well Michael (Mike) Ulichny fits each of the open roles",
  "tools": [
    {
      "name":"storage"
    },
    {
      "name":"database",
      "tables":["open_roles", "candidates", "candidate_role_scores"],
      "read_only": false
    }
  ],
  "model":"gpt-5.2"
}

`meshagent agents ask --room=resume --agent=meshagent.runner --input '{"prompt":"What roles do we have open?","model":"gpt-5.2","tools":[{"name":"database", "tables":["open_roles"], "read_only": false}]}'`

`
## Notes / to do 
- anytime an email comes in add it to the candidates table. When a new record comes in this needs to trigger another agent who compares the candidate to each of the open roles in the open_roles table and then stores how close the match is in the 


## Done
1. Created all the tables setup_tables.py
2. Used assistant to research and create job descriptions
3. Used mailbot CLI and gave it a custom process resume tool which :
    a. Moves file to resumes folder
    b. Invokes meshagent.runner with the storage, web search, and database toolkit
    c. Has custom prompt in the room for modifying
4. Used in room taskrunner with database toolkits to update other tables like open_roles table and candidates table 
5. Used in room assistant to ask about the resumes / open roles and how well they match 