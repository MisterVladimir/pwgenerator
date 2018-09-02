import copy
import subprocess
import numpy as np
import argparse
import pyperclip
import secrets
import string


class PWGenerator(object):
    def __init__(self, length, special=1, numbers=1):
        assert (special + numbers < length - 1), \
            ("Cannot use {} special character(s) and ".format(special) +
             "{} numbers when the password is ".format(numbers) +
             "{} units long.".format(length))

        self.length = length
        self.special = special
        self.numbers = numbers

    def generate(self):
        def to_string(li):
            return list(map(lambda x: str(x).upper(), li))

        def choice_no_rep(pool, n):
            assert n <= len(pool), "Almost got caught in an infinite loop."
            li = [None]*n
            pool = copy.deepcopy(pool)
            for i in range(n):
                item = secrets.choice(pool)
                del pool[pool.index(item)]
                li[i] = item
            return li

        result = np.array([secrets.choice(string.ascii_lowercase)
                           for _ in range(self.length)])
        remaining_indices = list(range(self.length))
        # number of uppercase letters
        n_uppercase = (self.length - self.numbers - self.special) // 2
        uppercase_indices = choice_no_rep(remaining_indices, n_uppercase)
        # remove indices marked to become uppercase letters
        for i, j in enumerate(uppercase_indices):
            del remaining_indices[j - i]

        numbers_indices = choice_no_rep(remaining_indices, self.numbers)
        # remove any indices reserved for integers
        remaining_indices = list(filter(lambda x: x not in numbers_indices,
                                        remaining_indices))

        special_indices = choice_no_rep(remaining_indices, self.special)

        # set the value of the resulting password
        result[uppercase_indices] = to_string(result[uppercase_indices])
        result[numbers_indices] = to_string([secrets.randbelow(10)
                                             for _ in numbers_indices])
        result[special_indices] = to_string([secrets.choice('!@#$%^&*')
                                             for _ in special_indices])
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
