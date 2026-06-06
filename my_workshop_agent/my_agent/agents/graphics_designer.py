from google.adk.agents import Agent

from ..rate_limit import throttle_before_model

graphic_designer = Agent(
    name="graphic_designer",
    model="gemini-3.5-flash",
    mode="single_turn",
    before_model_callback=throttle_before_model,
    description="Creates visual briefs for marketing campaigns.",
    instruction="""You are a creative art director.
When given a product or campaign brief, produce:
    - A visual concept description (color palette, mood, style)
    - Hero image / thumbnail idea with composition notes
    - Typography and layout recommendations
Write as a detailed brief a designer could hand off to a studio.""",
)