import uuid
import asyncio
import sys
from bedrock_supervisor import (steak_supervisor_agent, steak_supervisor_agent_single)
from agent_squad.orchestrator import AgentSquad, AgentSquadConfig
from agent_squad.agents import (BedrockLLMAgent,
 BedrockLLMAgentOptions,
 AgentResponse,
 AgentCallbacks)

orchestrator = AgentSquad(options=AgentSquadConfig(
  LOG_AGENT_CHAT=True,
  LOG_CLASSIFIER_CHAT=True,
  LOG_CLASSIFIER_RAW_OUTPUT=True,
  LOG_CLASSIFIER_OUTPUT=True,
  LOG_EXECUTION_TIMES=True,
  MAX_RETRIES=3,
  MAX_MESSAGE_PAIRS_PER_AGENT=10,
  USE_DEFAULT_AGENT_IF_NONE_IDENTIFIED=True
),
  default_agent=BedrockLLMAgent(BedrockLLMAgentOptions(
    name="Default Agent",
    streaming=False,
    description="This is the default agent that handles general queries and tasks.",
  ))
)

orchestrator.add_agent(steak_supervisor_agent)
# orchestrator.add_agent(steak_supervisor_agent_single)

async def handle_request(_orchestrator: AgentSquad, _user_input: str, _user_id: str, _session_id: str):
    response: AgentResponse = await _orchestrator.route_request(_user_input, _user_id, _session_id)
    
    print("\nMetadata:")
    print(f"Selected Agent: {response.metadata.agent_name}")
    if response.streaming:
        print('Response:', response.output.content[0]['text'])
    else:
        print('Response:', response.output.content[0]['text'])

if __name__ == "__main__":
    USER_ID = "user123"
    SESSION_ID = str(uuid.uuid4())
    print("Welcome to the interactive Multi-Agent system. Type 'quit' to exit.")
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            print("Exiting the program. Goodbye!")
            sys.exit()
        # Run the async function
        asyncio.run(handle_request(orchestrator, user_input, USER_ID, SESSION_ID))
