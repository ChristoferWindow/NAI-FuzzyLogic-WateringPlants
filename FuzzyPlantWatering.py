import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

humidity = ctrl.Antecedent(np.arange(0, 100, 1), 'humidity')
temperature = ctrl.Antecedent(np.arange(0, 40, 1), 'temperature')
water_need = ctrl.Antecedent(np.arange(0, 1000, 1), 'water_need')
water_amount = ctrl.Consequent(np.arange(0, 1000, 1), 'water_amount')

humidity['poor'] = fuzz.trimf(water_amount.universe, [0, 0, 33])
humidity['average'] = fuzz.trimf(water_amount.universe, [0, 33, 66])
humidity['high'] = fuzz.trimf(water_amount.universe, [33, 66, 100])

temperature['freezing'] = fuzz.trimf(water_amount.universe, [0, 0, 5])
temperature['cold'] = fuzz.trimf(water_amount.universe, [0, 5, 15])
temperature['average'] = fuzz.trimf(water_amount.universe, [5, 15, 23])
temperature['warm'] = fuzz.trimf(water_amount.universe, [15, 23, 33])
temperature['hot'] = fuzz.trimf(water_amount.universe, [23, 33, 40])

water_need['low'] = fuzz.trimf(water_amount.universe, [0, 0, 333])
water_need['medium'] = fuzz.trimf(water_amount.universe, [0, 333, 666])
water_need['high'] = fuzz.trimf(water_amount.universe, [333, 666, 1000])

water_amount['low'] = fuzz.trimf(water_amount.universe, [0, 0, 333])
water_amount['medium'] = fuzz.trimf(water_amount.universe, [0, 333, 666])
water_amount['high'] = fuzz.trimf(water_amount.universe, [333, 666, 1000])

rule1 = ctrl.Rule(humidity['poor'] | water_need['low'], water_amount['medium'])
rule2 = ctrl.Rule(water_need['average'], water_amount['medium'])
rule3 = ctrl.Rule(temperature['warm'] | water_need['high'], water_amount['high'])
rule4 = ctrl.Rule(humidity['poor'] | temperature['hot'], water_amount['high'])
rule5 = ctrl.Rule(water_need['high'] | temperature['average'] | humidity['high'], water_amount['medium'])

water_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])

water = ctrl.ControlSystemSimulation(water_ctrl)

water.input['humidity'] = 77
water.input['temperature'] = 23
water.input['water_need'] = 450

water.compte()

print(water.output['water'])
water.view(sim=water)

plt.show()