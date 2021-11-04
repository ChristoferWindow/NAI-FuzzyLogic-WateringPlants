import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

humidity = ctrl.Antecedent(np.arange(0, 100, 1), 'humidity')
temperature = ctrl.Antecedent(np.arange(0, 40, 1), 'temperature')
water_need = ctrl.Antecedent(np.arange(0, 1000, 1), 'water_need')
water_amount = ctrl.Consequent(np.arange(0, 1000, 1), 'water_amount')

water_need.automf(3)
water_amount.automf(3)

humidity['dry'] = fuzz.trimf(humidity.universe, [0, 0, 33])
humidity['optimal'] = fuzz.trimf(humidity.universe, [0, 33, 66])
humidity['humid'] = fuzz.trimf(humidity.universe, [33, 66, 100])

temperature['freezing'] = fuzz.trimf(temperature.universe, [0, 0, 5])
temperature['cold'] = fuzz.trimf(temperature.universe, [0, 5, 15])
temperature['optimal'] = fuzz.trimf(temperature.universe, [5, 15, 23])
temperature['warm'] = fuzz.trimf(temperature.universe, [15, 23, 33])
temperature['hot'] = fuzz.trimf(temperature.universe, [23, 33, 40])

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