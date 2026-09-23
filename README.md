# 🤖 LearnAgent

A beginner-friendly **AI computer agent** built with Python and the OpenAI API.

This project demonstrates how to build an AI agent from scratch, starting with a simple API connection and gradually giving the AI the ability to interact with the user's computer.

The current agent can:

- 💬 Have conversations with the user
- 🧠 Understand natural-language requests
- 🔧 Decide when to use a tool
- 🧮 Control the Windows Calculator
- 📖 Read the Calculator result from the Windows UI
- 🧠 Maintain conversation history
- 🖥️ Provide a graphical interface using Tkinter

This project is designed as a learning project for understanding **AI agents, function calling, computer automation, and tool-based AI systems**.

---

# 📁 Project Structure

```text
LearnAgent/
│
├── .env
├── .gitignore
│
├── calculator.py
├── agent.py
├── app.py
│
├── testapi.py
└── testagent.py
```

> `testapi.py` and `testagent.py` are development/testing files used while learning how the agent works. They are not required for the final GUI application, but are kept in the project to demonstrate the development process.

---

# 🧠 How the Agent Works

The project is built in several layers:

```text
                    User
                     │
                     ▼
              ┌─────────────┐
              │   app.py    │
              │     GUI     │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │  agent.py   │
              │  AI Agent   │
              └──────┬──────┘
                     │
                Tool call
                     │
                     ▼
            ┌─────────────────┐
            │ calculator.py   │
            │ Calculator Tool │
            └────────┬────────┘
                     │
                     ▼
            Windows Calculator
                     │
                     ▼
                  Result
                     │
                     ▼
                   AI
                     │
                     ▼
                  User
```

The important concept is that the AI does not directly control the computer.

Instead:

1. The user gives the AI a request.
2. The AI decides whether a tool is required.
3. The AI generates a function call.
4. Python executes the function.
5. The tool interacts with the computer.
6. The result is returned to the AI.
7. The AI produces the final response.

---

# 🛠️ Requirements

## Software

You will need:

- Windows
- Python 3.12 or compatible Python version
- Git
- VS Code or another code editor
- An OpenAI API key

The project currently uses:

- OpenAI Python SDK
- `python-dotenv`
- `pyautogui`
- `pywinauto`
- Tkinter

---

# 1️⃣ Clone the Repository

Clone the repository:

```powershell
git clone https://github.com/YOUR_USERNAME/LearnAgent.git
```

Enter the project:

```powershell
cd LearnAgent
```

---

# 2️⃣ Create a Python Environment

Using Conda:

```powershell
conda create -n calcAgent python=3.12
```

Activate it:

```powershell
conda activate calcAgent
```

You should now see something similar to:

```text
(calcAgent) PS C:\Users\...\LearnAgent>
```

---

# 3️⃣ Install Dependencies

Install the required Python packages:

```powershell
pip install openai python-dotenv pyautogui pywinauto
```

---

# 4️⃣ Create the `.env` File

The agent needs an OpenAI API key.

Create a file named:

```text
.env
```

in the root of the project:

```text
LearnAgent/
│
├── .env
├── agent.py
├── calculator.py
└── app.py
```

Put your API key inside:

```text
OPENAI_API_KEY=your_api_key_here
```

For example:

```text
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

Replace the example value with your actual API key.

## ⚠️ Security Warning

**Never upload your `.env` file to GitHub.**

The `.gitignore` file should contain:

```gitignore
.env
__pycache__/
```

This prevents Git from tracking your API key.

If an API key is accidentally uploaded to GitHub, revoke/rotate the key immediately.

---

# 5️⃣ Test the OpenAI API

Before building the agent, we first verify that Python can communicate with the OpenAI API.

Create:

```text
testapi.py
```

Use:

```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-luna",
    input="Say hello and tell me that the API is working."
)

print(response.output_text)
```

Run:

```powershell
python testapi.py
```

You should receive a response from the AI.

For example:

```text
Hello! The OpenAI API is working correctly.
```

If this works, your API connection is ready.

---

# 6️⃣ Test Windows Calculator Automation

Before connecting AI to the calculator, we first make sure Python can control Windows Calculator.

The project uses:

```text
PyAutoGUI
```

to control the keyboard and:

```text
pywinauto
```

to read the Calculator's user interface.

The basic workflow is:

```text
Python
   ↓
Open Windows Calculator
   ↓
Enter expression
   ↓
Press Enter
   ↓
Read Calculator display
```

The calculator functionality is contained in:

```text
calculator.py
```

The main function is:

```python
use_calculator(expression)
```

For example:

```python
use_calculator("400 / 33 + 5")
```

Windows Calculator performs the calculation and returns the result to Python.

---

# 7️⃣ Test the AI Agent Without the GUI

Before building the GUI, we test the agent directly from the terminal.

Create:

```text
testagent.py
```

Use:

```python
from agent import ask_agent


while True:

    message = input("\nYou: ")

    if message.lower() == "exit":
        break

    answer = ask_agent(message)

    print("\nAgent:", answer)
