from tkinter import *

class OptionPricerGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('Options Pricer')
        self._setup_mainframe()
        self._setup_initial_page()

        self._first_layer_choice = None

        self.root.mainloop()

    def _setup_mainframe(self):
        self.mainframe = Frame(self.root)
        self.mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)
        self.mainframe.pack(pady = 100, padx = 100)

    """
    Layer 0
    """

    def _setup_initial_page(self):
        # Create a Tkinter variable
        self.option_choice = StringVar(self.root)

        # Dictionary with options
        option_choices = { 'European', 'American', 'Geometric Asian', 'Arithmetic Asian', 'Geometric Basket', 'Arithmetic Basket'}
        self.option_choice.set('European') # set the default option

        popupMenu = OptionMenu(self.mainframe, self.option_choice, *option_choices)
        Label(self.mainframe, text="1. Choose an option type").grid(row = 1, column = 1)
        popupMenu.grid(row = 2, column =1)

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

    def destroy_option_dropdown(self, last_choice):
        print( self.option_choice.get() )
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
        # link function to change dropdown

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
        Label(self.mainframe, text="2. Choose the methodology").grid(row = 3, column = 1)
        self.first_popupmenu.grid(row = 4, column =1)

        # link function to change dropdown
        self.european_option_methods.trace('w', self.select_european_option_dropdown)

    def select_european_option_dropdown(self, *args):
        print(self.european_option_methods.get())
    
    def american_option(self):
        # Create a Tkinter variable
        self.american_option_methods = StringVar(self.root)

        # Dictionary with options
        american_option_methods_choices = {'Binominal Tree' }
        self.american_option_methods.set('-Select One-') # set the default option

        self.first_popupmenu = OptionMenu(self.mainframe, self.american_option_methods, *american_option_methods_choices)
        Label(self.mainframe, text="2. Choose the methodology").grid(row = 3, column = 1)
        self.first_popupmenu.grid(row = 4, column =1)

        # link function to change dropdown
        self.american_option_methods.trace('w', self.select_american_option_dropdown)

    def select_american_option_dropdown(self, *args):
        print(self.american_option_methods.get())

    def geometric_asian_option(self):
        # Create a Tkinter variable
        self.geometric_asian_option_methods = StringVar(self.root)

        # Dictionary with options
        geometric_asian_option_methods_choices = { 'Closed Form', 'Monte Carlo' }
        self.geometric_asian_option_methods.set('-Select One-') # set the default option

        self.first_popupmenu = OptionMenu(self.mainframe, self.geometric_asian_option_methods, *geometric_asian_option_methods_choices)
        Label(self.mainframe, text="2. Choose the methodology").grid(row = 3, column = 1)
        self.first_popupmenu.grid(row = 4, column =1)

        # link function to change dropdown
        self.geometric_asian_option_methods.trace('w', self.select_geometric_asian_option_dropdown)

    def select_geometric_asian_option_dropdown(self, *args):
        print(self.geometric_asian_option_methods.get())

    def arithmetic_asian_option(self):
        # Create a Tkinter variable
        self.arithmetic_asian_option_methods = StringVar(self.root)

        # Dictionary with options
        arithmetic_asian_option_methods_choices = { 'Monte Carlo', 'Monte Carlo with Control Variate' }
        self.arithmetic_asian_option_methods.set('-Select One-') # set the default option

        self.first_popupmenu = OptionMenu(self.mainframe, self.arithmetic_asian_option_methods, *arithmetic_asian_option_methods_choices)
        Label(self.mainframe, text="2. Choose the methodology").grid(row = 3, column = 1)
        self.first_popupmenu.grid(row = 4, column =1)

        # link function to change dropdown
        self.arithmetic_asian_option_methods.trace('w', self.select_arithmetic_asian_option_dropdown)

    def select_arithmetic_asian_option_dropdown(self, *args):
        print(self.arithmetic_asian_option_methods.get())

"""
Layer 2
"""
 
        



def main():
    OptionPricerGUI()

if __name__ == '__main__':
    main()