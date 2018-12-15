import diff_calc
import new_diff_calc
import requests
import pp_calc
import sys
import b_info
import configparser
from beatmap import Beatmap


def mod_str(mod):
    string = ""
    if mod.nf:
        string += "NF"
    if mod.ez:
        string += "EZ"
    if mod.hd:
        string += "HD"
    if mod.hr:
        string += "HR"
    if mod.dt:
        string += "DT"
    if mod.ht:
        string += "HT"
    if mod.nc:
        string += "NC"
    if mod.fl:
        string += "FL"
    if mod.so:
        string += "SO"
    return string


class mods:
    def __init__(self):
        self.nomod = 0,
        self.nf = 0
        self.ez = 0
        self.hd = 0
        self.hr = 0
        self.dt = 0
        self.ht = 0
        self.nc = 0
        self.fl = 0
        self.so = 0
        self.speed_changing = self.dt | self.ht | self.nc
        self.map_changing = self.hr | self.ez | self.speed_changing

    def update(self):
        self.speed_changing = self.dt | self.ht | self.nc
        self.map_changing = self.hr | self.ez | self.speed_changing


mod = mods()


def set_mods(mod, m):
    if m == "NF":
        mod.nf = 1
    if m == "EZ":
        mod.ez = 1
    if m == "HD":
        mod.hd = 1
    if m == "HR":
        mod.hr = 1
    if m == "DT":
        mod.dt = 1
    if m == "HT":
        mod.ht = 1
    if m == "NC":
        mod.nc = 1
    if m == "FL":
        mod.fl = 1
    if m == "SO":
        mod.so = 1


def return_values(c100_s, c50_s, misses_s, combo_s, file_name, mod_s):
    try:
        file = requests.get(b_info.main(file_name)).text.splitlines()
    except:
        print("ERROR: " + file_name + " not a valid beatmap")
        sys.exit(1)

    map = Beatmap(file)

    if combo_s == "":
        combo = map.max_combo
    else:
        combo = int(combo_s)

    mod_s = mod_s.upper()

    mod.dt = 0
    mod.ez = 0
    mod.fl = 0
    mod.hd = 0
    mod.hr = 0
    mod.ht = 0
    mod.nc = 0
    mod.nf = 0
    mod.so = 0

    if mod_s != "":
        mod_s = [mod_s[i:i + 2] for i in range(0, len(mod_s), 2)]
        for m in mod_s:
            set_mods(mod, m)
            mod.update()

    if c100_s == "":
        c100 = 0
    else:
        c100 = int(c100_s)

    if c50_s == "":
        c50 = 0
    else:
        c50 = int(c50_s)

    if misses_s == "":
        misses = 0
    else:
        misses = int(misses_s)

    mod_string = mod_str(mod)
    map.apply_mods(mod)
    diff = diff_calc.main(map)
    new_diff = new_diff_calc.main(map)
    pp, aim_value, speed_value, acc_value, old_aim_value, old_speed_value, old_pp, new_sr, td_pp = pp_calc.pp_calc(diff[0], diff[1], new_diff[0], new_diff[1], diff[3], misses, c100, c50, mod, combo)


    title = map.artist + " - " + map.title + "[" + map.version + "]"
    if mod_string != "":
        title += "+" + mod_string
    title += " (" + map.creator + ")\n"
    map_s = "Map: {}\n".format(title)
    difficulty_settings = "AR: {:.2f} CS: {:.2f} OD: {:.2f}\n".format(map.ar, map.cs, map.od)
    acc = "Acc: {:.2f}%\n\n".format(pp.acc_percent)
    circle_s = "Circles: {}\n".format(map.num_circles)
    slider_s = "Sliders: {}\n".format(map.num_sliders)
    spinner_s = "Spinners: {}\n".format(map.num_spinners)
    object_s = "Objects: {}\n\n".format(map.num_objects)
    comb_s = "Combo: {}/{}\n".format(int(combo), int(map.max_combo))
    miss_s = "Misses: {}\n\n".format(misses)
    aim_vs = "Aim Value: {:.2f}PP\n".format(aim_value)
    speed_vs = "Speed Value: {:.2f}PP\n".format(speed_value)
    acc_vs = "Acc Value: {:.2f}PP\n\n".format(acc_value)
    aim_ovs = "Old Aim Value: {:.2f}PP\n".format(old_aim_value)
    speed_ovs = "Old Speed Value: {:.2f}PP\n\n".format(old_speed_value)
    stars = "Old Star Rating: {:.2f}\n".format(diff[2])
    new_srs = "New Star Rating: {:.2f}\n\n".format(new_sr)
    old_pps = "Old Performance: {:.2f}PP\n".format(old_pp)
    td_pps = "Performance with TD: {:.2f}PP\n".format(td_pp)
    pp_s = "Performance: {:.2f}PP\n".format(pp.pp)

    return (map_s + difficulty_settings +  acc + circle_s + slider_s + spinner_s + object_s
            + comb_s + miss_s + aim_ovs + speed_ovs +
            aim_vs + speed_vs + acc_vs + stars + new_srs + old_pps + td_pps + pp_s)
