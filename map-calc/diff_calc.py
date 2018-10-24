import math


def main(file, balancing_values):
    map = file
    objects = []
    radius = (512 / 16) * (1. - 0.7 * (map.cs - 5) / 5);

    class consts:
        decay_base = [0.3, 0.15]

        almost_diameter = 90

        stream_spacing = 110
        single_spacing = 125

        weight_scaling = [1400, 26.25]

        circlesize_buff_threshhold = 30

    class d_obj:
        def __init__(self, base_object, radius, prev):
            radius = float(radius)
            self.ho = base_object
            self.strains = [1, 1]
            self.norm_start = 0
            self.norm_end = 0
            self.scaling_factor = 52.0 / radius
            if radius < consts.circlesize_buff_threshhold:
                self.scaling_factor *= 1 + min((consts.circlesize_buff_threshhold - radius), 5) / 50.0
            self.norm_start = [float(self.ho.pos[0]) * self.scaling_factor, float(self.ho.pos[1]) * self.scaling_factor]

            self.norm_end = self.norm_start
            # Calculate speed
            self.calculate_strain(prev, 0)
            # Calculate aim
            self.calculate_strain(prev, 1)

        def calculate_strain(self, prev, dtype):
            if (prev == None):
                return
            res = 0
            time_elapsed = int(self.ho.time) - int(prev.ho.time)
            decay = math.pow(consts.decay_base[dtype], time_elapsed / 1000.0)
            scaling = consts.weight_scaling[dtype]
            if self.ho.h_type == 1 or self.ho.h_type == 2:
                dis = math.sqrt(
                    math.pow(self.norm_start[0] - prev.norm_end[0], 2) + math.pow(self.norm_start[1] - prev.norm_end[1],
                                                                                  2))

                res = self.spacing_weights(dis, dtype) * scaling
            res /= max(time_elapsed, 50)
            self.strains[dtype] = prev.strains[dtype] * decay + res

        def spacing_weights(self, distance, diff_type):
            if diff_type == 0:
                if distance > consts.single_spacing:
                    return 2.5
                elif distance > consts.stream_spacing:
                    return 1.6 + 0.9 * (distance - consts.stream_spacing) / (
                            consts.single_spacing - consts.stream_spacing)
                elif distance > consts.almost_diameter:
                    return 1.2 + 0.4 * (distance - consts.almost_diameter) / (
                            consts.stream_spacing - consts.almost_diameter)
                elif distance > (consts.almost_diameter / 2.0):
                    return 0.95 + 0.25 * (distance - consts.almost_diameter / 2.0) / (consts.almost_diameter / 2.0)
                else:
                    return 0.95
            elif diff_type == 1:
                return math.pow(distance, 0.99)
            else:
                return 0.0

    def calculate_difficulty(type, objects):
        strain_step = 400
        prev = None
        max_strain = 0
        decay_weight = 0.9
        highest_strains = []
        interval_end = strain_step
        for obj in map.objects:
            new = d_obj(obj, radius, prev)
            objects.append(new)
            while int(new.ho.time) > interval_end:
                highest_strains.append(max_strain)
                if prev == None:
                    max_strain = 0
                else:
                    decay = math.pow(consts.decay_base[type], (interval_end - int(prev.ho.time)) / 1000.0)
                    max_strain = prev.strains[type] * decay
                interval_end += strain_step
            prev = new
            max_strain = max(new.strains[type], max_strain)
        # print max_strain
        total = 0
        difficulty = 0
        weight = 1.0
        highest_strains = sorted(highest_strains, reverse=True)
        print(len(highest_strains))
        for strain in highest_strains:
            total += strain ** balancing_values[3]
            difficulty += weight * strain
            weight *= decay_weight
        print_values = [total, difficulty]
        return difficulty, print_values


    star_scaling_factor = 0.0675
    extreme_scaling_factor = 0.5
    aim, aim_print_values = calculate_difficulty(1, objects)
    speed, speed_print_values = calculate_difficulty(0, objects)
    aim = math.sqrt(aim) * star_scaling_factor
    speed = math.sqrt(speed) * star_scaling_factor


    stars = aim + speed + abs(speed - aim) * extreme_scaling_factor

    alpha = balancing_values[0]
    beta = balancing_values[1]
    c = balancing_values[2]
    e = balancing_values[4]
    f = balancing_values[5]
    aim_total = aim_print_values[0]
    speed_total = speed_print_values[0]

    old_length_bonus = c + beta * ((2 + math.log(aim_total + speed_total, 10)) / (2 + math.log(stars, 10) / alpha) - 1)
    length_bonus = 1 + e ** (old_length_bonus-f) - e**(1-f)

    return [aim, speed, stars, map, length_bonus, 0, aim_print_values, speed_print_values, old_length_bonus]
