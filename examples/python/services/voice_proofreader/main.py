from meshagent.livekit.agents.voice import Voicebot
from meshagent.api.services import ServiceHost
from meshagent.api import RequiredToolkit, RequiredSchema
from meshagent.tools import Toolkit
import asyncio
from meshagent.tools.document_tools import DocumentAuthoringToolkit, DocumentTypeAuthoringToolkit
from meshagent.agents.schemas.document import document_schema
from meshagent.tools.storage import StorageToolkit, SaveFileFromUrlTool

import livekit.agents.utils.http_context
import livekit.agents.cli.log

from meshagent.agents import Listener, ListenerContext
from typing import Optional
from meshagent.api import Element, JsonResponse
from meshagent.api.schema_document import Text

service = ServiceHost()

context = livekit.agents.utils.http_context._new_session_ctx()
livekit.agents.cli.log.setup_logging("ERROR", True, True)

@service.path("/agent")
class SampleVoiceAgentWithTools(Voicebot):
    def __init__(self):
        
        super().__init__(
            name="meshagent.livekit.agent_with_tools",
            title="voice agent with tools",
            description="sample agent that will respond to a query via voice",
            labels=[ "voice" ],
            auto_greet_prompt="hello",
            rules=[
                "You are a helpful assistant communicating through voice.",
                "When editing an element, do not also insert the element into the root, only change the attributes of the element",
                "output presentation names MUST have the extension .presenation or automatically add the extension if it is not provided",
                "when writing a document, open the document where the output will be written, then examine the contents of the reference file that was provided by the user with markitdown, then use tool calls to write content to the new document",
                "you MUST make at least 1 tool call that writes content into the document before closing it",
                "after opening a document you MUST immediately display it to the user",
                "prefer to add analysis to an output document",
                "each paragraph MUST be inserted into the document with a seperate tool call",
                "you MUST only include a single paragraph per tool call when inserting content",
                "if you close a document, it needs to be opened before you can update attributes or insert elements in it",
                "if you need to ask the user something, you should use the say tool before invoking the ask_user tool to let the user know why they are being asked something."
            ],
            requires=[
                RequiredToolkit(name="ui", tools=[ "ask_user", "display_document", "show_toast" ]),
                RequiredToolkit(name="meshagent.markitdown", tools=[ "markitdown_from_file" ]),
                RequiredSchema(name="presentation"),
            ],
            toolkits=[
                Toolkit(name="local", tools=[ SaveFileFromUrlTool() ]),
                DocumentAuthoringToolkit(),
                DocumentTypeAuthoringToolkit(
                    schema=document_schema,
                    document_type="presentation"
                ),
            ],
        )

        self.wait_for_synchronize = True
    
    async def on_listening_started(self, listener_context: ListenerContext):
        pass

    async def on_element_inserted(self, listener_context: ListenerContext, element: Element) -> bool:
        return False

    async def on_attribute_changed(self, listener_context: ListenerContext, element: Element, attribute: Optional[str]) -> bool:
        return False
    
    async def watch(self, session, output_path: str):
        room = self.room
        
        doc = await room.sync.open(path=output_path, create=True)
        try:
            listener_context = ListenerContext(
                document=doc,
                room=room,
                call_context=context,
            )
        
            change_queue = list[Element | Text]()
            
            def append_children(node:Element):
                for child in node.get_children():
                    if child not in change_queue:
                        change_queue.append([child])
                    if isinstance(child, Element):
                        append_children(child)
            
            if self.wait_for_synchronize == False:
                change_queue.append([doc.root])
                append_children(doc.root)
            else:
                await doc.synchronized


            await self.on_listening_started(listener_context=listener_context)
                
            wait_for_changes = asyncio.Future()
            
            @doc.on("inserted")
            def on_inserted(e: Element):
                if e not in change_queue:
                    change_queue.append([e])
                    append_children(e)
                
                if wait_for_changes.done() == False:
                    wait_for_changes.set_result(True)


            @doc.on("updated")
            def on_updated(e: Element, attribute: str):
                if e not in change_queue:                            
                    change_queue.append([e, attribute])
                    #
                    # append_children(e)
                
                if wait_for_changes.done() == False:
                    wait_for_changes.set_result(True)


            waiting_for_end = True
            while waiting_for_end:
                await wait_for_changes
            
                while len(change_queue) > 0:

                    change = change_queue.pop(0)
                   
                    content = change[0]
                    if len(change) > 1:
                        
                        element : Element = change[0]
                        attr = "line"
                        text = element.get_attribute("line", None)
                        if text == None:
                            attr = "title"
                            text = element.get_attribute("title", None)
                       
                        if text != None:

                            print(f"checking change {text}")

                            response = await self.room.agents.ask(agent="meshagent.schema_planner", arguments={"prompt":f"if this statement is wrong, respond with a corrected statement (correction) and respond like a good friend might about your disagreement (response). Limit your response to a maximum one sentence, the shorter the better: {text}","output_schema":{"type":"object","additionalProperties":False, "required": [ "response", "accuracy", "correction" ], "properties": { 
                                "accuracy" : { "type" : "string", "enum" : [ "inaccurate", "subjective", "accurate"] },
                                "response" : { "type" : "string" },
                                "correction" : { "type" : "string" },
                            } }})

                            if isinstance(response, JsonResponse):
                                data = response.json
                                print(response.json)
                            
                                if data["accuracy"] == "inaccurate":

                                    handle = session.say(data["response"])

                                    element.set_attribute(attr, data["correction"])

                                elif data["accuracy"] == "subjective":
                                    
                                    handle = session.say(data["response"])
                                    
                    
                            done = await self.on_attribute_changed(listener_context, content, change[1])
                            if done:
                                waiting_for_end = False

                    else:
                        done = await self.on_element_inserted(listener_context, content)
                        if done:
                            waiting_for_end = False
                        
                    if content in change_queue:
                        change_queue.remove(content)

                    
                
                wait_for_changes = asyncio.Future()
        except Exception as e:
            raise

        finally:

            await asyncio.sleep(5)
            await room.sync.close(output_path)
            
            return {}
    


    def create_session(self):
        session = super().create_session()

        def watch_done(task: asyncio.Task):
            try:
                task.result()
            except Exception as e:
                print("watch failed: {e}")

        asyncio.create_task(self.watch(session, "presentation.presentation"))
        return session

asyncio.run(service.run())
