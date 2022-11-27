import os
import PySimpleGUI as psg

BPAD_TOP = ((20, 20), (20, 10))
BPAD_LEFT = ((20, 10), (0, 10))
curr_dir = os.getcwd()


def create_task_page():
    block_1 = [[psg.Text('Task Detail', font='Any 20', justification='center')],
               [psg.Text("", font='Any 10', key='Task_No')],
               [psg.Text("", font='Any 10', key='SS_Name')],
               [psg.Text("", font='Any 10', key='SS_Add')],
               [psg.Text("", font='Any 10', key='ES_Name')],
               [psg.Text("", font='Any 10', key='ES_Add')],
               [psg.Text("", font='Any 10', key='BT')],
               [psg.Text("", font='Any 10', key='DT')],
               [psg.Multiline("", font='Any 10', key='OP', size=(50, 150))]]

    block_2 = [[psg.Text('Interactive Map', font='Any 20', justification='center')],
               [psg.Image(filename="", size=(400, 300), key='Image')]]

    layout_full = [[psg.Column(block_1, size=(450, 550), pad=BPAD_TOP),
                   psg.Frame("Interactive Map", layout=block_2, size=(450, 550), pad=BPAD_TOP)],
                   [psg.Button('End Task', pad=(450, 0))]]

    return psg.Window('Start Task Page', layout_full, size=(1000, 700), resizable=True, finalize=True, )


def update_window(window, task_no, task):
    window['Task_No'].update('Task No: {:}'.format(task_no))
    window['SS_Name'].update('Start Station Name: {:}'.format(task.start_name))
    window['SS_Add'].update('Start Station Address: {:}'.format(task.start_address))
    window['ES_Name'].update('End Station Name: {:}'.format(task.end_name))
    window['ES_Add'].update('End Station Address: {:}'.format(task.end_address))
    window['BT'].update('Bikes to be transported: {:}'.format(task.bikes_required))
    window['DT'].update('Total Distance to travel: {:}'.format(task.travel_distance))
    window['OP'].update('Optimal Path: {:}'.format(task.optimal_path))

    return window


def add_map_image(window):
    filename = curr_dir + '/maps/map.png'
    window['Image'].update(filename=filename)
    window.refresh()
    return window
