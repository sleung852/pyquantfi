import sys
import PySimpleGUI as sg

from blackscholes import EuropeanOptionPricer
from impliedvol import ImpliedVolatilityEstimator
from asianoptionpricer import GeometricAsianOptionPricer, ArithmeticAsianOptionPricer
from basketoptionpricer import ArithmeticBasketOptionBasketPricer, GeometricBasketOptionPricer
from binominaltree import BinominalTree

sg.theme('Light Green 5')

OPTIONS_CHOICE = ['European', 'American', 'Geometric Asian', 'Arithmetic Asian', 'Geometric Basket', 'Arithmetic Basket']

methodology = {
    'European' : ['Black Scholes', 'Binominal Tree'],
    'American' : ['Binominal Tree'],
    'Geometric Asian' : ['Closed Form', 'Monte Carlo'],
    'Arithmetic Asian' : ['Monte Carlo', 'Monte Carlo with Control Variate'],
    'Geometric Basket' : ['Closed Form', 'Monte Carlo'],
    'Arithmetic Basket' : ['Monte Carlo', 'Monte Carlo with Control Variate'],
}

input_values_dict = {
            'European Black Scholes': ['S', 'K', 'T', 'sigma', 'r', 'q'],
            'European Binominal Tree': ['S', 'K', 'T', 'sigma', 'r', 'n'],
            'Geometric Asian Closed Form': ['S', 'K', 'T', 'sigma', 'r', 'n'],
            'Geometric Asian Monte Carlo': ['S', 'K', 'T', 'sigma', 'r', 'n', 'm'],
            'Arithmetic Asian Monte Carlo': ['S', 'K', 'T', 'sigma', 'r', 'n', 'm'],
            'Arithmetic Asian Monte Carlo with Control Variate': ['S', 'K', 'T', 'sigma', 'r', 'n', 'm'],
            'Geometric Basket Closed Form': ['S1', 'S2', 'K', 'T', 'sigma1', 'sigma2', 'r', 'rho'],
            'Geometric Basket Monte Carlo': ['S1', 'S2', 'K', 'T', 'sigma1', 'sigma2', 'r', 'rho', 'm'],
            'Arithmetic Basket Monte Carlo': ['S1', 'S2', 'K', 'T', 'sigma1', 'sigma2', 'r', 'rho', 'n', 'm'],
            'Arithmetic Basket Monte Carlo with Control Variate': ['S1', 'S2', 'K', 'T', 'sigma1', 'sigma2', 'r', 'rho', 'n', 'm'],
            'American Binominal Tree': ['S', 'K', 'T', 'sigma', 'r', 'n'],
        }

UNIQUE_INPUT_VALUES = ['S', 'S1', 'S2', 'K', 'T', 'sigma', 'sigma1', 'sigma2', 'r', 'rho', 'q' , 'n', 'm']

default1 = OPTIONS_CHOICE[0]
option_choice = methodology[default1]
default2 = option_choice[0]

option_layout = [
    [sg.Text('Step 1: Select an Option Type', background_color='darkseagreen')],
    [sg.Text('Option Type:', background_color='darkseagreen'), sg.Drop(values=OPTIONS_CHOICE, default_value = default1, auto_size_text=True, enable_events=True, key='-option_type-')],
    [sg.Text('Step 2: Select a Methodology', background_color='darkseagreen')],
    [sg.Text('Methodology:', background_color='darkseagreen'), sg.Drop(values=option_choice, default_value = default2, auto_size_text=True, enable_events=True, key='-option_method-')],
    [sg.Text('Step 3: Call or Put?', background_color='darkseagreen')],
    [sg.Text('Option Kind:', background_color='darkseagreen'), sg.Drop(values=['Call', 'Put'], default_value = 'Call', auto_size_text=True, enable_events=True, key='-option_kind-')]
    ]

# for input_value in UNIQUE_INPUT_VALUES:
#     if input_value in input_values_dict['European Black Scholes']: # default
#         option_layout.append([sg.Text(f'{input_value}:', background_color='darkseagreen', visible=True, key=f'-{input_value}_label-'), sg.Input(key=f'-{input_value}-', visible=True)])
#     else:
#         option_layout.append([sg.Text(f'{input_value}:', background_color='darkseagreen', visible=False, key=f'-{input_value}_label-'), sg.Input(key=f'-{input_value}-', visible=False)])

iv_layout = [[sg.Text('This is inside tab 5')],
            [sg.Input(key='-in4-')]]

layout = [[sg.TabGroup([[sg.Tab('Option Value', option_layout, background_color='darkseagreen', key='-mykey-'),
                        sg.Tab('Implied Volatility', iv_layout)]], key='-group1-', tab_location='top', selected_title_color='purple')],
        [sg.Button('Next', enable_events=True, key='-next-'), sg.Button('Exit', enable_events=True, key='-exit-')]
        ]

