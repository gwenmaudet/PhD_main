x_border = 0.5
y_border = 0.5
x_foot = 0.05
y_foot = 0.05
coordinates = {0: [0, 0], 1: [0, 2], 2: [2, 0], 3: [2, 2]}
x_max = 0
x_min = 0
y_max = 0
y_min = 0
for key_sensor in coordinates:
    if coordinates[key_sensor][0] > x_max:
        x_max = coordinates[key_sensor][0]
    if coordinates[key_sensor][0] < x_min:
        x_min = coordinates[key_sensor][0]
    if coordinates[key_sensor][1] > y_max:
        y_max = coordinates[key_sensor][1]
    if coordinates[key_sensor][1] < y_min:
        y_min = coordinates[key_sensor][1]

max_voltage = 2900

month_in_31 = [1, 3, 5, 7, 8, 10, 12]
