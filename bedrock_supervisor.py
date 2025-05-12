import os
from dotenv import load_dotenv

from agent_squad.agents import (
    BedrockLLMAgent,
    BedrockLLMAgentOptions,
    AmazonBedrockAgent,
    AmazonBedrockAgentOptions,
    AgentCallbacks,
    SupervisorAgent,
    SupervisorAgentOptions
)

# Load environment variables from .env file
load_dotenv()


class BedrockAgentCallbacks(AgentCallbacks):
    def on_llm_new_token(self, token: str) -> None:
        print(token, end='', flush=True)


reservation_agent = AmazonBedrockAgent(AmazonBedrockAgentOptions(
    name="Steakhouse Reservation Agent",
    description="Agent in charge of a Steakhouse reservation bookings",
    callbacks=BedrockAgentCallbacks(),
    streaming=True,
    agent_id=os.getenv("RESERVATION_AGENT_ID"),
    agent_alias_id=os.getenv("RESERVATION_AGENT_ALIAS_ID")
))

hr_agent = AmazonBedrockAgent(AmazonBedrockAgentOptions(
    name="Steakhouse hr agent",
    description="Agent in charge of a Steakhouse Hr department",
    callbacks=BedrockAgentCallbacks(),
    streaming=True,
    agent_id=os.getenv("HR_AGENT_ID"),
    agent_alias_id=os.getenv("HR_AGENT_ALIAS_ID")
))

shortlet_agent = AmazonBedrockAgent(AmazonBedrockAgentOptions(
    name="Steakhouse shortlet agent",
    description="Agent in charge of a Steakhouse shortlet bookings",
    callbacks=BedrockAgentCallbacks(),
    streaming=True,
    agent_id=os.getenv("SHORTLET_AGENT_ID"),
    agent_alias_id=os.getenv("SHORTLET_AGENT_ALIAS_ID")
))

ticket_agent = AmazonBedrockAgent(AmazonBedrockAgentOptions(
    name="Steakhouse ticket agent",
    description="Agent in charge of a Steakhouse ticketing system",
    callbacks=BedrockAgentCallbacks(),
    streaming=True,
    agent_id=os.getenv("TICKET_AGENT_ID"),
    agent_alias_id=os.getenv("TICKET_AGENT_ALIAS_ID")
))

steak_supervisor_agent = SupervisorAgent(SupervisorAgentOptions(
    name="Steakhouse supervisor agent",
    description="Supervisor agent in charge of a Steakhouse enterprise, acts as the supervisor agent",
    lead_agent=BedrockLLMAgent(BedrockLLMAgentOptions(
        name="Supervisor",
        description="Supervisor agent in charge of a Steakhouse enterprise, acts as the supervisor agent",
        model_id=os.getenv("MODEL_ID")
    )),
    team=[reservation_agent, hr_agent, shortlet_agent, ticket_agent]
))

steak_supervisor_agent_single = AmazonBedrockAgent(AmazonBedrockAgentOptions(
    name="Steakhouse supervisor agent - Bedrock",
    description="Supervisor agent in charge of a Steakhouse enterprise, acts as the supervisor agent",
    callbacks=BedrockAgentCallbacks(),
    streaming=True,
    agent_id=os.getenv("SUPERVISOR_AGENT_ID"),
    agent_alias_id=os.getenv("SUPERVISOR_AGENT_ALIAS_ID")
))

