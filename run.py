import numpy as np
import PySimpleGUI as sg
import pathlib
import sys

sg.theme('LightGreen6')
SAVE = "save"

choice1, choice2 = sg.Button("A", key="A"), sg.Button("B", key="B")
sort_layout = [
    [sg.Text("Which is better?")],
    [choice1, choice2],
    [sg.Button(SAVE)]
]

def take_input(a, b):
    choice1.update(text=str(a))
    choice2.update(text=str(b))
    input_choice = ""
    while input_choice not in ["A", "B"]:
        event, values = window.read()
        if event == SAVE:
            np.save(input_file.absolute().parent.joinpath(f"saved_{input_file.name}"), sorting_matrix)
        input_choice = event
    return -1 if input_choice == "A" else 1

load_file_layout = [
    [sg.Text('Input', size=(8, 1)), sg.Input(), sg.FileBrowse()],
    [sg.Button("Sort ascending"), sg.Button("Sort descending")]
]
event, load_file_values = sg.Window("Comparatron3000", load_file_layout).read(close=True)
rev = True if event == "Sort ascending" else False
input_file = pathlib.Path(load_file_values[0])

if input_file.suffix == ".save":
    sorting_matrix = np.load(input_file)
elif input_file.suffix == ".txt":
    with open(input_file) as input_fh:
        unsorted_list = input_fh.read().strip().split("\n")
    unsorted_list_len = len(unsorted_list)
    sorting_matrix = np.zeros((unsorted_list_len, unsorted_list_len))
else:
    sg.popup("Invalid file type. File must be a .txt or .save file")
    sys.exit()

window = sg.Window("Comparatron3000", sort_layout, finalize=True)

for row_index, row in enumerate(sorting_matrix):
    for column_index, column in enumerate(sorting_matrix):
        if column_index <= row_index or sorting_matrix[row_index][column_index] != 0:
            continue
        column_value = unsorted_list[column_index]
        row_value = unsorted_list[row_index]
        # comparison_value = input(f"Do you prefer {column_value} or {row_value}?")
        comparison_value = take_input(column_value, row_value)
        sorting_matrix[column_index][row_index] = comparison_value
        sorting_matrix[row_index][column_index] = -1 * comparison_value

sorting_order = sorting_matrix.sum(axis=0)
orderable_unsorted_list = zip(unsorted_list, sorting_order)
sorted_result = sorted(orderable_unsorted_list, key= lambda x: x[1])
if rev:
    sorted_result = sorted_result[::-1]
with open(input_file.absolute().parent.joinpath(f"sorted_{input_file.name}"), "w") as fh:
    fh.write("\n".join([x[0] for x in sorted_result]))