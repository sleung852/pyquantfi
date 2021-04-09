from tkinter import *

class OptionPricerGUI:
    def __init__(self):

        self.input_values = {
            'European_BS': ['S', 'K', 'T', 'sigma', 'r', 'q'],
            'European_BT': ['S', 'K', 'T', 'sigma', 'r', 'n'],
            'Asian_Geo_CF': ['S', 'K', 'T', 'sigma', 'r', 'n'],
            'Asian_Geo_MCS': ['S', 'K', 'T', 'sigma', 'r', 'n', 'm'],
            'Asian_Ari_MCS': ['S', 'K', 'T', 'sigma', 'r', 'n', 'm'],
            'Asian_Ari_MCS_CV': ['S', 'K', 'T', 'sigma', 'r', 'n', 'm'],
            'Basket_Geo_CF': ['S1', 'S2', 'K', 'T', 'sigma1', 'sigma2', 'r', 'rho'],
            'Basket_Geo_MCS': ['S1', 'S2', 'K', 'T', 'sigma1', 'sigma2', 'r', 'rho', 'm'],
            'Basket_Ari_MCS': ['S1', 'S2', 'K', 'T', 'sigma1', 'sigma2', 'r', 'rho', 'n', 'm'],
            'Basket_Ari_MCS_CV': ['S1', 'S2', 'K', 'T', 'sigma1', 'sigma2', 'r', 'rho', 'n', 'm'],
            'American_BT': ['S', 'K', 'T', 'sigma', 'r', 'n'],
        }

        self._reset_stored_values()

        self.root = Tk()
        self.root.title('Options Pricer')
        self._setup_mainframe()
        self._setup_initial_page()

        self._first_layer_choice = None
        self._second_layer_choice = []

        self.root.mainloop()

    def _setup_mainframe(self):
        self.mainframe = Frame(self.root)
        self.mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)
        self.mainframe.pack(pady = 20, padx = 20)

    def _reset_stored_values(self):
        self.storage = {i: [-1, None] for i in ['S','sigma', 'S1', 'S2', 'K', 'T', 'sigma1', 'sigma2', 'r', 'rho', 'n', 'm']}

    """
    Layer 0
    """

    def _setup_initial_page(self):
        # Create a Tkinter variable
        self.option_choice = StringVar(self.root)

        # Dictionary with options
        option_choices = { 'European', 'American', 'Geometric Asian', 'Arithmetic Asian', 'Geometric Basket', 'Arithmetic Basket'}
        self.option_choice.set('- Select One -') # set the default option

        popupMenu = OptionMenu(self.mainframe, self.option_choice, *option_choices)
        Label(self.mainframe, text="1. Choose an option type", anchor=W).grid(row = 1, column = 1)
        popupMenu.grid(row = 2, column = 1)

        self.option_choice.trace('w', self.select_option_dropdown)

    def select_option_dropdown(self, *args):
        print( self.option_choice.get() )

        # destroy previous drop down menu
        if self._first_layer_choice is None:
            pass
        else:
            self.first_popupmenu.destroy()

        # create new drop down menu
        if self.option_choice.get() == 'European':
            self.european_option()
        elif self.option_choice.get() == 'American':
            self.american_option()
        elif self.option_choice.get() == 'Geometric Asian':
            self.geometric_asian_option()
        elif self.option_choice.get() == 'Arthmetic Asian':
            self.arithmetic_asian_option()
        elif self.option_choice.get() == 'Geometric Basket':
            self.geometric_asian_option()
        elif self.option_choice.get() == 'Arthmetic Basket':
            self.arithmetic_asian_option()

        self._first_layer_choice = self.option_choice.get()
        # link function to change dropdown

    # def destroy_option_dropdown(self, last_choice):
    #     print( self.option_choice.get() )
    #     if self.option_choice.get() == 'European':
    #         self.european_option()
    #     elif self.option_choice.get() == 'American':
    #         self.american_option()
    #     elif self.option_choice.get() == 'Geometric Asian':
    #         self.geometric_asian_option()
    #     elif self.option_choice.get() == 'Arthmetic Asian':
    #         self.arithmetic_asian_option()
    #     elif self.option_choice.get() == 'Geometric Basket':
    #         self.geometric_basket_option()
    #     elif self.option_choice.get() == 'Arthmetic Basket':
    #         self.arithmetic_basket_option()
    #     # link function to change dropdown

    """
    Layer 1
    """
        
    def european_option(self):
        # Create a Tkinter variable
        self.european_option_methods = StringVar(self.root)

        # Dictionary with options
        european_option_methods_choices = { 'Blackscholes', 'Binominal Tree' }
        self.european_option_methods.set('-Select One-') # set the default option

        self.first_popupmenu = OptionMenu(self.mainframe, self.european_option_methods, *european_option_methods_choices)
        Label(self.mainframe, text="2. Choose the methodology", anchor=W).grid(row = 3, column = 1)
        self.first_popupmenu.grid(row = 4, column =1)

        # link function to change dropdown
        self.european_option_methods.trace('w', self.select_european_option_dropdown)

    def select_european_option_dropdown(self, *args):
        print(self.european_option_methods.get())
        if self.european_option_methods.get() == "Blackscholes":
            self.setup_entry_form('European_BS')
        elif self.european_option_methods.get() == "Binominal Tree":
            self.setup_entry_form('European_BT')
    
    def american_option(self):
        # Create a Tkinter variable
        self.american_option_methods = StringVar(self.root)

        # Dictionary with options
        american_option_methods_choices = {'Binominal Tree' }
        self.american_option_methods.set('-Select One-') # set the default option

        self.first_popupmenu = OptionMenu(self.mainframe, self.american_option_methods, *american_option_methods_choices)
        Label(self.mainframe, text="2. Choose a methodology", anchor=W).grid(row = 3, column = 1)
        self.first_popupmenu.grid(row = 4, column =1)

        # link function to change dropdown
        self.american_option_methods.trace('w', self.select_american_option_dropdown)

    def select_american_option_dropdown(self, *args):
        print(self.american_option_methods.get())
        if self.american_option_methods.get() == "Binominal Tree":
            self.setup_entry_form('American_BT')

    def geometric_asian_option(self):
        # Create a Tkinter variable
        self.geometric_asian_option_methods = StringVar(self.root)

        # Dictionary with options
        geometric_asian_option_methods_choices = { 'Closed Form', 'Monte Carlo' }
        self.geometric_asian_option_methods.set('-Select One-') # set the default option

        self.first_popupmenu = OptionMenu(self.mainframe, self.geometric_asian_option_methods, *geometric_asian_option_methods_choices)
        Label(self.mainframe, text="2. Choose a methodology", anchor=W).grid(row = 3, column = 1)
        self.first_popupmenu.grid(row = 4, column =1)

        # link function to change dropdown
        self.geometric_asian_option_methods.trace('w', self.select_geometric_asian_option_dropdown)

    def select_geometric_asian_option_dropdown(self, *args):
        print(self.geometric_asian_option_methods.get())
        if self.geometric_asian_option_methods.get() == "Closed Form":
            self.setup_entry_form('Asian_Geo_CF')
        elif self.geometric_asian_option_methods.get() == "Monte Carlo":
            self.setup_entry_form('Asian_Geo_MCS')

    def arithmetic_asian_option(self):
        # Create a Tkinter variable
        self.arithmetic_asian_option_methods = StringVar(self.root)

        # Dictionary with options
        arithmetic_asian_option_methods_choices = { 'Monte Carlo', 'Monte Carlo with Control Variate' }
        self.arithmetic_asian_option_methods.set('-Select One-') # set the default option

        Label(self.mainframe, text="2. Choose a methodology", anchor=W).grid(row = 3, column = 1)
        self.first_popupmenu = OptionMenu(self.mainframe, self.arithmetic_asian_option_methods, *arithmetic_asian_option_methods_choices)
        self.first_popupmenu.grid(row = 4, column =1)

        # link function to change dropdown
        self.arithmetic_asian_option_methods.trace('w', self.select_arithmetic_asian_option_dropdown)

    def select_arithmetic_asian_option_dropdown(self, *args):
        print(self.arithmetic_asian_option_methods.get())
        if self.arithmetic_asian_option_methods.get() == "Monte Carlo":
            self.setup_entry_form('Asian_Ari_MCS')
        elif self.arithmetic_asian_option_methods.get() == "Monte Carlo with Control Variate":
            self.setup_entry_form('Asian_Ari_MCS_CV')

    def geometric_basket_option(self):
        # Create a Tkinter variable
        self.geometric_asian_option_methods = StringVar(self.root)

        # Dictionary with options
        geometric_asian_option_methods_choices = { 'Closed Form', 'Monte Carlo' }
        self.geometric_asian_option_methods.set('-Select One-') # set the default option

        self.first_popupmenu = OptionMenu(self.mainframe, self.geometric_asian_option_methods, *geometric_asian_option_methods_choices)
        Label(self.mainframe, text="2. Choose a methodology", anchor=W).grid(row = 3, column = 1)
        self.first_popupmenu.grid(row = 4, column =1)

        # link function to change dropdown
        self.geometric_asian_option_methods.trace('w', self.select_geometric_asian_option_dropdown)

    def select_geometric_basket_option_dropdown(self, *args):
        print(self.geometric_asian_option_methods.get())
        if self.geometric_asian_option_methods.get() == "Closed Form":
            self.setup_entry_form('Basket_Geo_CF')
        elif self.geometric_asian_option_methods.get() == "Monte Carlo":
            self.setup_entry_form('Basket_Geo_MCS')

    def arithmetic_basket_option(self):
        # Create a Tkinter variable
        self.arithmetic_asian_option_methods = StringVar(self.root)

        # Dictionary with options
        arithmetic_asian_option_methods_choices = { 'Monte Carlo', 'Monte Carlo with Control Variate' }
        self.arithmetic_asian_option_methods.set('-Select One-') # set the default option

        Label(self.mainframe, text="2. Choose a methodology", anchor=W).grid(row = 3, column = 1)
        self.first_popupmenu = OptionMenu(self.mainframe, self.arithmetic_asian_option_methods, *arithmetic_asian_option_methods_choices)
        self.first_popupmenu.grid(row = 4, column =1)

        # link function to change dropdown
        self.arithmetic_asian_option_methods.trace('w', self.select_arithmetic_asian_option_dropdown)

    def select_arithmetic_basket_option_dropdown(self, *args):
        print(self.arithmetic_asian_option_methods.get())
        if self.arithmetic_asian_option_methods.get() == "Monte Carlo":
            self.setup_entry_form('Basket_Ari_MCS')
        elif self.arithmetic_asian_option_methods.get() == "Monte Carlo with Control Variate":
            self.setup_entry_form('Basket_Ari_MCS_CV')
    
    """
    Layer 2
    """

    def setup_entry_form(self, input_string):
        if len(self._second_layer_choice) == 0:
            pass
        else:
            for item in self._second_layer_choice:
                item.destroy()

        Label(self.mainframe, text="3. Enter parameters", anchor=W).grid(row = 5, column = 1)
        row_counter = 6
        for val in self.input_values[input_string]:
            # for i_row in range(6, 10):
            label_temp = Label(self.mainframe, text=val)
            label_temp.grid(row = row_counter, column = 1)
            entry_temp = Entry(self.mainframe, width=5)
            entry_temp.grid(row = row_counter, column = 2)
            self.storage[input_string][1] = entry_temp 
            self._second_layer_choice.append(label_temp)
            self._second_layer_choice.append(entry_temp)
            row_counter+=1
        
        button_confirm = Button(self.mainframe, text='Calculate', command=self.calculate)
        button_confirm.grid(row=row_counter, column=1)
        self._second_layer_choice.append(button_confirm)
        
    def _check_storage_is_empty(self):
        """
        To check whether 
        """
        for key, values in self.storage.items():
            if values[1] is not None:
                return False
        return True

    def _get_storage_valid_keys(self):
        valid_keys = []
        for key, values in self.storage.items():
            if values[1] is not None:
                valid_keys.append(key)
        return valid_keys

    def _get_values(self):
        valid_keys = self._get_storage_valid_keys()
        for key in valid_keys:
            self.storage[key][0] = self.storage[key][1].get()

    def calculate(self):
        print('Gather parameters')
        self._get_values()
        print('Print text calculating')
        Label(self.mainframe, text='Loading', '')
        print('Run functions')
        print('Print values')


def main():
    OptionPricerGUI()

if __name__ == '__main__':
    main()