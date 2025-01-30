from multi_agent_orchestrator.agents import (BedrockLLMAgent,
                                             BedrockLLMAgentOptions,
                                             AgentCallbacks, ChainAgent, ChainAgentOptions)

class BedrockLLMAgentCallbacks(AgentCallbacks):
    def on_llm_new_token(self, token: str) -> None:
        print(token, end='', flush=True)


research_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
    name="Research Agent",
    description="Analyzes and validates the given content, expanding on relevant topics and ensuring accuracy.",
    callbacks=BedrockLLMAgentCallbacks(),
    streaming=True
))

analysis_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
    name="Analysis Agent",
    description="Extracts key insights, trends, and relevant points from the content, identifying core themes.",
    callbacks=BedrockLLMAgentCallbacks(),
    streaming=True
))

report_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
    name="Report Agent",
    description="Creates a structured report summarizing the research findings and key insights into a coherent format.",
    callbacks=BedrockLLMAgentCallbacks(),
    streaming=True
))


options = ChainAgentOptions(
    name='ChainAnalysisAgent',
    description='A research, analayis and report generation chain of agents that takes user research input and gives a final report after proper research & analysis',
    agents=[research_agent, analysis_agent, report_agent],
    default_output='The chain processing encountered an issue.',
    save_chat=True
)

chain_agent = ChainAgent(options)
