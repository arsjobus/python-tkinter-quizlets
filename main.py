import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import random

MAX_QUESTIONS = 20  # Maximum number of questions per quiz

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Quiz")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.questions = []
        self.current_question = 0
        self.score = 0
        self.answered = False

        # Load CSV
        self.load_csv()

        if not self.questions:
            messagebox.showerror("Error", "No questions loaded. Exiting.")
            root.destroy()
            return

        # Shuffle and limit to MAX_QUESTIONS
        random.shuffle(self.questions)
        if len(self.questions) > MAX_QUESTIONS:
            self.questions = self.questions[:MAX_QUESTIONS]

        # Set up answer variable *before* creating RadioButtons
        self.var = tk.StringVar()
        self.var.set("-1")  # Prevents Tkinter from using "None"
        self.var.trace("w", self.check_answer)

        # GUI elements
        self.question_label = tk.Label(
            root, text="", wraplength=700, font=("Arial", 16), justify="center"
        )
        self.question_label.pack(pady=20)

        # Radio buttons
        self.options = []
        for i in range(4):
            rb = tk.Radiobutton(
                root, text="", variable=self.var, value=str(i),
                font=("Arial", 14), wraplength=700, justify="left"
            )
            rb.pack(anchor="w", padx=50, pady=10)
            self.options.append(rb)

        self.feedback_label = tk.Label(
            root, text="", font=("Arial", 14), fg="red", wraplength=700, justify="center"
        )
        self.feedback_label.pack(pady=20)

        self.next_button = tk.Button(root, text="Next", command=self.next_question, font=("Arial", 14))
        self.next_button.pack(pady=20)

        self.show_question()

    def load_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            return

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            # Expect CSV: question, option1, option2, option3, option4, correct_index
            self.questions = [row for row in reader if len(row) == 6]

    def show_question(self):
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            self.question_label.config(text=f"Q{self.current_question + 1}: {q[0]}")

            # Reset selection safely
            self.var.set("-1")
            self.answered = False
            self.feedback_label.config(text="")

            for i in range(4):
                self.options[i].config(text=q[i+1], state="normal")
        else:
            self.show_score()

    def check_answer(self, *args):
        val = self.var.get()

        # Ignore invalid states
        if self.answered or val in ("", None, "None", "-1"):
            return

        selected = int(val)
        q = self.questions[self.current_question]
        correct = int(q[5])

        if selected == correct:
            self.feedback_label.config(text="Correct!", fg="green")
            self.score += 1
        else:
            self.feedback_label.config(
                text=f"Incorrect! Correct answer: {q[correct + 1]}",
                fg="red"
            )

        self.answered = True

        # Disable after answering
        for rb in self.options:
            rb.config(state="disabled")

    def next_question(self):
        self.current_question += 1
        self.show_question()

    def show_score(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        score_label = tk.Label(
            self.root, text=f"Your Score: {self.score}/{len(self.questions)}",
            font=("Arial", 20)
        )
        score_label.pack(pady=100)

        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy, font=("Arial", 16))
        exit_button.pack(pady=50)


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
