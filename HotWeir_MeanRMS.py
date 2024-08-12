import numpy as np

from HotWeir_Util import HotWeir_Util
import yaml

try:
    # Load the "config.yaml" for WindSpeed file name
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        WindSpeed_files = HotWeir_Util.extract_range_from_string(config['Files_number']['WindSpeed_file'])

    # Load the "Calibration_result.yaml" for calibration coefficient.
    with open('Calibration_result.yaml', 'r') as file:
        config = yaml.safe_load(file)
        if not config['Calibration_Result']['isPolyfit']:
            raise ValueError("Need to Run the calibration program first!")
        Coefficients = config['Calibration_Result']['Coefficients']

    Coefficients.reverse()
    mean_value = []
    RMS_value = []
    for WindSpeed_file in WindSpeed_files:
        eSignals = HotWeir_Util.get_lists_file(WindSpeed_file)
        windSpeeds = []
        for eSignal in eSignals:
            windSpeed = 0.0
            for i in range(len(Coefficients)):
                windSpeed = windSpeed + Coefficients[i] * (eSignal ** i)
            windSpeeds.append(windSpeed)
        mean_value.append(np.mean(windSpeeds))
        RMS_value.append(np.std(windSpeeds))

    # Write the result into excel.
    headers = ['file name', 'mean value', 'RMS value']
    data = []
    for fls, mv, rms in zip(WindSpeed_files, mean_value, RMS_value):
        data.append([fls, mv, rms])

    HotWeir_Util.write_to_excel(headers,data,'output.xlsx')

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    input("Press Enter to exit...")
