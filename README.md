# Function

This two python code is used for data processing of the hot-weir probe data, included calibration of wind speed and calculated the mean and RMS value of the rest of data after calibration.

# How to Use?
1. Put all the hot-weir probe file in the same folder with the .exe file
2. Open "config.yaml"
3. Input the calibration files' file name into [Files_number][Calibration_file].
4. Input the experiment files' file name into [Files_number][WindSpeed_file].
5. Input the [Polyfit_Parameter][Corresponding_windSpeed] in Unit(Hz). This line means the motor speed of the wind tunnel when you do the calibration. Separate with space.
6. Double check the wind speed relation is suitable for your wind tunnel or not.
7. Save and Close "config.yaml"
8. Run "HotWeir_Calibation.exe" for calibration, you will get a graph of polyfit result and a "Calibration_result.yaml", that's for running the calculation file.
9. Run "HotWeir_MeanRMS.exe" and you can get the result of mean and RMS wind speed of each file in excel.
