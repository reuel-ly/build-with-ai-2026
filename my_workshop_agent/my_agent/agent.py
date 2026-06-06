from google.adk.agents import Agent

from .agents import researcher, graphic_designer, writer
from .rate_limit import throttle_before_model

root_agent = Agent(
    name="marketing_orchestrator",
    model="gemini-3.5-flash",
    description="Orchestrates the researcher, graphic designer, and writer.",
    before_model_callback=throttle_before_model,
    instruction="""You are a marketing project lead.
For any product or campaign request:
   1. Ask the researcher to analyse relevant trends.
   2. Pass the research to the writer to produce copy.
   3. Ask the graphic designer to create a visual brief.
   4. Present all three outputs together as a cohesive campaign package.
Always coordinate all three agents before responding.""",
    sub_agents=[
        researcher,
        graphic_designer,
        writer,
    ],
)