import requests
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class Agent:
    def __init__(self):
        self.llm=ChatGroq(
        model_name="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
        self.tools = {
    "search_wikipedia": self.search_wikipedia
}



    # Define the tool
    def search_wikipedia(self,query:str):
        """Search on Wikipedia and return the summary of the first result."""
        try:
            response = requests.get("https://en.wikipedia.org/w/api.php",  headers={
            "User-Agent": "AgenticAIProject/1.0 (yarasfand886@gmail.com)"
        },
            params={
                "action":"query",
                "prop":"extracts",
                "exintro":True,
                "explaintext":True,
                "titles":query,
                "format":"json"
                
                
            })
            if response.status_code != 200:
                return f"HTTP Error {response.status_code}"
            data = response.json()


            pages = data["query"]["pages"]
            page = next(iter(pages.values()))

            if "extract" in page and page["extract"]:
                return page["extract"]
            else:
                return "No result found."
        except Exception as e:
            return f"Error: {str(e)}"


    # Define the llm
    


    def call_llm(self,prompt:str):
        """Call the LLM and return the response."""
        try:
            response=self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"

    def parse_response(self,response: str):
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

    def run_agent(self,question: str, max_steps=5):
        history = f"Question: {question}\n"
        searched=False

        prompt_template = """
    You are an autonomous agent.

    You must respond in this format:

    Thought: your reasoning
    Action: search_wikipedia | finish
    Action Input: input for the action
    Rule: You must call search_wikipedia at least once before finish.

    """

        for step in range(max_steps):
            prompt = prompt_template + history
            response = self.call_llm(prompt)
            print("\nLLM Response:\n", response)

            thought, action, action_input = self.parse_response(response)

            # if action == "finish":
            #     if not searched:
            #         observation = "You must call search_wikipedia at least once before finish."

            #         print("\nObservation", observation)
            #     else:
            #         print("\nFinal Answer:", action_input)
            #         return action_input

            

            # if action == "search_wikipedia":
            #     observation = search_wikipedia(action_input)
            #     if observation and observation !="No result found.":
            #         searched = True
            #     print("Observation:\n", observation[:500])
            # else:
            #     observation = "Invalid action."

            #Tools registry
        
            allowed_actions = set(self.tools.keys())|{"finish"}

            if action not in allowed_actions:
                observation = f"Invalid action. Allowed actions are {allowed_actions}."
            elif action == "finish":
                if not searched:
                    observation = "You must call search_wikipedia at least once before finish."

                else:
                    print("\nFinal Answer:", action_input)
                    return action_input
            
            else:
                observation = self.tools[action](action_input)
                if "Error" not in observation and observation != "No result found.":
                    searched = True


            history += f"""
    Thought: {thought}
    Action: {action}
    Action Input: {action_input}
    Observation: {observation}
    """

        print("Max steps reached.")



if __name__ == "__main__":
    agent = Agent()
    agent.run_agent("Who directed Inception and what other movie did he direct?")