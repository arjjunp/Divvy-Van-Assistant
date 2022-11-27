import PySimpleGUI as psg
from ranking.transportation.create_operation import Operations
from reports.reports import Reports
from gui.start_task_page import create_task_page, update_window, add_map_image
from databases.stations.update_stations import update_data_completion
from maps.develop_map import create_thread, stop_thread, create_request
from maps.generate_pic import click


BORDER_COLOR = '#C7D5E0'
DARK_HEADER_COLOR = '#1B2838'
BPAD_TOP = ((20, 20), (20, 10))
BPAD_LEFT = ((20, 10), (0, 10))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((10, 20), (10, 20))


class Dashboard:
    def __init__(self, user, table):
        self.radius_sel = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        self.tasks_sel = []
        self.user = user
        self.table = table
        self.l = Reports()

    def create_user_page(self):
        block_1 = [[psg.Text('Divvy Van Assistant', size=(50, 1), justification='center', pad=BPAD_TOP, font='Any 20')]]

        block_2 = [[psg.Text('Select Radius Here', font='Any 20')],
                   [psg.Combo(self.radius_sel, key='radius', size=(50, 150))],
                   [psg.Button('Set Radius')]]

        block_3 = [[psg.Text('Select Task Here', font='Any 20', justification='center')],
                   [psg.Listbox(self.tasks_sel, key='tasks_sel', size=(50, 10))],
                   [psg.Button('Set Task')]]

        block_4 = [[psg.Text('Task Detail', font='Any 20', justification='center')],
                   [psg.Text("", font='Any 10', key='Task_No')],
                   [psg.Text("", font='Any 10', key='SS_Name')],
                   [psg.Text("", font='Any 10', key='SS_Add')],
                   [psg.Text("", font='Any 10', key='ES_Name')],
                   [psg.Text("", font='Any 10', key='ES_Add')],
                   [psg.Text("", font='Any 10', key='BT')],
                   [psg.Text("", font='Any 10', key='DT')],
                   [psg.Multiline("", font='Any 10', key='OP', size=(50, 170))]]

        layout = [
                [psg.Column(block_1, size=(920, 90), pad=BPAD_TOP)],
                [psg.Column([[psg.Column(block_2, size=(450, 150), pad=BPAD_LEFT_INSIDE)],
                            [psg.Column(block_3, size=(450, 270), pad=BPAD_LEFT_INSIDE)]], pad=BPAD_LEFT, background_color='#00316E'),
                 psg.Column(block_4, size=(450, 390), pad=BPAD_RIGHT)],
                [psg.Button('Start Task', pad=(250, 0)), psg.Button('Exit and Log Out')]]

        return psg.Window('User Page', layout, size=(1000, 700), resizable=True, finalize=True)

    def update_window(self, window, task_no, task):
        window['Task_No'].update('Task No: {:}'.format(task_no))
        window['SS_Name'].update('Start Station Name: {:}'.format(task.start_name))
        window['SS_Add'].update('Start Station Address: {:}'.format(task.start_address))
        window['ES_Name'].update('End Station Name: {:}'.format(task.end_name))
        window['ES_Add'].update('End Station Address: {:}'.format(task.end_address))
        window['BT'].update('Bikes to be transported: {:}'.format(task.bikes_required))
        window['DT'].update('Total Distance to travel: {:}'.format(task.travel_distance))
        window['OP'].update('Optimal Path: {:}'.format(task.optimal_path))

        return window

    def run(self):
        dashboard_win = self.create_user_page()
        start_task_win = None
        global tasks_generated, rad, selected_task_no, selected_task

        while True:
            window, event, values = psg.read_all_windows()

            if event in (psg.WIN_CLOSED, 'Exit and Log Out'):
                break

            if window == dashboard_win:
                if event == 'Set Radius':
                    rad = values['radius']
                    log_count = 2

                    operations_obj = Operations(radius=rad, logins=log_count)
                    tasks_generated = operations_obj.run()

                    tasks_list = ['Task: ' + str(i+1) for i in range(0, len(tasks_generated))]
                    window['tasks_sel'].update(values=tasks_list)

                if event == 'Set Task':
                    selected_task_no = int(values['tasks_sel'][0].split()[1])
                    selected_task = tasks_generated[selected_task_no-1]
                    window = self.update_window(window, selected_task_no, selected_task)

                if event == 'Start Task':
                    dashboard_win.close()
                    start_task_win = create_task_page()
                    start_task_win = update_window(start_task_win, selected_task_no, selected_task)
                    create_request(selected_task)
                    create_thread()
                    click()
                    start_task_win = add_map_image(start_task_win)

            if window == start_task_win:
                if event == 'End Task':
                    self.l._update_aggregate(self.user, selected_task_no, selected_task)
                    self.l._dailylog(self.user, selected_task_no, selected_task)
                    update_data_completion(self.table, selected_task)
                    start_task_win.close()

                    # STOP THREAD SOMEHOW
                    dashboard_win = self.create_user_page()
