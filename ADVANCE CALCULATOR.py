import ast
import math
import operator
import tkinter as tk
from tkinter import messagebox


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("All-in-One Calculator")
        self.root.geometry("450x650")
        self.root.minsize(350, 500)
        self.root.configure(bg="#1e1e2f")

        self.expression = tk.StringVar()
        self.degrees = True

        self.create_display()
        self.create_buttons()

        self.root.bind("<Return>", lambda event: self.calculate())
        self.root.bind("<Escape>", lambda event: self.clear())
        self.root.bind("<BackSpace>", lambda event: self.backspace())

    def create_display(self):
        title = tk.Label(
            self.root,
            text="ADVANCED CALCULATOR",
            font=("Arial", 16, "bold"),
            bg="#1e1e2f",
            fg="white"
        )
        title.pack(pady=12)

        self.display = tk.Entry(
            self.root,
            textvariable=self.expression,
            font=("Arial", 24),
            justify="right",
            bg="#30304a",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.display.pack(fill="x", padx=12, pady=10, ipady=15)

        self.mode_button = tk.Button(
            self.root,
            text="Angle Mode: DEG",
            command=self.toggle_mode,
            bg="#505078",
            fg="white",
            relief="flat"
        )
        self.mode_button.pack(fill="x", padx=12, pady=4)

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#1e1e2f")
        button_frame.pack(fill="both", expand=True, padx=8, pady=8)

        buttons = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "⌫"],
            ["1", "2", "3", "-", "("],
            ["0", ".", "=", "+", ")"],
            ["sin", "cos", "tan", "sqrt", "π"],
            ["log", "ln", "x²", "^", "√"],
            ["abs", "!", "pi", "e", "%"],
            ["asin", "acos", "atan", "floor", "ceil"],
            ["MS", "MR", "MC", "Ans", "±"],
        ]

        self.last_answer = 0
        self.memory = 0

        for r, row in enumerate(buttons):
            button_frame.rowconfigure(r, weight=1)

            for c, label in enumerate(row):
                button_frame.columnconfigure(c, weight=1)

                if label == "=":
                    color = "#27ae60"
                elif label in ("C", "⌫", "MC"):
                    color = "#c0392b"
                elif label in ("+", "-", "*", "/", "^", "%"):
                    color = "#46506a"
                elif label in (
                    "sin", "cos", "tan", "sqrt", "√",
                    "log", "ln", "x²", "abs", "!",
                    "asin", "acos", "atan", "floor", "ceil"
                ):
                    color = "#514b80"
                else:
                    color = "#34344f"

                button = tk.Button(
                    button_frame,
                    text=label,
                    font=("Arial", 11, "bold"),
                    bg=color,
                    fg="white",
                    activebackground="#6c63a8",
                    activeforeground="white",
                    relief="flat",
                    command=lambda x=label: self.on_click(x)
                )
                button.grid(
                    row=r, column=c,
                    sticky="nsew", padx=3, pady=3
                )

    def toggle_mode(self):
        self.degrees = not self.degrees
        mode = "DEG" if self.degrees else "RAD"
        self.mode_button.config(text=f"Angle Mode: {mode}")

    def clear(self):
        self.expression.set("")

    def backspace(self):
        self.expression.set(self.expression.get()[:-1])

    def on_click(self, value):
        current = self.expression.get()

        if value == "C":
            self.clear()
        elif value == "⌫":
            self.backspace()
        elif value == "=":
            self.calculate()
        elif value == "±":
            if current:
                self.expression.set(f"-({current})")
        elif value == "MS":
            self.memory = self.last_answer
        elif value == "MR":
            self.expression.set(current + str(self.memory))
        elif value == "MC":
            self.memory = 0
        elif value == "Ans":
            self.expression.set(current + str(self.last_answer))
        elif value in ("sin", "cos", "tan", "sqrt", "√",
                       "log", "ln", "abs", "asin", "acos",
                       "atan", "floor", "ceil"):
            function = "sqrt" if value == "√" else value
            self.expression.set(current + function + "(")
        elif value == "x²":
            self.expression.set(f"({current})**2")
        elif value == "!":
            self.expression.set(current + "!")
        elif value == "π":
            self.expression.set(current + "pi")
        else:
            self.expression.set(current + value)

    def safe_evaluate(self, expression):
        expression = expression.replace("^", "**")

        constants = {"pi": math.pi, "e": math.e}

        def trig_sin(x):
            return math.sin(math.radians(x) if self.degrees else x)

        def trig_cos(x):
            return math.cos(math.radians(x) if self.degrees else x)

        def trig_tan(x):
            angle = math.radians(x) if self.degrees else x
            if abs(math.cos(angle)) < 1e-12:
                raise ValueError("Tangent is undefined at this angle")
            return math.tan(angle)

        def inverse(function, x):
            result = function(x)
            return math.degrees(result) if self.degrees else result

        functions = {
            "sin": trig_sin,
            "cos": trig_cos,
            "tan": trig_tan,
            "asin": lambda x: inverse(math.asin, x),
            "acos": lambda x: inverse(math.acos, x),
            "atan": lambda x: inverse(math.atan, x),
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "abs": abs,
            "floor": math.floor,
            "ceil": math.ceil,
            "factorial": math.factorial,
        }

        binary = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
        }

        unary = {
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }

        def factorial(x):
            if not isinstance(x, (int, float)):
                raise ValueError("Invalid factorial")
            if not math.isfinite(x) or x < 0 or x != int(x):
                raise ValueError("Factorial needs a non-negative integer")
            if x > 170:
                raise ValueError("Number is too large")
            return math.factorial(int(x))

        functions["factorial"] = factorial

        def evaluate(node):
            if isinstance(node, ast.Expression):
                result = evaluate(node.body)

            elif isinstance(node, ast.Constant):
                if isinstance(node.value, bool) or not isinstance(
                    node.value, (int, float)
                ):
                    raise ValueError("Only numbers are allowed")
                result = node.value

            elif isinstance(node, ast.Name):
                if node.id not in constants:
                    raise ValueError("Unknown constant")
                result = constants[node.id]

            elif isinstance(node, ast.BinOp):
                op_type = type(node.op)
                if op_type not in binary:
                    raise ValueError("Unsupported operator")

                left = evaluate(node.left)
                right = evaluate(node.right)

                if op_type is ast.Pow and abs(right) > 1000:
                    raise ValueError("Exponent is too large")

                result = binary[op_type](left, right)

            elif isinstance(node, ast.UnaryOp):
                op_type = type(node.op)
                if op_type not in unary:
                    raise ValueError("Unsupported operator")
                result = unary[op_type](evaluate(node.operand))

            elif isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name):
                    raise ValueError("Invalid function")

                name = node.func.id
                if name not in functions or node.keywords:
                    raise ValueError("Unsupported function")

                args = [evaluate(arg) for arg in node.args]
                result = functions[name](*args)

            else:
                raise ValueError("Invalid expression")

            if isinstance(result, float):
                if not math.isfinite(result):
                    raise ValueError("Result is not finite")
                if abs(result) > 1e100:
                    raise ValueError("Result is too large")

            return result

        tree = ast.parse(expression, mode="eval")
        return evaluate(tree)

    def calculate(self):
        expression = self.expression.get().strip()
        if not expression:
            return

        # Convert postfix factorial: 5! -> factorial(5)
        expression = expression.replace("π", "pi")
        expression = expression.replace("×", "*").replace("÷", "/")

        import re
        expression = re.sub(
            r"(\b(?:\d+(?:\.\d+)?|pi|e|\([^()]*\)))!",
            r"factorial(\1)",
            expression
        )

        try:
            result = self.safe_evaluate(expression)

            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 12)

            self.last_answer = result
            self.expression.set(str(result))

        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Cannot divide by zero.")
        except (ValueError, TypeError, OverflowError) as error:
            messagebox.showerror("Calculation Error", str(error))
        except SyntaxError:
            messagebox.showerror(
                "Syntax Error", "Please enter a valid expression."
            )
        except Exception:
            messagebox.showerror(
                "Error", "Unable to calculate this expression."
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()