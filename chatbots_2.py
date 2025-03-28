"""Injected Chatbots"""

import ooze
from ollama import chat, ChatResponse

# Manually place items in the DI-graph
ooze.provide_static("llm", chat)


@ooze.provide("model")
class Model:
    """Interacts with an LLM model via Ollama"""

    def __init__(self, llm: callable, model_name: str):
        self.model_name = model_name
        self.llm = llm

    def chat(self, messages: list[dict]) -> ChatResponse:
        """Interact with the LLM"""
        return self.llm(self.model_name, messages)


class BaseChatbot:
    """A base class that encapsulates common chatbot functionality"""
    system_prompt = "You're a helpful assistant."

    def __init__(self, model: Model):
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self.model = model

    def chat(self, prompt: str):
        """Chat with the model"""
        self.messages.append({"role": "user", "content": prompt})
        response = self.model.chat(self.messages)
        if response.message.content:
            self.messages.append({"role": "assistant", "content": response.message.content})

    def text(self, prompt: str):
        """Return chat response to prompt as text"""
        self.chat(prompt)
        return self.messages[-1]["content"]


@ooze.provide("pirate_chatbot")
class PirateChatbot(BaseChatbot):
    """A pirate chatbot"""
    system_prompt = "You're a helpful assistant that talks like a pirate."


@ooze.provide("piglatin_chatbot")
class PigLatinChatbot(BaseChatbot):
    """A pig-latin chatbot"""
    system_prompt = "You're a helpful assistant that talks only in Pig-Latin."


@ooze.startup
def main(pirate_chatbot: BaseChatbot, piglatin_chatbot: BaseChatbot):
    """The main function of the script"""
    print(pirate_chatbot.text("How's your day in 10 words or less?"))
    print(piglatin_chatbot.text("How's your day in 10 words or less?"))


if __name__ == '__main__':
    ooze.run()
