import asyncio
import logging
from typing import Optional
from meshagent.otel import otel_config
from meshagent.api import Element
from meshagent.api.services import ServiceHost
from meshagent.agents import Listener, ListenerContext

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

otel_config(service_name="listener")
service = ServiceHost()


@service.path("/listener")
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


asyncio.run(service.run())
