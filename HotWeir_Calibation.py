import yaml
import numpy as np
import matplotlib.pyplot as plt
from HotWeir_Util import HotWeir_Util


# Load the YAML configuration file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Get Real Wind Speed from Config file
Corresponding_windSpeed = config['Polyfit_Parameter']['Corresponding_windSpeed']
WindSpeed_relationship = config['Polyfit_Parameter']['WindSpeed_relationship']
# Get the two coefficients in the "WindSpeed_relationship".
relationship_a, relationship_b = HotWeir_Util.extract_numbers_from_string(WindSpeed_relationship)
real_windSpeed_Hz = HotWeir_Util.extract_numbers_from_string(Corresponding_windSpeed)
real_windSpeed = []
for windSpeed in real_windSpeed_Hz:
    if windSpeed == 0.0:
        # When motor is 0hz, set the wind speed to 0m/s
        real_windSpeed.append(0.0)
    else:
        real_windSpeed.append(relationship_a * windSpeed + relationship_b)


# Get the mean electric signal for each file.
file_numbers = HotWeir_Util.extract_range_from_string(config['Files_number']['Calibration_file'])
signal_mean = []
for file_number in file_numbers:
    electric_value = HotWeir_Util.get_lists_file(file_number)
    signal_mean.append(np.mean(electric_value))


# PolyFit the electric signal to real wind speed.
Polyfit_degree = int(config['Polyfit_Parameter']['Polyfit_degree'])
x = np.array(signal_mean)
y = np.array(real_windSpeed)
coefficients = np.polyfit(x, y, Polyfit_degree)


# Write the coefficients into "Calibration_result.yaml" and set isPolyfit to "True"
coefficients_list = coefficients.tolist()
# Structure for the new YAML file
calibration_result = {
    'Calibration_Result': {
        'Coefficients': coefficients_list,
        'isPolyfit': True,
    }
}
# Write the new configuration to the YAML file
with open('Calibration_result.yaml', 'w') as file:
    yaml.safe_dump(calibration_result, file, default_flow_style=False)

print("Calibration result saved successfully")


# Plot the raw data and polyfit function
polynomial = np.poly1d(coefficients)
y_fit = polynomial(x)

plt.scatter(x, y, color='red', label='Points')
plt.plot(x, y_fit, label='Curves')
plt.legend()
plt.show()
