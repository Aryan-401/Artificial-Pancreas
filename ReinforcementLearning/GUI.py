import tkinter
import customtkinter

# System Settings
customtkinter.set_appearance_mode('light')
customtkinter.set_default_color_theme('blue')

## App frame
app = customtkinter.CTk()
app.geometry('1000x600')
app.title('Bergman Minimal Model based Reinforcement Learning')
app.resizable(False, False)


## Functions
def choose_model(model_name):
    if model_name in ["Previous Paper", "LSTM wo BN", "LSTM w BN"]:
        return model_name
    else:
        raise ValueError('Invalid model name')


def is_numeric(text):
    """Checks if the input text is a valid number (integer or float)."""
    try:
        float(text)
        return True
    except ValueError:
        return False

heading = customtkinter.CTkLabel(app, text='BMM based RL Model Inference', font=('Sans Serif', 20))
heading.pack(padx=10, pady=10)

model_choose_list = customtkinter.CTkOptionMenu(app, values=["Previous Paper", "LSTM wo BN", "LSTM w BN"],
                                                command=choose_model)
model_choose_list.pack(padx=10, pady=10)

grid_frame = customtkinter.CTkFrame(master=app, width=400, height=500)
grid_frame.pack(padx=20, side='left', pady=20)
grid_frame.grid_propagate(False)
grid_frame.pack_propagate(False)

graph_frame = customtkinter.CTkFrame(master=app, width=600, height=500)
graph_frame.pack(side='right', pady=20, padx=20)
graph_frame.grid_propagate(False)

# Add image to graph frame
image = tkinter.PhotoImage("Graph", file="graph.png")
image_label = customtkinter.CTkLabel(master=graph_frame, image=image)
image_label.pack()

# Create a grid of 10 inputs in a 5 rows 2 col list
for i in range(5):
    for j in range(2):
        # Check for numeric input before adding entry
        def validate(text):
            if not is_numeric(text):
                return False
            return True


        vcmd = app.register(validate)  # Register validation function
        entry = (customtkinter.CTkEntry(
            master=grid_frame,
            placeholder_text="0",
            validate="key",
            validatecommand=(vcmd, '%P')  # Pass the text to the validation function
        ))
        entry.grid(row=i, column=j, padx=30, pady=10)

def submit_data():
    data = []
    for i in range(5):
        for j in range(2):
            entry_widget = grid_frame.grid_slaves(row=i, column=j)[0]
            data.append(float(entry_widget.get()))


    params = {}
    for i in range(3):
        for j in range(0, 10, 2):
            entry_widget = parameters.grid_slaves(row=i, column=j + 1)[0]
            try:
                params[parameters.grid_slaves(row=i, column=j)[0].cget('text')] = float(entry_widget.get())
            except ValueError:
                pass

    all_data = {
      "grid_data": data,
      "parameters": params
    }

    # TODO: connect backend
    return all_data


button_submit = customtkinter.CTkButton(master=grid_frame, text='Submit', command=submit_data)
button_submit.pack(side='bottom', pady=5)
parameters = customtkinter.CTkFrame(master=grid_frame, width=350, height=150)
parameters.pack(pady=5, side='bottom')
parameters.grid_propagate(False)

all_cons = ['I', 'X', 'G', 'p1', 'p2', 'p3', 'τ', 'n', 'Gb', 'u', 'Ag', 'tI', 'tG', 'Vg', ' ']
pre_val = ['0.054', '0.0067', '120.0', '0.0337', '0.0209', '7.5e-06', '0.083333', '0.214', '144.0', '0.054', '0.8', '33.0', '24.0', '13.79', " "]
for i in range(3):
    for j in range(0, 10, 2):
        sym = all_cons[i * 5 + j // 2]
        te = pre_val[i * 5 + j // 2]
        if sym == ' ':
            disabled = 'disabled'
        else:
            disabled = 'normal'


        def validate(text):
            if not is_numeric(text):
                return False
            return True


        vcmd = app.register(validate)
        label = customtkinter.CTkLabel(master=parameters, text=sym, width=5).grid(row=i, column=j, padx=5, pady=10)
        entry = customtkinter.CTkEntry(master=parameters, width=30, state=disabled, validate="key",
                                       validatecommand=(vcmd, '%P'), placeholder_text=te).grid(row=i, column=j + 1, padx=9, pady=10)
parameters.pack_propagate(False)

app.mainloop()
