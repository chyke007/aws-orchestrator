from agent_squad.agents import (BedrockLLMAgent,
                                             BedrockLLMAgentOptions,
                                             AgentCallbacks,
                                             SupervisorAgent,
                                             SupervisorAgentOptions)


class BedrockLLMAgentCallbacks(AgentCallbacks):
    def on_llm_new_token(self, token: str) -> None:
        print(token, end='', flush=True)


ticket_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
            name="Ticket Agent",
            description="Creates a ticket about customer issues",
            callbacks=BedrockLLMAgentCallbacks()
        ))
    
credit_card_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
            name="Credit Card Agent",
            description="Handles card issues, asks for customer card details when needed",
            callbacks=BedrockLLMAgentCallbacks()
        ))

supervisor_agent = SupervisorAgent(SupervisorAgentOptions(
    name="Supervisor Agent",
    description="Coordinates support inquiries",
    lead_agent=BedrockLLMAgent(BedrockLLMAgentOptions(
        name="Support Team Lead",
        description="Coordinates support inquiries"
    )),
    team=[credit_card_agent, ticket_agent]
))
