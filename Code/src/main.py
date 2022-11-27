import PySimpleGUI as sg
from gui.login_page import Login
from dashboard import Dashboard
from reports.reports import Reports
from databases.stations.database_creation import get_collection
from databases.stations.emulate_real_world import start_background_process


sg.theme('TealMono')
data = get_collection()
start_background_process(data)


class Start_Divvy:
    def __int__(self):
        self.sign_in_result = None
        self.login = Login()

    def start_page(self):
        self.sign_in_result = False
        layout = [[sg.Text('Welcome to My Divvy Van Assistant Software', font=100, justification="c")],
                  [sg.Button('Sign In'), sg.Button('Sign Up'), sg.Button('Reports')],
                  [sg.Button('About Us'), sg.Button('Help'), sg.Button('Contact Us'), sg.Button('Exit')]]

        return sg.Window('My Divvy Van Assistant', layout, margins=(250, 250), finalize=True)

    def about_us(self):
        layout = [[sg.Text('About Us', font=500, justification="c")],
                  [sg.Text('Divvy Van Assistant is a GUI application for Divvy Van drivers which aims to help\
                  \nthem to transport divvy bikes and scooters from one station to another while ensuring optimal\
                  \ntravel routes. The main idea is to build a system that will keep track of all the divvy stations\
                  \nand the bikes available at each station. Our goal is to increase the efficiency of the entire system\
                  \nwithout affecting the day to day activities in and around the city.', font=300)],
                  [sg.Button('Back')]]

        return sg.Window('Sign In page', layout, margins=(50, 50), finalize=True)

    def contact_us(self):
        layout = [[sg.Text('Contact Us:', font=500)],
                  [sg.Text('Email : abc@divvy.com', font=400)],
                  [sg.Text('Phone : +1 123-456-8900', font=400)],
                  [sg.Text('Address : UIC, Chicago ,IL 60607.', font=400)],
                  [sg.Button('Back')]]
        return sg.Window('Sign Up Page', layout, margins=(100, 80), finalize=True)

    def help_section(self):
        layout = [[sg.Text('Help Section and FAQs:\n', font=200)],
                  [sg.Text('For New Users:', font=100)],
                  [sg.Text('1) Can I create a new user ID?', font=50)],
                  [sg.Text('~ No. The corporate will create one for you.', font=50)],
                  [sg.Text('2) How long will it take to activate my ID?', font=50)],
                  [sg.Text('~ It will be instantly activated once the corporate approves it.', font=50)],
                  [sg.Text('3) Who do I contact in case I have trouble logging in?', font=50)],
                  [sg.Text('~ Please contact the Admin.\n', font=50)],
                  [sg.Text('', font=50)],
                  [sg.Text('For Returning Users:', font=100)],
                  [sg.Text('1) Can I change my password?', font=50)],
                  [sg.Text('~ Yes. Please contact the admin.', font=50)],
                  [sg.Text('2) What is the pasword when logging in for the first time?', font=50)],
                  [sg.Text('~ Corporate will give you the credentials once account is created.', font=50)],
                  [sg.Text('3) Can I reset the Application?', font=50)],
                  [sg.Text('~ Yes. Please reboot and it will be reset.\n', font=50)],
                  [sg.Button('Back')]]
        return sg.Window('Help and FAQ page', layout, margins=(20, 20), finalize=True)

    def run(self):
        window1, window2 = self.start_page(), None

        while True:
            window, event, values = sg.read_all_windows()
            if event in (sg.WIN_CLOSED, 'Exit'):
                self.sign_in_result = False
                break

            if window == window1:
                if event == 'About Us':
                    window1.hide()
                    window2 = self.about_us()

                if event == 'Contact Us':
                    window1.hide()
                    window2 = self.contact_us()

                if event == 'Help':
                    window1.hide()
                    window2 = self.help_section()

                if event == 'Sign In':
                    self.sign_in_result, self.user_name = self.sign_in()
                    if self.sign_in_result:
                        break
                    continue

                if event == 'Sign Up':
                    result = self.sign_up()
                    if result:
                        self.sign_in_result, self.user_name = self.sign_in()
                        if self.sign_in_result:
                            break
                    continue

                if event == 'Reports':
                    window2 = self.reports()
                    continue

            if window == window2:
                if event == 'Back':
                    window2.hide()
                    window1.un_hide()

        if self.sign_in_result:
            dashboard = Dashboard(user=self.user_name, table=data)
            dashboard.run()

    def sign_in(self):
        login = Login()
        result = login.sign_in()
        return result

    def sign_up(self):
        login = Login()
        result = login.create_account()
        return result

    def reports(self):
        sg.popup("Login with Admin Credentials")
        login = Login()
        result, username = login.sign_in(admin=True)
        if result:
            start_report = Reports()
            start_report.start_page()
        return


if __name__ == "__main__":
    start_divvy = Start_Divvy()
    start_divvy.run()
