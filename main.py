from ast import List
from email import message
import json
from openai import OpenAI
from dotenv import load_dotenv
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)
from pypdf import PdfReader
import gradio as gr
import requests
import os


class Main:
    def __init__(self):
        load_dotenv(override=True)
        print("initiated!")
        self.openai = OpenAI(base_url="http://localhost:11434/v1", api_key="anything")
        print("OpenAI instance created!")

    def extractPdf(self, url: str):
        resp = PdfReader(url)
        profile_details = ""
        for page in resp.pages:
            text = page.extract_text()
            profile_details += text
        self.profile_details = profile_details

    def sendPushNotififications(self, message):
        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": os.getenv(
                    "PUSHOVER_TOKEN"
                ),  # 🛠 FIXED: should be PUSHOVER_TOKEN
                "user": os.getenv("PUSHOVER_USER"),
                "message": message,
            },
        )
        return {"recorded": "OK"}

    def handleToolCalls(self, toolCalls):
        results = []
        for toolCall in toolCalls:
            print(toolCall.function.name)
            arguments = json.loads(toolCall.function.arguments)
            message = ""
            result = {}
            if toolCall.function.name == "log_unanswered_question":
                message = f"User asked: {arguments.get('question')}. But I don't know the answer to this question."
            elif toolCall.function.name == "log_user_details":
                name = arguments.get("name") or "Not Provided"
                email = arguments.get("email") or "Not Provided"
                message = f"User wants to share details. Name: {name}, Email: {email}"
            if message:
                result = self.sendPushNotififications(message)

            results.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": toolCall.id,
                }
            )
        print(results)
        return results

    def chat(self, message, history):
        name = "Samdominic"
        system_prompt = f"You are {name}. You should act like {name}. You can answer by using the profile details."
        system_prompt += f"\n\n{name}'s profile details: {self.profile_details}. You can also answer general questions or engage in casual conversation."
        system_prompt += f"\n\nIf you don't know the answer to a question about {name}, then only use this tool `log_unanswered_question`."
        system_prompt += f"\n\nIf the user intrested to keep in touch and share details , then only use this tool `log_user_details`."
        system_prompt += f"\n\nOtherwise, continue talking normally as {name}."

        messages: list[ChatCompletionMessageParam] = (
            [{"role": "system", "content": system_prompt}]
            + history
            + [{"role": "user", "content": message}]
        )
        done = False
        while not done:
            resp = self.openai.chat.completions.create(
                model="llama3.2", messages=messages, tools=self.tools
            )
            print(resp.choices[0].finish_reason)
            if resp.choices[0].finish_reason == "tool_calls":
                results = self.handleToolCalls(resp.choices[0].message.tool_calls)
                messages.append(resp.choices[0].message)
                messages.extend(results)
            else:
                done = True
        return resp.choices[0].message.content

    def loadTools(self):
        print("loading tools...")
        log_unanswered_question: ChatCompletionToolParam = {
            "type": "function",
            "function": {
                "name": "log_unanswered_question",
                "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The questions you could not answer.",
                        },
                    },
                    "required": ["question"],
                    "additionalProperties": False,
                },
            },
        }

        log_user_details: ChatCompletionToolParam = {
            "type": "function",
            "function": {
                "name": "log_user_details",
                "description": ("Always use this tool if user wants to keep in touch."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the user",
                        },
                        "email": {
                            "type": "string",
                            "description": "Name of the email.",
                        },
                    },
                    "required": ["email"],
                    "additionalProperties": False,
                },
            },
        }

        self.tools = [log_unanswered_question, log_user_details]


if __name__ == "__main__":
    main = Main()
    main.loadTools()
    main.extractPdf("./assets/Profile.pdf")
    gr.ChatInterface(main.chat, type="messages").launch()
    # main.questionAndAnswerToAI()

    # def questionAndAnswerToAI(self):
    #     openai = OpenAI(base_url="http://localhost:11434/v1", api_key="")
    #     resp = openai.chat.completions.create(
    #         model="llama3.2",
    #         messages=[{"role": "user", "content": "Can you ask question about India?"}],
    #     )
    #     question = resp.choices[0].message.content
    #     print("question:/n" + question)
    #     resp1 = openai.chat.completions.create(
    #         model="llama3.2", messages=[{"role": "user", "content": question}]
    #     )
    #     answer = resp1.choices[0].message.content
    #     print("answer:/n", answer)