window = sg.Window('Option Calculator', layout,
                default_element_size=(12, 1))

def menu_window():
    option_layout = [
        [sg.Text('Step 1: Select an Option Type', background_color='darkseagreen')],
        [sg.Text('Option Type:', background_color='darkseagreen'), sg.Drop(values=OPTIONS_CHOICE, default_value = default1, auto_size_text=True, enable_events=True, key='-option_type-')],
        [sg.Text('Step 2: Select a Methodology', background_color='darkseagreen')],
        [sg.Text('Methodology:', background_color='darkseagreen'), sg.Drop(values=option_choice, default_value = default2, auto_size_text=True, enable_events=True, key='-option_method-')],
        [sg.Text('Step 3: Call or Put?', background_color='darkseagreen')],
        [sg.Text('Option Kind:', background_color='darkseagreen'), sg.Drop(values=['Call', 'Put'], default_value = 'Call', auto_size_text=True, enable_events=True, key='-option_kind-')]
        ]

    # for input_value in UNIQUE_INPUT_VALUES:
    #     if input_value in input_values_dict['European Black Scholes']: # default
    #         option_layout.append([sg.Text(f'{input_value}:', background_color='darkseagreen', visible=True, key=f'-{input_value}_label-'), sg.Input(key=f'-{input_value}-', visible=True)])
    #     else:
    #         option_layout.append([sg.Text(f'{input_value}:', background_color='darkseagreen', visible=False, key=f'-{input_value}_label-'), sg.Input(key=f'-{input_value}-', visible=False)])

    iv_layout = [[sg.Text('This is inside tab 5')],
                [sg.Input(key='-in4-')]]

    layout = [[sg.TabGroup([[sg.Tab('Option Value', option_layout, background_color='darkseagreen', key='-mykey-'),
                            sg.Tab('Implied Volatility', iv_layout)]], key='-group1-', tab_location='top', selected_title_color='purple')],
            [sg.Button('Next', enable_events=True, key='-next-'), sg.Button('Exit', enable_events=True, key='-exit-')]
            ]

    window = sg.Window('Option Calculator', layout,
                    default_element_size=(12, 1))
    return window


def update_window(option_choice_str, option_method_str, option_kind_str):

    option_layout = []

    option_layout.append([sg.Text(f'{option_choice_str} {option_kind_str} Option via {option_method_str}', background_color='darkseagreen')])

    for input_value in UNIQUE_INPUT_VALUES:
        if input_value in input_values_dict[full_option_str]:
            option_layout.append([sg.Text(f'{input_value}:', background_color='darkseagreen', key=f'-{input_value}_label-'), sg.Input(key=f'-{input_value}-', visible=True)])

    # iv_layout = [[sg.Text('This is inside tab 5')],
    #             [sg.Input(key='-in4-')]]

    # layout = [[sg.TabGroup([[sg.Tab('Option Value', option_layout, background_color='darkseagreen', key='-mykey-'),
    #                         sg.Tab('Implied Volatility', iv_layout)]], key='-group1-', tab_location='top', selected_title_color='purple')],
    #         [sg.Button('Compute', enable_events=True, key='-compute-'), sg.Button('Menu', enable_events=True, key='-menu-')]
    #         ]
    option_layout.append([sg.Button('Compute', enable_events=True, key='-compute-'), sg.Button('Menu', enable_events=True, key='-menu-')])

    window = sg.Window('Option Calculator', option_layout, default_element_size=(12, 1))
    return window

# def update_drop_box_1(window):
#     print('update_drop_box_1')
#     select = values['-option_type-']
#     option_choice = methodology[select]
#     window['-option_method-'].update(value=option_choice[0], values=option_choice)
#     return window

# def update_drop_box_2(window, option_method_str=None):
#     print('update_drop_box_2 triggered')
#     select = values['-option_type-'] + ' ' + values['-option_method-']
#     # if option_method_str is None:
#     #     select = values['-option_type-'] + ' ' + values['-option_method-']
#     # else:
#     #     select = values['-option_type-'] + ' ' + option_method_str
#     input_fields = input_values_dict[select]
#     for input_field in UNIQUE_INPUT_VALUES:
#         if input_field in input_fields:
#             window[f'-{input_field}_label-'].update(visible=True)
#             window[f'-{input_field}-'].update(visible=True)
#         else:
#             window[f'-{input_field}_label-'].update(visible=False)
#             window[f'-{input_field}-'].update(visible=False)
#     return window

