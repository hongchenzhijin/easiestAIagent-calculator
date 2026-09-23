import tkinter as tk
from tkinter import scrolledtext
import threading

from agent import ask_agent


class AgentApp:

    def __init__(self, root):

        self.root = root

        root.title("AI Computer Agent")
        root.geometry("850x700")

        # --------------------------------------------
        # Chat area
        # --------------------------------------------

        self.chat = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            state="disabled"
        )

        self.chat.pack(
            fill=tk.BOTH,
            expand=True,
            padx=15,
            pady=(15, 10)
        )

        # --------------------------------------------
        # Status
        # --------------------------------------------

        self.status = tk.Label(
            root,
            text="● Agent ready",
            anchor="w",
            font=("Segoe UI", 9)
        )

        self.status.pack(
            fill=tk.X,
            padx=15
        )

        # --------------------------------------------
        # Input area
        # --------------------------------------------

        input_frame = tk.Frame(root)

        input_frame.pack(
            fill=tk.X,
            padx=15,
            pady=15
        )

        self.input_box = tk.Entry(
            input_frame,
            font=("Segoe UI", 12)
        )

        self.input_box.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            ipady=10
        )

        self.input_box.bind(
            "<Return>",
            self.send_message
        )

        self.send_button = tk.Button(
            input_frame,
            text="Send",
            font=("Segoe UI", 11),
            command=self.send_message
        )

        self.send_button.pack(
            side=tk.RIGHT,
            padx=(10, 0),
            ipadx=20,
            ipady=7
        )

        # --------------------------------------------
        # Welcome message
        # --------------------------------------------

        self.add_message(
            "Agent",
            "Hello! I'm your computer agent.\n"
            "I can use the Windows Calculator for you."
        )

        self.input_box.focus()

    # --------------------------------------------
    # Display message
    # --------------------------------------------

    def add_message(self, sender, message):

        self.chat.config(state="normal")

        self.chat.insert(
            tk.END,
            f"{sender}\n",
            "sender"
        )

        self.chat.insert(
            tk.END,
            f"{message}\n\n"
        )

        self.chat.config(state="disabled")

        self.chat.see(tk.END)

    # --------------------------------------------
    # Send message
    # --------------------------------------------

    def send_message(self, event=None):

        message = self.input_box.get().strip()

        if not message:
            return

        self.input_box.delete(0, tk.END)

        self.add_message(
            "You",
            message
        )

        self.status.config(
            text="● Agent is working..."
        )

        self.send_button.config(
            state="disabled"
        )

        # Run AI in background thread
        threading.Thread(
            target=self.process_message,
            args=(message,),
            daemon=True
        ).start()

    # --------------------------------------------
    # Process request
    # --------------------------------------------

    def process_message(self, message):

        try:

            answer = ask_agent(message)

            self.root.after(
                0,
                self.show_answer,
                answer
            )

        except Exception as error:

            self.root.after(
                0,
                self.show_answer,
                f"Error: {error}"
            )

    # --------------------------------------------
    # Show answer
    # --------------------------------------------

    def show_answer(self, answer):

        self.add_message(
            "Agent",
            answer
        )

        self.status.config(
            text="● Agent ready"
        )

        self.send_button.config(
            state="normal"
        )

        self.input_box.focus()


# --------------------------------------------
# Start application
# --------------------------------------------

root = tk.Tk()

app = AgentApp(root)

root.mainloop()