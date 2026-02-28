import tkinter as tk
from tkinter import messagebox, ttk
# from ztool.storage import repo 
# this can t run with it we can replace it with a mock repo for testing purposes



class Ztool(tk.Tk):
    def __init__(self, repo: None, registery: None):
        super().__init__()
        self.repo = repo
        self.registery = registery
        if (self.repo is None) or (self.registery is None):
            self.projects = []
        else:
            self.projects = self.repo.load()
        
        self.title("Ztool")
        self.geometry("860x600")
        self.style_config()
        
    def style_config(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("treeview", background="white", foreground="#000000", fieldbackground="white")
    
    def main_ui(self) -> None:
        top = ttk.Frame(self, padding=8, relief="raised")
        top.pack(fill="x") # fill the horizontal space of the window, allowing the top frame to expand and contract as the window is resized, while maintaining its height.
        ttk.Label(top, text="Tool Chest", font=("Segoe UI", 9, "bold")).pack(anchor="w") # anchor="w" aligns the label to the left (west) side of the top frame, ensuring that the "Tool Chest" title is positioned at the left edge of the frame for a clean and organized layout.
        action = ttk.Frame(top)
        action.pack(fill="x")
        ttk.Button(action, text="Create Project",).pack(side="left", padx=2) # command=self.create_project
        ttk.Button(action, text="Destroy Project", ).pack(side="left", padx=2) # command=self.remove_project
        
        main = ttk.Frame(self, padding=8)
        main.pack(fill="both", expand=True) #fill both horizontal and vertical space of the window, allowing the main frame to expand and contract as the window is resized, providing a flexible area for displaying project information and other content.
        ttk.Label(main, text="Projects").pack(anchor="w")
        
        columns = ("name", "path", "icon")
        self.tree = ttk.Treeview(main, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("name", text="Project Name")
        self.tree.heading("path", text="Project Path")
        self.tree.heading("icon", text="Project Icon")
        self.tree.column("name", width=180, stretch=False) #
        self.tree.column("path", width=470, stretch=True)
        self.tree.column("icon", width=170, stretch=True)
        
        scrollbar = ttk.Scrollbar(main, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        filter_bar = ttk.Frame(self, padding=8, relief="sunken") # sunken relief style to visually separate the filter bar from the main content area
        filter_bar.pack(fill="x", side="bottom")
        ttk.Label(filter_bar, text="Filter:").pack(side="left")
        self.filter_var = tk.StringVar()
        # self.filter_var.trace_add("write", self.update_filter) # trace_add method
        ttk.Entry(filter_bar, textvariable=self.filter_var).pack(side="left", fill="x", expand=True, padx=6)
        
        
# test
if __name__ == "__main__":
    app = Ztool(repo=None, registery=None)
    app.main_ui()
    app.mainloop() 
    