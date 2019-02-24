import os
import tkinter as tk
import process

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.processing = False
        self.triple_list = [] # list of triples to send to neo4j
        
    def create_widgets(self):
        # params
        text_height = 10
        text_width = 10
        offset = 5
        start = text_width // 2 - offset

        # text box
        self.text = tk.Text(self)
        self.text.grid(row=0, column=0, columnspan=text_height, rowspan=text_width)
        self.text.bind('<ButtonRelease-1>', self.build)

        # open
        self.open = tk.Button(self, text='open', command=self.open)
        self.open.grid(row=text_height+1, column=start)

        # save button
        self.save = tk.Button(self, text='save', command=self.save)
        self.save.grid(row=text_height+1, column=start+1)

        # exit button
        self.exit = tk.Button(self, text='exit', fg='red',
                              command=self.master.destroy)
        self.exit.grid(row=text_height+1, column=start+2)

        # start processing
        self.process = tk.Button(self, text='process', command=self.process)
        self.process.grid(row=text_height+1, column=start+3)
        
    def process(self):
        if self.processing:
            # call process.py (to send values to neo4j)
            self.text.config(bg='#ffffff')
            self.processing = False
            # only push triple if it is filled
            if None not in self.triple:
                self.triple_list.append(self.triple)
            process.push(self.triple_list)
        
        else: # do processing of text
            self.text.config(bg='#cccccc')
            self.processing = True

            # triple to be filled
            self.triple = [None, None, None]

            # display triple
            self.relation = tk.Label(self, text='')
            self.relation.grid(row=12, columnspan=10)
        
    def build(self, event):
        if self.processing:
            selection = self.text.selection_get()

            # check which part of triple we are updating
            if not self.triple[0]:
                self.triple[0] = selection
            elif not self.triple[1]:
                self.triple[1] = selection
            elif not self.triple[2]:
                self.triple[2] = selection
            else:
                # save the triple, reset it, place selection
                self.triple_list.append(self.triple)
                self.triple = [selection, None, None]

            # update text
            self.relation['text'] = f'({self.triple[0]})-[{self.triple[1]}]->({self.triple[2]})'
            
    def open(self):
        """ Currently just opens the main file
        """
        text = ''
        with open('./raw_notes/main', 'r') as f:
            lines = f.readlines()
            text = "".join(lines)

        self.text.insert('end', text)

    def save(self):
        input_text = self.text.get("1.0", 'end-1c')

        file_name = input_text.split('\n', 1)[0]
        
        with open('./raw_notes/' + file_name, 'w') as f:
            f.write(input_text)

        
root = tk.Tk()
app = Application(master=root)

app.mainloop()
