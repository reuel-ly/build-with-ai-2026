from google.adk.agents import Agent

from ..rate_limit import throttle_before_model

researcher = Agent(
    name="researcher",
    model="gemini-3.5-flash",
    mode="single_turn",
    before_model_callback=throttle_before_model,
    description="Researches marketing trends for a given product or industry.",
    instruction="""You are a senior market research analyst.
When given a product or industry, provide:
    - Current marketing trends (3-5 bullet points)
    - Key competitor messaging themes
    - Audience pain points and motivators
Be concise, specific, and actionable.""",
)