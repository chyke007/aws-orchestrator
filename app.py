import uuid
import asyncio
import sys
from chained import chain_agent 
from supervisor import supervisor_agent

from multi_agent_orchestrator.orchestrator import MultiAgentOrchestrator, OrchestratorConfig
from multi_agent_orchestrator.agents import (BedrockLLMAgent,
 BedrockLLMAgentOptions,
 AgentResponse,
 AgentCallbacks)

orchestrator = MultiAgentOrchestrator(options=OrchestratorConfig(
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

class BedrockLLMAgentCallbacks(AgentCallbacks):
    def on_llm_new_token(self, token: str) -> None:
        print(token, end='', flush=True)

football_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
    name="Football Insights Agent",
    description="Expert in football analysis, covering team strategies, player stats, match predictions, and historical comparisons.",
    callbacks=BedrockLLMAgentCallbacks()
))
orchestrator.add_agent(football_agent)

life_hack_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
    name="Life Hacks & Motivation Agent",
    description="Provides life hacks for efficiency, productivity tips, motivational insights, and goal-setting strategies for self-improvement.",
    callbacks=BedrockLLMAgentCallbacks()
))
orchestrator.add_agent(life_hack_agent)

#Add Chained agent
orchestrator.add_agent(chain_agent)

#Add Supervisor agent
orchestrator.add_agent(supervisor_agent)

async def handle_request(_orchestrator: MultiAgentOrchestrator, _user_input: str, _user_id: str, _session_id: str):
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
