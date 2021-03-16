import tkinter as tk
import tkinter.ttk as ttk
import psutil
import time


class Application(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.initialize_user_interface()

    def initialize_user_interface(self):
        # Configure the root object for the Application
        self.root.title("Task manager")
        # Configure the background
        self.root.config(background="blue")
        # Button to kill the proccess
        self.delete_button = tk.Button(
            self.root, text="Delete", command=self.delete_data
        )
        self.delete_button.grid(row=5, column=3)
        # Button to refresh the process
        self.refresh_button = tk.Button(
            self.root, text="Refresh", command=self.Refresh_data
        )
        self.refresh_button.grid(row=5, column=2)
        # Button to exit
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=0, column=3)

        # Button to convert Gb to Mb
        self.mb_button = tk.Button(self.root, text="MB", command=self.mem_perMB)
        self.mb_button.grid(row=5, column=85)

        # Button to convert Mb to Gb
        self.gB_button = tk.Button(self.root, text="Gb", command=self.mem_perG)
        self.gB_button.grid(row=5, column=60)

        # Set the treeview
        self.tree = ttk.Treeview(self.root, columns=("Name", "ID"))

        # Set the heading (Attribute Names)
        self.tree.heading("#0", text="Pid")
        self.tree.heading("#1", text="%memory")
        self.tree.heading("#2", text="$cpu")

        # Specify attributes of the columns (We want to stretch it!)
        self.tree.column("#0", stretch=tk.YES)
        self.tree.column("#1", stretch=tk.YES)
        self.tree.column("#2", stretch=tk.YES)

        self.tree.grid(row=4, columnspan=4, sticky="nsew")
        self.treeview = self.tree

        # Define the variables to control the row of the treeview
        self.id = 0
        self.iid = 0
        # Insert in the treeview the dates of proccess
        for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):
            self.treeview.insert(
                "",
                "end",
                iid=self.iid,
                text=proc.pid,
                values=(
                    proc.memory_percent(),
                    proc.cpu_percent() / psutil.cpu_count(),
                ),
            )
            # In this case we will add 1 to the variable for each interaction of the loop
            self.iid = self.iid + 1
            self.id = self.id + 1

        # The label to show the proccess number in the system
        process_label = tk.Label(
            self.root,
            bg="black",
            fg="green",
            anchor="center",
            font="Arial 11 bold",
            width=6,
        )
        process_label.grid(row=5, column=1, sticky="w")
        process_label.config(text="{}".format(self.id))

        digi = tk.Label(
            self.root,
            text="N# process:",
            font="arial 11 bold",
            bg="midnight blue",
            fg="white",
        )
        digi.grid(row=5, column=0, sticky="e")
        digim = tk.Label(
            self.root,
            text="Disk free:",
            font="arial 11 bold",
            bg="midnight blue",
            fg="white",
        )
        digim.grid(row=6, column=0, sticky="e")

        # The label to show the free disk in the systems
        disk_label = tk.Label(
            self.root,
            bg="black",
            fg="green",
            anchor="center",
            font="Arial 11 bold",
            width=15,
        )
        disk_label.grid(row=6, column=1, sticky="w")
        disk = psutil.disk_usage("/")
        disk_label.config(text="{}Mb".format((disk.free / 1048576)))

        ram = tk.Label(
            self.root,
            text="Ram free:",
            font="arial 11 bold",
            bg="midnight blue",
            fg="white",
        )
        ram.grid(row=7, column=0, sticky="e")

        # The label to show the free ram in the system
        ram_label = tk.Label(
            self.root,
            bg="black",
            fg="green",
            anchor="center",
            font="Arial 11 bold",
            width=15,
        )
        ram_label.grid(row=7, column=1, sticky="w")
        ram = psutil.virtual_memory()
        ram_label.config(text="{}Mb".format((ram.free / 1048576)))

    # The function to kill the proccess
    def delete_data(self):
        row_id = int(self.tree.focus())
        print(self.treeview.item(row_id, option="text"))
        # my example
        parent = psutil.Process(self.treeview.item(row_id, option="text"))
        for child in parent.children(
            recursive=True
        ):  # or parent.children() for recursive=False
            child.kill()
        parent.kill()
        self.treeview.delete(row_id)
        self.Refresh_data()

    # Clean the table and Reinsert the data , call the differents functions like N_pro for show the number of proccess
    def Refresh_data(self):
        self.tree.delete(*self.tree.get_children())
        self.idd = 0
        self.id = 0
        self.Insert_data()
        self.N_pro()
        self.mem_perMB()
        self.ram_perMb()

    # Insert the data into the table
    def Insert_data(self):
        for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):

            self.treeview.insert(
                "",
                "end",
                iid=self.iid,
                text=proc.pid,
                values=(proc.memory_percent(), proc.cpu_percent()),
            )
            self.iid = self.iid + 1
            self.id = self.id + 1

    # Change the disk free to Mb
    def mem_perMB(self):

        disk_label = tk.Label(
            self.root,
            bg="black",
            fg="green",
            anchor="center",
            font="Arial 11 bold",
            width=15,
        )
        disk_label.grid(row=6, column=1, sticky="w")
        disk = psutil.disk_usage("/")
        disk_label.config(text="{}Mb".format((disk.free / 1048576)))

        self.ram_perMb()

    # Change the disk free to Gb
    def mem_perG(self):

        disk_label = tk.Label(
            self.root,
            bg="black",
            fg="green",
            anchor="center",
            font="Arial 11 bold",
            width=15,
        )
        disk_label.grid(row=6, column=1, sticky="w")
        disk = psutil.disk_usage("/")
        disk_label.config(text="{}Gb".format(round((disk.free / 1073741824), 2)))

        self.ram_perG()

    # Show the number of proccess
    def N_pro(self):
        process_label = tk.Label(
            self.root,
            bg="black",
            fg="green",
            anchor="center",
            font="Arial 11 bold",
            width=15,
        )
        process_label.grid(row=5, column=1, sticky="w")
        process_label.config(text="{}".format(self.id))

    # Change the free ram to Gb
    def ram_perG(self):

        ram_label = tk.Label(
            self.root,
            bg="black",
            fg="green",
            anchor="center",
            font="Arial 11 bold",
            width=15,
        )
        ram_label.grid(row=7, column=1, sticky="w")
        ram = psutil.virtual_memory()
        ram_label.config(text="{}Gb".format(round((ram.free / 1073741824), 2)))

    # Change free ram to Mb
    def ram_perMb(self):

        ram_label = tk.Label(
            self.root,
            bg="black",
            fg="green",
            anchor="center",
            font="Arial 11 bold",
            width=15,
        )
        ram_label.grid(row=7, column=1, sticky="w")
        ram = psutil.virtual_memory()
        ram_label.config(text="{}Mb".format((ram.free / 1048576)))


app = Application(tk.Tk())
app.root.mainloop()