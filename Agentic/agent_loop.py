import requests
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Define the tool
def seach_wikipedia(query:str):
    """Search on Wikipedia and return the summary of the first result."""
    try:
        response = requests.get("https://en.wikipedia.org/w/api.php",
        params={
            "action":"query",
            "list":"search",
            "srsearch":query,
            "format":"json"
        })
        data = response.json()


        if data["query"]["search"]:
            return data["query"]["search"][0]["snippet"]
        else:
            return "No result found."
    except Exception as e:
        return f"Error: {str(e)}"


# Define the llm
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)


def call_llm(prompt:str):
    """Call the LLM and return the response."""
    try:
        response=llm.invoke(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def parse_response(response: str):
    lines = response.split("\n")
    thought = ""
    action = ""
    action_input = ""

    for line in lines:
        if line.startswith("Thought:"):
            thought = line.replace("Thought:", "").strip()
        elif line.startswith("Action:"):
            action = line.replace("Action:", "").strip()
        elif line.startswith("Action Input:"):
            action_input = line.replace("Action Input:", "").strip()

    return thought, action, action_input

def run_agent(question: str, max_steps=5):
    history = f"Question: {question}\n"

    prompt_template = """
You are an autonomous agent.

You must respond in this format:

Thought: your reasoning
Action: search_wikipedia or finish
Action Input: input for the action

"""

    for step in range(max_steps):
        prompt = prompt_template + history
        response = call_llm(prompt)

        print("\nLLM Response:\n", response)

        thought, action, action_input = parse_response(response)

        if action == "finish":
            print("\nFinal Answer:", action_input)
            return action_input

        if action == "search_wikipedia":
            observation = seach_wikipedia(action_input)
        else:
            observation = "Invalid action."

        history += f"""
Thought: {thought}
Action: {action}
Action Input: {action_input}
Observation: {observation}
"""

    print("Max steps reached.")



if __name__ == "__main__":
    run_agent("Who directed Inception and what other movie did he direct?")
