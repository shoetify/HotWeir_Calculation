import re


class HotWeir_Util:

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