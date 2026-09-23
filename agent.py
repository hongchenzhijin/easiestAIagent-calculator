import json

from openai import OpenAI
from dotenv import load_dotenv

from calculator import use_calculator


load_dotenv()

client = OpenAI()


# --------------------------------------------------
# Conversation memory
# --------------------------------------------------

conversation = []


# --------------------------------------------------
# Tools available to the AI
# --------------------------------------------------

tools = [
    {
        "type": "function",
        "name": "use_calculator",
        "description": (
            "Use the Windows Calculator application on the user's PC "
            "to perform arithmetic calculations. "
            "Always use this tool when the user asks you to calculate "
            "a mathematical expression."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "A mathematical expression using numbers and "
                        "basic operators such as +, -, *, /, %, "
                        "and parentheses."
                    )
                }
            },
            "required": ["expression"],
            "additionalProperties": False
        },
        "strict": True
    }
]


# --------------------------------------------------
# Agent instructions
# --------------------------------------------------

SYSTEM_PROMPT = """
You are a helpful computer AI agent.

You have access to tools that can interact with the user's computer.

Rules:

1. Understand the user's request carefully.
2. When arithmetic calculation is requested, use the
   use_calculator tool instead of calculating it yourself.
3. Explain the result clearly after the tool finishes.
4. You may have a normal conversation without using tools.
5. Never claim that you performed an action unless the tool
   actually performed it successfully.
6. If a tool returns an error, explain the error honestly.
"""


# --------------------------------------------------
# Agent
# --------------------------------------------------

def ask_agent(user_message):

    # Add user message to memory
    conversation.append({
        "role": "user",
        "content": user_message
    })

    while True:

        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions=SYSTEM_PROMPT,
            tools=tools,
            input=conversation
        )

        # Add AI response to conversation
        conversation.extend(response.output)

        tool_was_used = False

        # --------------------------------------------------
        # Process tool calls
        # --------------------------------------------------

        for item in response.output:

            if item.type != "function_call":
                continue

            tool_was_used = True

            if item.name == "use_calculator":

                arguments = json.loads(item.arguments)

                expression = arguments["expression"]

                result = use_calculator(expression)

                conversation.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": str(result)
                })

        # --------------------------------------------------
        # If no tool was requested, we have the final answer
        # --------------------------------------------------

        if not tool_was_used:

            return response.output_text