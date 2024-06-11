import re
import os
import openpyxl

class HotWeir_Util:

    @staticmethod
    def write_to_excel(headers, datas, file_name):

        """
        This function use to write data into excel file.

        :param:
            headers: list, the list of the header.
            datas: list, the list of data (length of headers should equal to rows of datas)
            file_name: String, the output excel file name.
        :return: NAN
        """

        wb = openpyxl.Workbook()
        ws = wb.active

        ws.append(headers)
        for data in datas:
            ws.append(data)

        wb.save(file_name)
        print(f"Data has been written to {file_name}")

    @staticmethod
    def get_lists_file(file_number):

        """
        This function get all the electric signal with a given file name and return the list of the signals.

        :param string: Just the file name you want to get the value(e.g., "10017").
        :return: A list of float number of this file.
        """

        file_name = file_number + '.txt'
        # Check if the file exists and read the file
        if os.path.isfile(file_name):
            print(f"Reading '{file_name}' ...")

            # Read the file
            try:
                with open(file_name, 'r') as file:
                    content = file.read()
                    lines = content.split('\n')
                    list = []
                    for line in lines:
                        if line:
                            list.append(float(line))
                    return (list)
            except Exception as e:
                print(f"An error occurred while reading the file: {e}")
        else:
            print(f"Error: The file '{file_name}' does not exist.")
            exit()

    @staticmethod
    def extract_range_from_string(string):

        """
        This function takes a string representing a range of numbers and returns a list of strings
        representing the numbers in the range.

        :param string: A string representing a range of numbers (e.g., "10017-10023").
        :return: A list of strings representing the numbers in the range.
        """

        pattern = r'(\d+)-(\d+)'
        match = re.match(pattern, string)

        if match:
            start_str = match.group(1)
            end_str = match.group(2)

            if len(start_str) != len(end_str):
                raise ValueError("Start and end numbers must have the same length")

            start_num = int(start_str)
            end_num = int(end_str)

            return [str(num).zfill(len(start_str)) for num in range(start_num, end_num + 1)]
        else:
            raise ValueError("The input string does not match the expected pattern")

    @staticmethod
    def extract_numbers_from_string(string):

        """
        This function recognize all the number in the string and return a list of number.

        :param string: A string with numbers (e.g., "y=0.1726x-0.06956").
        :return: A list of float number representing the numbers in the string.
        """

        pattern = r'-?\d+\.?\d*'
        numbers = re.findall(pattern, string)
        return [float(num) for num in numbers]


# Example usage
if __name__ == "__main__":
    util = HotWeir_Util()

    # Test extract_range_from_string
    range_string = "0014-0016"
    print("Range:", util.extract_range_from_string(range_string))

    # Test extract_numbers_from_string
    number_string = "0 10 -15.5 20.2 25.75 -30"
    print("Numbers:", util.extract_numbers_from_string(number_string))