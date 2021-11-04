import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

'''
Flower Power - system nawadniania roślin
OPIS PROBLEMU:

Na podstawie :
- temperatury
- zapotrzebowania rośliny na wodę
- wilgotności powietrza
zwraca informację o ilośći wody ( na dobę w ml) jaką należy podlać roślinkę z pomocą Fuzzy Logic
'''
# Humidity from 0 to 100 percent
humidity = ctrl.Antecedent(np.arange(0, 100, 1), 'humidity')

# Temperature from 0 to 40 celcius degrees - we assume this plant is in the house
temperature = ctrl.Antecedent(np.arange(0, 40, 1), 'temperature')

# Average water need of a certain plant specie from 0 to 1000 ml per day
# This is AVERAGE and depends from different environment conditions
water_need = ctrl.Antecedent(np.arange(0, 1000, 1), 'water_need')

# Water amount a plant needs per day given all the conditions
water_amount = ctrl.Consequent(np.arange(0, 1000, 1), 'water_amount')

# Automatically split water_need and water_amount on 3 categories low, medium, max
water_need.automf(3)
water_amount.automf(3)

# We define rules for humidity if it's dry, optimal, humid
humidity['dry'] = fuzz.trimf(humidity.universe, [0, 0, 33])
humidity['optimal'] = fuzz.trimf(humidity.universe, [0, 33, 66])
humidity['humid'] = fuzz.trimf(humidity.universe, [33, 66, 100])

# Temperature has more levels as it matters more for plant
temperature['freezing'] = fuzz.trimf(temperature.universe, [0, 0, 5])
temperature['cold'] = fuzz.trimf(temperature.universe, [0, 5, 15])
temperature['optimal'] = fuzz.trimf(temperature.universe, [5, 15, 23])
temperature['warm'] = fuzz.trimf(temperature.universe, [15, 23, 33])
temperature['hot'] = fuzz.trimf(temperature.universe, [23, 33, 40])

# We define set of rules
rule1 = ctrl.Rule(humidity['dry'] | water_need['poor'], water_amount['average'])
rule2 = ctrl.Rule(water_need['average'], water_amount['average'])
rule3 = ctrl.Rule(temperature['warm'] | water_need['good'], water_amount['good'])
rule4 = ctrl.Rule(humidity['dry'] | temperature['hot'], water_amount['good'])
rule5 = ctrl.Rule(water_need['good'] | temperature['optimal'] | humidity['humid'], water_amount['average'])

water_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])

water = ctrl.ControlSystemSimulation(water_ctrl)

water.input['humidity'] = 77
water.input['temperature'] = 23
water.input['water_need'] = 450

water.compute()

print(water.output['water_amount'])
water_amount.view(sim=water)

plt.show()