```

Run:

```powershell
python testagent.py
```

You can now talk to the agent from the terminal.

For example:

```text
You: Calculate 400 divided by 33 and then add 5
```

The AI should understand the request and generate a tool call similar to:

```text
use_calculator("400 / 33 + 5")
```

Python then executes the tool.

Windows Calculator opens and performs the calculation.

The result is returned to the AI.

The AI then produces the final response.

---

# 8️⃣ Understanding Function Calling

The most important part of this project is **function calling**.

The AI is given a tool definition:

```python
tools = [
    {
        "type": "function",
        "name": "use_calculator",
        ...
    }
]
```

This tells the AI:

> You have access to a tool called `use_calculator`.

The AI can then decide:

```text
User:
Calculate 400 / 33 + 5

AI:
I need the calculator tool.
```

It generates a function call:

```text
use_calculator
expression = "400 / 33 + 5"
```

Python receives the request and executes:

```python
use_calculator("400 / 33 + 5")
```

The result is then returned to the AI.

This creates the fundamental agent loop:

```text
User
 ↓
AI
 ↓
Tool decision
 ↓
Python function
 ↓
Computer
 ↓
Tool result
 ↓
AI
 ↓
Final response
```

---

# 9️⃣ Run the Complete GUI Application

Once the API and agent are working, run:

```powershell
python app.py
```

A graphical interface will open.

You can type:

```text
Calculate 12345 * 678
```

The agent will:

1. Understand the request
2. Decide that the calculator is required
3. Call `use_calculator()`
4. Open Windows Calculator
5. Enter the calculation
6. Read the result
7. Return the result to the AI
8. Display the answer in the GUI

---

# 🖥️ Current Architecture

The final application consists of three main components.

## `app.py`

Responsible for the graphical interface.

```text
User
 ↓
Tkinter GUI
```

---

## `agent.py`

Responsible for the AI logic.

```text
User request
 ↓
OpenAI
 ↓
Tool decision
 ↓
Tool execution
 ↓
Final response
```

It also stores the conversation history so the agent can understand follow-up requests.

---

## `calculator.py`

Responsible for computer interaction.

```text
AI tool call
 ↓
Python
 ↓
PyAutoGUI
 ↓
Windows Calculator
 ↓
Pywinauto
 ↓
Result
```

---

# 🔄 Example Conversation

The agent can understand natural language rather than requiring a specific command format.

### Example 1

```text
You:
Calculate 400 divided by 33 and then add 5
```

The AI can transform the request into:

```text
400 / 33 + 5
```

and send it to the Calculator tool.

---

### Example 2

```text
You:
Calculate 500 * 20
```

Then:

```text
You:
Now divide that by 4
```

Because the agent maintains conversation history, it can understand that:

```text
500 * 20 = 10000

10000 / 4 = 2500
```

---

# 🔐 Security

The API key is stored in:

```text
.env
```

and loaded using:

```python
load_dotenv()
```

The key is never hard-coded into the Python source code.

Make sure `.gitignore` contains:

```gitignore
.env
__pycache__/
```

Never commit:

```text
.env
```

to GitHub.

---

# 📚 What This Project Teaches

This project demonstrates several fundamental concepts behind AI agents:

### 1. LLM API

Connecting Python to an AI model.

### 2. Prompting

Giving the AI instructions about how it should behave.

### 3. Function Calling

Giving the AI access to external functions.

### 4. Tools

Allowing the AI to interact with the outside world.

### 5. Computer Automation

Using Python to interact with Windows applications.

### 6. UI Automation

Reading information directly from an application's user interface.

### 7. Agent Memory

Maintaining conversation history between requests.

### 8. GUI Development

Building an interface for the AI using Tkinter.

---

# 🚀 Future Development

This project is intentionally being developed step-by-step.

Potential future tools include:

```text
AI Agent
│
├── 🧮 Calculator
│
├── 📁 File System
│
├── 💻 Computer Control
│
├── 🌐 Web Search
│
└── 💬 WhatsApp
```

The long-term goal is to build an agent capable of receiving messages through WhatsApp, understanding the request, deciding what action is required, and asking for human approval before performing sensitive actions.

For example:

```text
Downline:
Please send today's command to Group A.

             ↓

          AI Agent

             ↓

       Understand request

             ↓

       Prepare message

             ↓

       Human approval

             ↓

          Approved

             ↓

       Send WhatsApp
```

This project therefore serves as the foundation for learning how to build more advanced **tool-using AI agents and computer automation systems**.

---

# 📌 Development Philosophy

The project is intentionally built without immediately relying on large agent frameworks.

Instead, the core mechanism is implemented explicitly:

```text
LLM
 ↓
Function Call
 ↓
Python
 ↓
Tool
 ↓
Result
 ↓
LLM
```

Understanding this mechanism first makes it much easier to understand frameworks such as LangChain, LangGraph, and other agent frameworks later.

---

# 🧑‍💻 Author

Built as a hands-on learning project for exploring:

- Artificial Intelligence
- AI Agents
- Python
- OpenAI API
- Function Calling
- Computer Automation
- Windows UI Automation
- GUI Development
- Git & GitHub
