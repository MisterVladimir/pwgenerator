import subprocess
import numpy as np
import argparse
import pyperclip


class PWGenerator(object):
    lowercase = list('abcdefghijklmnopqrstuvwxyz')

    def __init__(self, length, special=1, numbers=1):
        assert (special + numbers < length - 1), \
            ("Cannot use {} special character(s) and ".format(special) +
             "{} numbers when the password is ".format(numbers) +
             "{} units long.".format(length))

        self.length = length
        self.special = special
        self.numbers = numbers

    def generate(self):
        result = np.random.choice(self.lowercase, self.length)
        remaining_indices = list(range(self.length))
        # number of uppercase letters
        n_uppercase = (self.length - self.numbers - self.special) // 2
        uppercase_indices = np.random.choice(remaining_indices, n_uppercase,
                                             replace=False)
        # remove indices marked to become uppercase letters
        for i, j in enumerate(uppercase_indices):
            del remaining_indices[j - i]

        numbers_indices = np.random.choice(remaining_indices, self.numbers,
                                           replace=False)
        # remove any indices reserved for integers
        remaining_indices = list(filter(lambda x: x not in numbers_indices,
                                        remaining_indices))

        special_indices = np.random.choice(remaining_indices, self.special,
                                           replace=False)

        # set the value of the resulting password
        result[uppercase_indices] = list(''.join(
            result[uppercase_indices]).upper())
        result[numbers_indices] = np.random.randint(
                                            0, 10, self.numbers).astype('S1')
        result[special_indices] = np.random.choice(list('!@#$%^&*'),
                                                   self.special)
        return ''.join(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--special", type=int, default=1,
                        help="number of special characters (!@#$%^&*) to"
                        "include.")
    parser.add_argument("-n", "--numbers", type=int, default=1,
                        help="number of integers to include.")
    parser.add_argument("-l", "--length", type=int, default=16,
                        help="password length")
    args = parser.parse_args()
    length = args.length
    numbers = args.numbers
    special = args.special
    gen = PWGenerator(length, special, numbers)
    result = gen.generate()
    pyperclip.copy(result)

    # old method of copying to clipboard; only works on Windows
    # import locale
    # encoding = locale.getpreferredencoding()
    # subprocess.run(['clip.exe'], input=result.encode(encoding), check=True)

    print("{} has been copied to the clipboard.".format(result))
