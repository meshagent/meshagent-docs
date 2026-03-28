# Chat and Voice Agent with Custom Tools

Chat & voice agents built with **custom tools**. 

In this example we create a custom TaskTracker toolkit that allows the agent to write and read tasks to the Room database. 

To do this we will add a new room_setup.py file that creates a table for the tasks when the room starts up. We also create a tasks toolkits with two custom tools to **WriteTask** and **GetTasks** from the database. 

This is a simple example of adding tasks, to create a more useful task writer we'd want to add date information and other metadata to better track and filter tasks. This example is mainly to demonstrate writing to room storage and adding custom tools to our chat agent.

Remember to run room_setup.py before running main.py that way our task table is added to the room before the agent joins it.