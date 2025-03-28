"""A simple web searching agent"""
import sys

import ooze
import requests
from ollama import chat, ChatResponse

# Manually place items in the DI-graph
ooze.provide_static("llm", chat)
ooze.provide_static("http_post", requests.post)
ooze.provide_static("log", print)


@ooze.provide("model")
class Model:
    """Interacts with an LLM model via Ollama"""

    def __init__(self, llm: callable, model_name: str):
        self.model_name = model_name
        self.llm = llm

    def chat(self, messages: list[dict], tools: list) -> ChatResponse:
        """Send messages and tools to LLM and wait for response"""
        return self.llm(self.model_name, messages, tools=tools)


@ooze.provide("agent")
class Agent:
    """A simple agent that searches the Internet to answer the prompt"""
    system_prompt = """
    You are a helpful assistant.  Use the tools at your disposal to answer questions.  Use the information returned
    from the tool to answer the question.  Keep you answers short and sweet.  Do not include any disclaimers in your
    answers.
    """

    def __init__(self, model: Model, http_post: callable, log: callable, SERPAPI_API_KEY: str):
        self.model = model
        self.http_post = http_post
        self.log = log
        self.tools = {"search_tool": self.search_tool}
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self.api_key = SERPAPI_API_KEY

    def chat(self, prompt: str = None) -> ChatResponse:
        """Chat with the model"""
        if prompt:
            self.messages.append({"role": "user", "content": prompt})
        response = self.model.chat(self.messages, list(self.tools.values()))
        if response.message.content:
            self.messages.append({"role": "assistant", "content": response.message.content})
        return response

    def answer(self, prompt: str):
        """Use the tool(s) answer the user's prompt."""
        chat_count = 0
        while True:
            response = self.chat(prompt)
            chat_count += 1
            if chat_count > 10:
                return "Sorry, I was unable to answer your question at this time."
            for tool_call in response.message.tool_calls or []:
                tool_name = tool_call.function.name
                tool_to_call = self.tools[tool_name]
                result = tool_to_call(**tool_call.function.arguments)
                self.messages.append({"role": "tool", "name": tool_name, "content": result})
                prompt = None
            if response.message.tool_calls:
                continue
            else:
                return self.messages[-1]["content"].strip()

    def search_tool(self, query: str):
        """
        Search the Internet for information.
        Args:
            query: What to search for.
        Returns:
            Information obtained from the Internet.
        """
        url = f"https://google.serper.dev/search"
        payload = {"q": query}
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }
        self.log(f"Search tool engaged with query: {query}")
        response = self.http_post(url, headers=headers, json=payload, allow_redirects=False)
        search_results = response.json().get("organic", [])
        return "\n".join([r.get("snippet", '') for r in search_results])


@ooze.magic
def main(prompt: str, agent: Agent, log: callable, PWD: str):
    """The main function of the script"""
    log(f"Running from {PWD}")
    log(f"Prompt: {prompt}")
    response = agent.answer(prompt)
    log(f"Response: {response}")


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:])
    main(prompt)
