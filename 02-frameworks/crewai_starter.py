from crewai import Agent, Task, Crew, Process
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

llm = LLM(model="ollama/mistral:latest", base_url="http://localhost:11434")


def create_linkedin_content_agent(topic: str) -> Crew:
    # Define the AI agent focused on generating LinkedIn content for AI pros
    content_agent = Agent(
        role="Content Creator for LinkedIn",
        goal=f"Generate engaging LinkedIn posts tailored for AI professionals on the topic: {topic}",
        verbose=False,
        llm=llm,
        backstory=(
            "You are a professional content writer specialized in crafting insightful and concise LinkedIn posts "
            "that resonate with AI professionals. Your style is clear, informative, and engaging."
        ),
    )

    # Define the task with dynamic topic interpolation
    task = Task(
        description=f"Write a LinkedIn post about: {topic}\n"
        "Focus on relevance to AI professionals, keep it concise (around 150-200 words), "
        "and include a call to action.",
        expected_output="A LinkedIn post text ready to be published.",
        agent=content_agent,
    )

    # Create the crew with the agent and task, sequential execution
    crew = Crew(
        agents=[content_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    return crew


if __name__ == "__main__":
    topic = (
        "The future of Large Language Models in AI"  # Example, can be dynamically set
    )
    crew = create_linkedin_content_agent(topic)
    result = crew.kickoff()
    print("Generated LinkedIn Post:\n", result)
