import tkinter as tk
from tkinter import ttk


# Function to handle user input and display responses
def send_message(event=None):
    user_input = entry.get()
    display_text_user(" :You", user_input, "user")

    # Add code to interact with OpenAI here
    # Response = openai.send_message(user_input)
    response = "This is a sample response from the chat bot."
    display_text("Chat Bot: ", response, "bot")
    entry.delete(0, tk.END)


# Function to display messages in the chat box
def display_text(sender, text, tag):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, sender, tag)
    chat_box.insert(tk.END, text + "\n")
    chat_box.config(state=tk.DISABLED)


def display_text_user(sender, text, tag):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, text, tag)
    chat_box.insert(tk.END, sender + "\n")
    chat_box.config(state=tk.DISABLED)

# Create the main Tkinter window
root = tk.Tk()
root.title("Chat Bot")

# Create a card-like frame for the chat box
chat_frame = ttk.Frame(root, padding=10, relief=tk.RAISED, borderwidth=2)
chat_frame.pack(fill=tk.BOTH, expand=True)

# Create a chat box to display messages
chat_box = tk.Text(chat_frame, width=50, height=15, wrap=tk.WORD, state=tk.DISABLED, pady=10, padx=10)
chat_box.pack(fill=tk.BOTH, expand=True,)

# Configure tags for user and bot messages
chat_box.tag_config("user", justify='right')
chat_box.tag_config("bot", justify='left', foreground='green')

# Create a separator to separate the chat box area from the user input area
separator = ttk.Separator(root, orient=tk.HORIZONTAL)
separator.pack(fill=tk.X, padx=10, pady=5)

# Create an entry widget for user input
entry = ttk.Entry(root, width=40)
entry.pack(padx=10, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

# Bind the Enter key press to the send_message function
entry.bind('<Return>', send_message)

# Create a "Send" button with an arrow label
send_button_style = ttk.Style()
send_button_style.configure("Custom.TButton", font=("Helvetica", 14), padding=10)
send_button = ttk.Button(root, text="➡", command=send_message, style="Custom.TButton")
send_button.pack(padx=10, pady=5, side=tk.LEFT)

# Start the Tkinter event loop
root.mainloop()
