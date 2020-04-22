import pathlib

import PySimpleGUI as sg

sg.theme('DarkAmber')

def input_comparator(a, b):
    input_choice = ""
    choice1.update(text=str(a))
    choice2.update(text=str(b))
    while input_choice not in ["A", "B"]:
        event, values = window.read()
        input_choice = event
    return 1 if input_choice == "A" else -1

# unsorted_list = ["1", "4", "2", "8", "7"]

def merge_sort(l):
    if len(l) == 1:
        return l
    midpoint = len(l) // 2
    new_l = []
    l1 = merge_sort(l[:midpoint])
    l2 = merge_sort(l[midpoint:])
    while l1 and l2:
        comp_result = input_comparator(l1[0], l2[0])
        if comp_result < 1:
            new_l.append(l1[0])
            l1 = l1[1:]
        else:
            new_l.append(l2[0])
            l2 = l2[1:]

    new_l.extend(l1)
    new_l.extend(l2)
    return new_l

def check_sorting(sorted_list):
    for index, elem in enumerate(sorted_list[:-1]):
        comp_result = input_comparator(elem, sorted_list[index+1])
        if comp_result > 0:
            return 1
    return 0


load_file_layout = [
    [sg.Text('Input', size=(8, 1)), sg.Input(), sg.FileBrowse()],
    [sg.Button("Sort ascending"), sg.Button("Sort descending")]
]
event, load_file_values = sg.Window("Forbes' Comparator", load_file_layout).read(close=True)
input_file = pathlib.Path(load_file_values[0])

with open(input_file) as input_fh:
    unsorted_list = input_fh.read().strip().split("\n")

choice1, choice2 = sg.Button("A", key="A"), sg.Button("B", key="B")
sort_layout = [
    [sg.Text("Which do you prefer?")],
    [choice1, choice2]
]
window = sg.Window("Forbes' Comparator", sort_layout, finalize=True)

sorted_list = merge_sort(unsorted_list)
check_result = check_sorting(sorted_list)
if check_result != 0:
    sg.popup("Forbes' Comparator", "Could not determine a ranking as your rankings were not consistent")
else:
    if event == "Sort descending":
        sorted_list = sorted_list[::-1]

    with open(input_file.absolute().parent.joinpath(f"sorted_{input_file.name}"), "w") as output_fh:
        output_fh.write("\n".join(sorted_list))