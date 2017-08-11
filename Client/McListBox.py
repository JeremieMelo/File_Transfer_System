import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk

class McListBox(ttk.Treeview):
    """use a ttk.TreeView as a multicolumn ListBox"""
    def __init__(self, master, table_header = None,table_list = None, *options, **args):
        self.table_header = table_header
        self.table_list = table_list
        self.tree = None
        self._setup_widgets(master)
        self._build_tree()
        super(McListBox, self).__init__()

    def _setup_widgets(self, master):
        self.container = master#ttk.Frame()
        #self.container.pack(fill='both', expand=False)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(master, columns=self.table_header, show="headings")
        self.vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        self.hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set,
            xscrollcommand=self.hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.container)
        self.vsb.grid(column=1, row=0, sticky='ns', in_=self.container)
        self.hsb.grid(column=0, row=1, sticky='ew', in_=self.container)

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        for col in self.table_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in self.table_list:
            #print(type(self.table_list), self.table_list)
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)+10
                if self.tree.column(self.table_header[ix],width=None)<col_w:
                    self.tree.column(self.table_header[ix], width=col_w+20)

        #print(self.container.width)

    def _rebuild_tree(self):
        self.tree.configure(columns=self.table_header)
        self._build_tree()

    def _set_header(self,header = None):
        self.table_header = header

    def _set_list(self,list = None):
        self.table_list = list
        
    def _selection(self):
        return(self.tree.selection())
    def _get_children(self, item = None):
        if(item):
            return self.tree.get_children(item)
        else:return self.tree.get_children()
def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))
if __name__ == "__main__" :
    # the test data ...
    car_header = ['car', 'repair']
    car_list = [
        ('Hyundai', 'brakes') ,
        ('Honda', 'light') ,
        ('Lexus', 'battery') ,
        ('Benz', 'wiper') ,
        ('Ford', 'tire') ,
        ('Chevy', 'air') ,
        ('Chrysler', 'piston') ,
        ('Toyota', 'brake pedal') ,
        ('BMW', 'seat')
    ]
    root = tk.Tk()
    root.wm_title("multicolumn ListBox")
    frm= ttk.Frame(root)
    frm.grid(row = 0, column = 0, sticky = 'news')
    mc_listbox = McListBox(frm,table_header=car_header,table_list=car_list)
    def update_table():
        for i in map(mc_listbox.tree.delete,mc_listbox.tree.get_children('')):
            pass
        mc_listbox._rebuild_tree()
        print(mc_listbox.tree.winfo_width())

    tk.Button(root,text="update",command=update_table).grid(row = 1, column = 0, sticky = 'nwes')
    root.mainloop()
