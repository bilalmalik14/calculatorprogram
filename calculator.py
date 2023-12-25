import tkinter as tk
import math

CALCULATORCOLOR = "#F5F5F5"
LABELCOLOR = "#25265E"
SMALLFONT = ("Arial", 16)
LARGEFONT = ("Arial", 40, "bold")
BUTTONCOLOR = "#FFFFFF"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")
        
        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()
        self.button_frame = self.create_buttons_frame()
        
        self.total_label, self.current_label = self.create_display_labels()

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_root_button()
        self.create_inverse_button()
        self.bind_keys()
        self.create_backspace_function()
        
    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=CALCULATORCOLOR, 
                               fg=LABELCOLOR, padx=24, font=SMALLFONT)    
        total_label.pack(expand=True, fill="both")
        
        current_label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=CALCULATORCOLOR, 
                                 fg=LABELCOLOR, padx=24, font=LARGEFONT)    
        current_label.pack(expand=True, fill="both")

        return total_label, current_label
        
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=CALCULATORCOLOR)
        frame.pack(expand=True, fill="both")
        return frame
    
    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()
                
    def create_digit_buttons(self):
        self.digits = {
            7: (1, 0), 8: (1, 1), 9: (1, 2),
            4: (2, 0), 5: (2, 1), 6: (2, 2),
            1: (3, 0), 2: (3, 1), 3: (3, 2),
            0: (4, 1), '.': (4, 2)  
        }
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.button_frame, text=str(digit), 
                                bg=BUTTONCOLOR, fg=LABELCOLOR, 
                                font=('Arial', 16, 'bold'), 
                                bd=0, highlightthickness=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()
        
                
    def create_operator_buttons(self):
        self.operations = ["/", "*", "-", "+"]  # Use standard symbols for operations
        symbols = ["\u00F7", "\u00D7", "-", "+"]  # Display symbols
        for i, symbol in enumerate(symbols):
            button = tk.Button(self.button_frame, text=symbol, 
                            bg="#FAF9F6", fg=LABELCOLOR, 
                            font=('Arial', 20, 'bold'), 
                            bd=0, highlightthickness=0, command=lambda x=self.operations[i]: self.append_operator(x))
            button.grid(row=i, column=3, sticky=tk.NSEW)

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()
        
    # Adjust your create_buttons_frame method to have equal weight for all rows and columns
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")

        # Configure the grid with equal weight
        for x in range(5):  # 5 rows
            frame.grid_rowconfigure(x, weight=1)
        for y in range(4):  # 4 columns to match the number of operator buttons
            frame.grid_columnconfigure(y, weight=1)

        return frame

    def create_clear_button(self):
        button = tk.Button(self.button_frame, text="C", 
                           bg="#FAF9F6", fg=LABELCOLOR, 
                           font=('Arial', 20, 'bold'), 
                           bd=0, highlightthickness=0, 
                           command=self.clear)
        button.grid(row=4, column=0, columnspan=1, sticky=tk.NSEW)
        
    def create_square_button(self):
        button = tk.Button(self.button_frame, text="x\u00B2", 
                           bg="#FAF9F6", fg=LABELCOLOR, 
                           font=('Arial', 20, 'bold'), 
                           bd=0, highlightthickness=0, 
                           command=self.square)
        button.grid(row=0, column=2, columnspan=1, sticky=tk.NSEW)
        
    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()
    def create_root_button(self):
        button = tk.Button(self.button_frame, text="\u221A",  
                           bg="#FAF9F6", fg=LABELCOLOR, 
                           font=('Arial', 20, 'bold'), 
                           bd=0, highlightthickness=0, 
                           command=self.root)
        button.grid(row=0, column=1, columnspan=1, sticky=tk.NSEW)
        
    def root(self):
        try:
            # Calculate the square root of the current expression
            self.current_expression = str(math.sqrt(float(self.current_expression)))
        except Exception as e:
            # Handle any errors (like taking the square root of a negative number)
            self.current_expression = "Error"
        finally:
            # Update the display
            self.update_label()
        
    def create_inverse_button(self):
        button = tk.Button(self.button_frame, text="1/x", 
                           bg="#FAF9F6", fg=LABELCOLOR, 
                           font=('Arial', 20, 'bold'), 
                           bd=0, highlightthickness=0, 
                           command=self.reciprocal)
        button.grid(row=0, column=0, columnspan=1, sticky=tk.NSEW)
        
    def reciprocal(self):
        try:
            # Calculate the reciprocal of the current expression
            self.current_expression = str(1 / float(self.current_expression))
        except ZeroDivisionError:
            # Handle division by zero
            self.current_expression = "Error"
        except Exception as e:
            # Handle any other errors
            self.current_expression = "Error"
        finally:
            # Update the display
            self.update_label()
            
            
    def evaluate(self):
        try:
            # Evaluate the expression and update the display
            self.total_expression += self.current_expression
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            # Handle any errors e.g., division by zero, syntax error
            self.current_expression = "Error"
        finally:
            self.update_label()
            self.update_total_label()

    def create_equals_button(self):
        button = tk.Button(self.button_frame, text="=", 
                           bg="#89CFF0", fg=LABELCOLOR, 
                           font=('Arial', 20, 'bold'), 
                           bd=0, highlightthickness=0, 
                           command=self.evaluate)
        button.grid(row=4, column=3, columnspan=1, sticky=tk.NSEW)
        
    def update_total_label(self):
        self.total_label.config(text=self.total_expression)
        
    def update_label(self):
        self.current_label.config(text=self.current_expression[:11])
    
    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
            
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))
            
    def create_backspace_function(self):
        self.window.bind("<BackSpace>", self.handle_backspace)

    def handle_backspace(self, event):
        # Remove the last character from the current expression
        self.current_expression = self.current_expression[:-1]
        self.update_label()
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()
