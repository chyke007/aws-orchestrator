from multi_agent_orchestrator.agents import (BedrockLLMAgent,
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
            callbacks=BedrockLLMAgentCallbacks(),
            streaming=True
        ))
    
credit_card_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
            name="Credit Card Agent",
            description="Handles card issues, asks for customer card details when needed",
            callbacks=BedrockLLMAgentCallbacks(),
            streaming=True
        ))

supervisor_agent = SupervisorAgent(SupervisorAgentOptions(
    lead_agent=BedrockLLMAgent(BedrockLLMAgentOptions(
        name="Support Team Lead",
        description="Coordinates support inquiries"
    )),
    team=[credit_card_agent, ticket_agent]
))
