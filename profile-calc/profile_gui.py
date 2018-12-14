import profile_calc
from tkinter import *
from tkinter.ttk import *
import sys
import configparser
import requests

key = input("API key (get it at https://old.ppy.sh/p/api): ")

username = input("profile username? ")

# Function used to kill the program entirely.

def kill():
    sys.exit()


def sort_values(sort_by):
    global pp_info, tree, root

    if sort_by == "old_pp":
        sorted_list = [i for i in
                       sorted(pp_info, key=lambda x: x[2], reverse=True)]
    elif sort_by == "new_pp":
        sorted_list = [i for i in
                       sorted(pp_info, key=lambda x: x[1], reverse=True)]
    else:
        sorted_list = [i for i in
                       sorted(pp_info, key=lambda x: x[2] / float(x[1]))]

    tree.destroy()

    tree = Treeview(root)

    tree.config(columns=("1", "2", "3"))
    tree.column("1", stretch=False, width=150)
    tree.column("2", stretch=False, width=150)
    tree.column("3", stretch=False, width=150)
    tree.heading("1", text="Old Performance")
    tree.heading("2", text="Proposed Performance")
    tree.heading("3", text="Percent Change")

    for i in sorted_list:
        try:
            tree.insert("", "end", text=i[0], values=("{:.2f}PP".format(i[2]),
                                                      "{:.2f}PP".format(i[1]),
                                                      "{:.2f}%".format(100 * i[1] / float(i[2]))))
        except:
            tree.insert("", "end", text=i[0], values=("{:.2f}PP".format(i[2]),
                                                      "{:.2f}PP".format(i[1]),
                                                      "{:.2f}%".format(0)))

    tree.pack(fill='both', expand=True)



try:
    url = 'https://osu.ppy.sh/api/get_user?k={}&u={}'.format(key, username)
    jsonurl = str(requests.get(url).text)
    jsonurl = jsonurl[1:-2]
    profile_split = jsonurl.split("},")[0]
    profile_info = profile_split[1:-1].split(",")
    profile_list = [i.split(":") for i in profile_info]
    profile_pp = float(profile_list[11][1][1:-1])
except:
    try:
        url = 'https://osu.ppy.sh/api/get_user?k={}&u=peppy'.format(key)
        jsonurl = str(requests.get(url).text)
        jsonurl = jsonurl[1:-2]
        profile_split = jsonurl.split("},")[0]
        profile_info = profile_split[1:-1].split(",")
        profile_list = [i.split(":") for i in profile_info]
        profile_pp = float(profile_list[11][1][1:-1])
    except:
        while True:
            root = Tk()
            root.title("osu-calc")

            w = Text(root)
            w.insert(1.0,"Invalid API key. Make sure that you have typed your API key correctly.")
            w.pack()
            w.configure(state="disabled")

            root.protocol("WM_DELETE_WINDOW", kill)

            root.mainloop()
    while True:
        root = Tk()
        root.title("osu-calc")

        w = Text(root)
        w.insert(1.0, "Invalid username. Check to see if you made a typo or maybe the user is restricted.")
        w.pack()
        w.configure(state="disabled")

        root.protocol("WM_DELETE_WINDOW", kill)

        root.mainloop()

while True:

    root = Tk()
    root.resizable(width=False, height=True)
    root.geometry("1200x800")
    root.title("osu-calc")

    pp_info = profile_calc.return_values(username, key)

    old_sorted_list = [i for i in
                       sorted(pp_info, key=lambda x: x[2], reverse=True)]

    old_pp = sum([old_sorted_list[i][2] * (0.95 ** i) for i in range(len(old_sorted_list))])

    new_sorted_list = [i for i in
                       sorted(pp_info, key=lambda x: x[1], reverse=True)]

    new_pp = sum([new_sorted_list[i][1] * (0.95 ** i) for i in range(len(new_sorted_list))])

    Label(root, text="Old Total Performance: {:.2f}PP".format(profile_pp)).pack()
    Label(root, text="New Total Performance: {:.2f}PP".format(new_pp + (profile_pp - old_pp))).pack()

    #Label(root, text="Old Total Performance: {:.2f}PP".format(old_pp)).pack()
    #Label(root, text="New Total Performance: {:.2f}PP".format(new_pp)).pack()

    Button(root, text="Sort by Old Performance", command=lambda: sort_values("old_pp")).pack()
    Button(root, text="Sort by Proposed Performance", command=lambda: sort_values("new_pp")).pack()
    Button(root, text="Sort by Percent Change", command=lambda: sort_values("percent")).pack()

    tree = Treeview(root)

    tree.config(columns=("1", "2", "3"))
    tree.column("1", stretch=False, width=150)
    tree.column("2", stretch=False, width=150)
    tree.column("3", stretch=False, width=150)
    tree.heading("1", text="Old Performance")
    tree.heading("2", text="Proposed Performance")
    tree.heading("3", text="Percent Change")

    sorted_list = [i for i in
                   sorted(pp_info, key=lambda x: x[1], reverse=True)]

    for i in sorted_list:
        try:
            tree.insert("", "end", text=i[0], values=("{:.2f}PP".format(i[2]),
                                                      "{:.2f}PP".format(i[1]),
                                                      "{:.2f}%".format(100 * i[1] / float(i[2]))))
        except:
            tree.insert("", "end", text=i[0], values=("{:.2f}PP".format(i[2]),
                                                      "{:.2f}PP".format(i[1]),
                                                      "{:.2f}%".format(0)))

    tree.pack(fill="both", expand=True)

    # If window is closed, stop the program.
    root.protocol("WM_DELETE_WINDOW", kill)

    root.mainloop()