def compute_option_price(option_choice_str, option_method_str, option_kind_str, values):
    print('computation initialsied')
    # parse option_kind_str
    if option_kind_str == 'Call':
        params_option_kind = {'kind':'C'}
    else:
        params_option_kind = {'kind':'P'}

    params_str = input_values_dict[f'{option_choice_str} {option_method_str}']
    params = {key_str: float(values[f'-{key_str}-']) for key_str in params_str}

    # for param, val in params.items():

    option_str = f'{option_choice_str} {option_method_str}'
    print(option_str)
    print(params_option_kind)

    if option_str == 'European Black Scholes':
        option_calculator = EuropeanOptionPricer(**params)
        return option_calculator.get_option_premium(**params_option_kind)
    elif option_str == 'European Binominal Tree':
        option_calculator = BinominalTree(**params)
        params_option_kind['option_type'] = 'european'
        return option_calculator.get_option_premium(**params_option_kind)

    elif option_str == 'Geometric Asian Closed Form':
        option_calculator = GeometricAsianOptionPricer(**params)
        params_option_kind['method'] = 'closed'
        return option_calculator.get_option_premium(**params_option_kind)
    elif option_str == 'Geometric Asian Monte Carlo':
        params_option_kind['method'] = 'mcs'
        params_option_kind['m'] = params['m'] #asdasd
        del params['m']
        option_calculator = GeometricAsianOptionPricer(*params)
        return option_calculator.get_option_premium(**params_option_kind)

    elif option_str == 'Arithmetic Asian Monte Carlo':
        params_option_kind['method'] = 'mc'
        # params_option_kind['m'] = params['m'] #asdasd
        # del params['m']
        option_calculator = ArithmeticAsianOptionPricer(**params)
        return option_calculator.get_option_premium(**params_option_kind)
    elif option_str == 'Arithmetic Asian Monte Carlo with Control Variate':
        params_option_kind['method'] = 'cv'
        # params_option_kind['m'] = params['m'] #asdasd
        # del params['m']
        option_calculator = ArithmeticAsianOptionPricer(**params)
        return option_calculator.get_option_premium(**params_option_kind)

    elif option_str == 'Geometric Basket Closed Form':
        option_calculator = GeometricBasketOptionPricer(**params)
        params_option_kind['method'] = 'closed'
        return option_calculator.get_option_premium(**params_option_kind)
    elif option_str == 'Geometric Basket Monte Carlo':
        params_option_kind['method'] = 'mcs'
        params_option_kind['m'] = params['m'] #asdasd
        del params['m']
        option_calculator = GeometricBasketOptionPricer(**params)
        return option_calculator.get_option_premium(**params_option_kind)

    elif option_str == 'Arithmetic Basket Monte Carlo':
        option_calculator = ArithmeticAsianOptionPricer(**params)
        params_option_kind['mode'] = 'mc'
        return option_calculator.get_option_premium(**params_option_kind)
    elif option_str == 'Arithmetic Basket Monte Carlo with Control Variate':
        option_calculator = ArithmeticAsianOptionPricer(**params)
        params_option_kind['mode'] = 'cv'
        return option_calculator.get_option_premium(**params_option_kind)

    elif option_str == 'American Binominal Tree':
        option_calculator = ArithmeticAsianOptionPricer(**params)
        params_option_kind['option_type'] = 'american'
        return option_calculator.get_option_premium(**params_option_kind)
    
    return None

while True:

    event, values = window.read()

    print(event, values)
    if event == sg.WIN_CLOSED  or event=='-exit-':
        break
    elif event == '-option_type-':
        select = values[event]
        option_choice = methodology[select]
        window['-option_method-'].update(value=option_choice[0], values=option_choice)
    elif event == '-next-':
        option_choice_str = values['-option_type-']
        option_method_str = values['-option_method-']
        option_kind_str = values['-option_kind-']
        full_option_str = f'{option_choice_str} {option_method_str}'
        window.close()

        window2 = update_window(option_choice_str, option_method_str, option_kind_str)

        while event != sg.WIN_CLOSED:
            event2, values2 = window2.read()
            print(event2, values2)

            if event2 == '-compute-':
                option_choice_str = values['-option_type-']
                option_method_str = values['-option_method-']
                option_kind_str = values['-option_kind-']
                # print(option_choice_str, option_method_str, option_kind_str, values2)
                option_price = compute_option_price(option_choice_str, option_method_str, option_kind_str, values2)
                sg.Popup(f'Option Price: {option_price}', keep_on_top=True)
            elif event2 =='-menu-':
                window2.close()
                window = menu_window()
            elif event2 == sg.WIN_CLOSED  or event2 =='-exit-':
                break

    sg.popup_non_blocking(event, values)

window.close()