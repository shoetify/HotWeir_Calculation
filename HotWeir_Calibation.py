import yaml
import re
import os
import numpy as np
import matplotlib.pyplot as plt


def get_mean_value_from_a_file(file_number):
    file_name = file_number + '.txt'
    # Check if the file exists and read the file
    if os.path.isfile(file_name):
        print(f"Reading '{file_name}' ...")

        # Read the file
        try:
            with open(file_name, 'r') as file:
                content = file.read()
                lines = content.split('\n')
                sum = 0.0
                count = 0
                for line in lines:
                    if line:
                        sum += float(line)
                        count += 1
                return (sum / count)
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
    else:
        print(f"Error: The file '{file_name}' does not exist.")
        exit()


# This Function is used for extract all the number from the config file.
def extract_numbers_from_string(string):
    # This regex matches integers, decimals, and negative numbers
    pattern = r'-?\d+\.?\d*'
    numbers = re.findall(pattern, string)
    # Convert the list of strings to a list of floats
    return [float(num) for num in numbers]


# This Function is used for extract the calibration file.
def extract_range_from_string(string):
    # This regex matches the start and end of the range
    pattern = r'(\d+)-(\d+)'
    match = re.match(pattern, string)

    if match:
        start_str = match.group(1)
        end_str = match.group(2)

        # Ensure both start and end have the same length
        if len(start_str) != len(end_str):
            raise ValueError("Start and end numbers must have the same length")

        start_num = int(start_str)
        end_num = int(end_str)

        # Generate a list of strings from start_num to end_num with leading zeros
        return [str(num).zfill(len(start_str)) for num in range(start_num, end_num + 1)]
    else:
        raise ValueError("The input string does not match the expected pattern")


# Load the YAML configuration file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Get Real Wind Speed from Config file
Corresponding_windSpeed = config['Polyfit_Parameter']['Corresponding_windSpeed']
WindSpeed_relationship = config['Polyfit_Parameter']['WindSpeed_relationship']
relationship_a, relationship_b = extract_numbers_from_string(WindSpeed_relationship)
real_windSpeed_Hz = extract_numbers_from_string(Corresponding_windSpeed)
real_windSpeed = []
for windSpeed in real_windSpeed_Hz:
    if windSpeed == 0.0:
        real_windSpeed.append(0.0)
    else:
        real_windSpeed.append(relationship_a * windSpeed + relationship_b)

# Get the mean electric signal for each file.
file_numbers = extract_range_from_string(config['Calibration_File']['file_number'])
signal_mean = []
for file_number in file_numbers:
    signal_mean.append(get_mean_value_from_a_file(file_number))

# PolyFit the electric signal to real wind speed.
Polyfit_degree = int(config['Polyfit_Parameter']['Polyfit_degree'])
x = np.array(signal_mean)
y = np.array(real_windSpeed)
coefficients = np.polyfit(x, y, Polyfit_degree)

# Plot the raw data and polyfit function
polynomial = np.poly1d(coefficients)
y_fit = polynomial(x)

with open("CaliFile.txt", "w") as cali_file:
    cali_file.write(coefficients)
    print('Successfully write down CaliFile')

plt.scatter(x, y, color='red', label='Points')
plt.plot(x, y_fit, label='Curves')
plt.legend()
plt.show()
