import PySimpleGUI as sg

num_buttons = 2
layout = [[sg.Text('Your typed chars appear here:'), sg.Text('', key='_OUTPUT_')],
            [sg.Input(do_not_clear=True, key='_IN_')],
            *[[sg.Button('Button'),] for i in range(num_buttons)],
            [sg.Button('Add Rows'), sg.Button('Delete Rows' ), sg.Button('Exit')]]

location = (600,600)
window = sg.Window('Window Title', location=location).Layout(layout)


num_buttons = 2
while True:             # Event Loop
    event, values = window.Read()
    print(event, values)
    if event is None or event == 'Exit':
        break
    if event == 'Add Rows' or event == 'Delete Rows':
        num_buttons +=  -2 if event == 'Delete Rows' else 2

        layout = [[sg.Text('Your typed chars appear here:'), sg.Text('', key='_OUTPUT_')],
                    [sg.Input(do_not_clear=True, key='_IN_')],
                    *[[sg.Button('Button'),] for i in range(num_buttons)],
                  [sg.Button('Add Rows'), sg.Button('Delete Rows'), sg.Button('Exit')]]
        window1 = sg.Window('Window Title', location=location).Layout(layout)
        window.Close()
        window = window1

window.Close()