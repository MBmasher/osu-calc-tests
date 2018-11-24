import tkinter
import calc
import sys


# Function used to kill the program entirely.


def kill():
    sys.exit()


def calculate_pp():
    global map_link, c100, c50, miss, combo, info_l, alpha, beta, d_
    info_l["text"] = calc.return_values(c100.get(),
                                        c50.get(),
                                        miss.get(),
                                        combo.get(),
                                        map_link.get(),
                                        mods.get(),
                                        (float(alpha.get()),
                                         float(beta.get()),
                                         float(c_.get()),
                                         float(d_.get())))


while True:
    root = tkinter.Tk()
    root.resizable(width=False, height=False)
    root.title("osu-calc")

    tkinter.Label(root, text="Beatmap ID:").grid(row=0, column=0)
    tkinter.Label(root, text="(Optional) Amount of 100s:").grid(row=1, column=0)
    tkinter.Label(root, text="(Optional) Amount of 50s:").grid(row=2, column=0)
    tkinter.Label(root, text="(Optional) Amount of misses:").grid(row=3, column=0)
    tkinter.Label(root, text="(Optional) Combo:").grid(row=4, column=0)
    tkinter.Label(root, text="(Optional) Mods:").grid(row=5, column=0)
    tkinter.Label(root, text="alpha:").grid(row=6, column=0)
    tkinter.Label(root, text="beta:").grid(row=7, column=0)
    tkinter.Label(root, text="c:").grid(row=8, column=0)
    tkinter.Label(root, text="d:").grid(row=9, column=0)
    tkinter.Label(root, text="Proposed variables: alpha=??, beta=??, c=??, d=??").grid(row=10, column=0, columnspan=2)

    map_link = tkinter.Entry(root, width=40)
    map_link.grid(row=0, column=1)

    c100 = tkinter.Entry(root, width=40)
    c100.grid(row=1, column=1)

    c50 = tkinter.Entry(root, width=40)
    c50.grid(row=2, column=1)

    miss = tkinter.Entry(root, width=40)
    miss.grid(row=3, column=1)

    combo = tkinter.Entry(root, width=40)
    combo.grid(row=4, column=1)

    mods = tkinter.Entry(root, width=40)
    mods.grid(row=5, column=1)

    alpha = tkinter.Entry(root, width=40)
    alpha.grid(row=6, column=1)

    beta = tkinter.Entry(root, width=40)
    beta.grid(row=7, column=1)

    c_ = tkinter.Entry(root, width=40)
    c_.grid(row=8, column=1)

    d_ = tkinter.Entry(root, width=40)
    d_.grid(row=9, column=1)

    tkinter.Button(root, fg="blue", text="Calculate pp!", command=calculate_pp).grid(row=11, column=0, columnspan=2)

    info_l = tkinter.Label(root)
    info_l.grid(row=12, column=0, columnspan=2)

    # If window is closed, stop the program.
    root.protocol("WM_DELETE_WINDOW", kill)

    root.mainloop()
