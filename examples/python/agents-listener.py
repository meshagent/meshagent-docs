import asyncio
from typing import Optional
from meshagent.api import Element
from meshagent.agents import Listener, ListenerContext, connect_development_agent


class SampleListener(Listener):
    def __init__(self):
        # We want the listener to only deliver new changes, so we'll tell it to start listening after the document has been synchronized
        super().__init__(
            name="samples.listener",
            title="sample listener",
            description="a sample agent that listens to a document",
            wait_for_synchronize=True,
        )

    # this method will be called when we start listening
    async def on_listening_started(self, listener_context: ListenerContext):
        print("The listener has started")

    # this method will be called any time a new element is inserted
    async def on_element_inserted(
        self, listener_context: ListenerContext, element: Element
    ) -> bool:
        print(f"an element was inserted {element.tag_name}")

        # If we return True, the listener will stop, returning False keeps the listener active
        return False

    # this method will be called any time an attribute is updated
    async def on_attribute_changed(
        self,
        listener_context: ListenerContext,
        element: Element,
        attribute: Optional[str],
    ) -> bool:
        print(
            f"an attribute was changed {element.tag_name} {attribute}={element[attribute]}"
        )

        # If we return True, the listener will stop, returning False keeps the listener active
        return False


async def main():
    room_name = "examples"

    # start our agent in developer mode, it will connect to the room and be available immediately from the admin console UI
    await connect_development_agent(room_name=room_name, agent=SampleListener())


asyncio.run(main())
