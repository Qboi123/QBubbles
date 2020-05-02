import random
import string


class Random(random.Random):
    # noinspection PyAttributeOutsideInit
    def seed(self, a=None, version=2):
        from os import urandom as _urandom
        from hashlib import sha512 as _sha512
        if a is None:
            try:
                # Seed with enough bytes to span the 19937 bit
                # state space for the Mersenne Twister
                a = int.from_bytes(_urandom(2500), 'big')
            except NotImplementedError:
                import time
                a = int(time.time() * 256)  # use fractional seconds

        if version == 2:
            if isinstance(a, (str, bytes, bytearray)):
                if isinstance(a, str):
                    a = a.encode()
                a += _sha512(a).digest()
                a = int.from_bytes(a, 'big')

        self._current_seed = a
        super().seed(a)

    def getseed(self):
        return self._current_seed

    def randomstring(self, length, symbols=string.ascii_letters):
        s = ""
        symbols_list = list(symbols)
        for _ in range(length):
            s += self.choice(symbols_list)
        return s

    def randombytes(self, length, range_: range):
        b = b''

        if range_.start < 0:
            raise ValueError("Range start must be between 0 and 255")
        elif range_.start > 255:
            raise ValueError("Range start must be between 0 and 255")
        if range_.stop < 0:
            raise ValueError("Range stop must be between 0 and 255")
        elif range_.stop > 255:
            raise ValueError("Range stop must be between 0 and 255")
        for _ in range(length):
            rand = self.randrange(range_.start, range_.stop, range_.step)
            integer = int(rand)
            b += integer.to_bytes(1, "little")
        return b

    def randomhex(self, range_: range):
        rand = self.randrange(range_.start, range_.stop, range_.step)
        hexadecimal = hex(int(rand))
        return hexadecimal

    def randomfloat(self, min_, max_):
        rand: float = self.random()
        out = (rand * (max_ - min_)) + min_
        return out


# fast math algorithms
class FastRandom(object):
    def __init__(self, seed):
        self.seed = seed

    def randint(self):
        self.seed = (214013 * self.seed + 2531011)
        return (self.seed >> 16) & 0x7FFF


if __name__ == '__main__':
    a = Random(65535)
    print(f"Random bytes : {a.randombytes(1, range(15, 255, 16))}")
    print(f"Random hex   : {a.randomhex(range(0x0f, 0xff, 0x0010))}")
    print(f"Random string: {a.randomstring(10, string.ascii_letters)}")
    print(f"Random float : {a.randomfloat(0, 10)}")

    print(f"\nRandom Values are now the same value")
    print(f"Random bytes : {Random(1024).randombytes(1, range(15, 255, 16))}")
    print(f"Random hex   : {Random(1024).randomhex(range(0x0f, 0xff, 0x0010))}")
    print(f"Random string: {Random(1024).randomstring(10, string.ascii_letters)}")
    print(f"Random float : {Random(1024).randomfloat(0, 10)}")

    print("\nTesting Random floats")

    import tkinter as tk
    import tkinter.ttk as ttk

    root_randf = tk.Tk()
    root_randf.geometry("400x119")
    root_randf.title("Testing Random floats")

    s_randf = ttk.Style()
    s_randf.theme_use("default")

    max_seed_number_randf = 16  # Standard: 1024
    max_tries_randf = 16  # 65536  # Standard: 16

    highest_randf = -1.0

    highest_lbl_randf = tk.Label(root_randf, text=f"{highest_randf}", anchor="w", font="consolas")
    randfloat_lbl_randf = tk.Label(root_randf, text=f"", anchor="w", font="consolas")
    curr_seed_lbl_randf = tk.Label(root_randf, text=f"", anchor="w", font="consolas")
    curr_try_lbl_randf = tk.Label(root_randf, text=f"", anchor="w", font="consolas")
    progress_randf = ttk.Progressbar(root_randf, maximum=((max_seed_number_randf + 1) * (max_tries_randf + 1)), value=0)
    # empty = tk.Label(root, text=f"")
    # seed_progress = ttk.Progressbar(root, maximum=max_seed_number, value=0)
    # try_progress = ttk.Progressbar(root, maximum=max_tries, value=0)
    highest_lbl_randf.pack(fill="x")  # , expand=True)
    randfloat_lbl_randf.pack(fill="x")  # , expand=True)
    curr_seed_lbl_randf.pack(fill="x")  # , expand=True)
    curr_try_lbl_randf.pack(fill="x")  # , expand=True)
    progress_randf.pack(fill="x", pady=0)
    # empty.pack(fill="x", pady=1)
    # seed_progress.pack(fill="x", pady=1)
    # try_progress.pack(fill="x")

    i = -1
    for seed in range(0, max_seed_number_randf):
        a = Random(seed)
        curr_seed_lbl_randf.config(text=f"seed      ={seed}")
        # seed_progress.config(value=seed)
        for tries in range(0, max_tries_randf):
            _randfloat = a.randomfloat(0, 10)
            curr_try_lbl_randf.config(text=f"try       ={tries}")
            randfloat_lbl_randf.config(text=f"_randfloat={_randfloat}")
            # print(f"Seed {seed} | Try {tries} | {_randfloat}")
            if _randfloat > highest_randf:
                highest_randf = _randfloat
                highest_lbl_randf.config(text=f"highest   ={highest_randf};s={seed};t={tries}")
            i += 1
            # try_progress.config(value=tries)
            progress_randf.config(value=i)
            root_randf.update()
    root_randf.mainloop()

    print(f"Highest float value       : {highest_randf}")
    print(f"Seeds processed           : {max_seed_number_randf}")
    print(f"Tries per seed processed  : {max_tries_randf}")
    print(f"Total random floats tested: {max_tries_randf * max_seed_number_randf}")
    print("")
    print("Testing FastRandom(seed=...)")

    fast_rand_root = tk.Tk()
    fast_rand_root.geometry("400x119")
    fast_rand_root.title("Testing FastRandom(seed=...)")

    s_fr = ttk.Style()
    s_fr.theme_use("default")

    max_seed_number_fr = 512  # Standard: 1024
    max_tries_fr = 512  # 65536  # Standard: 16

    highest_fr = None

    highest_lbl_fr = tk.Label(fast_rand_root, text=f"", anchor="w", font="consolas")
    randfloat_lbl_fr = tk.Label(fast_rand_root, text=f"", anchor="w", font="consolas")
    curr_seed_lbl_fr = tk.Label(fast_rand_root, text=f"", anchor="w", font="consolas")
    curr_try_lbl_fr = tk.Label(fast_rand_root, text=f"", anchor="w", font="consolas")
    progress_fr = ttk.Progressbar(fast_rand_root, maximum=((max_seed_number_fr + 1) * (max_tries_fr + 1)), value=0)
    # empty = tk.Label(fast_rand_root, text=f"")
    # seed_progress = ttk.Progressbar(fast_rand_root, maximum=max_seed_number_fr, value=0)
    # try_progress = ttk.Progressbar(fast_rand_root, maximum=max_tries_fr, value=0)
    highest_lbl_fr.pack(fill="x")  # , expand=True)
    randfloat_lbl_fr.pack(fill="x")  # , expand=True)
    curr_seed_lbl_fr.pack(fill="x")  # , expand=True)
    curr_try_lbl_fr.pack(fill="x")  # , expand=True)
    progress_fr.pack(fill="x", pady=0)
    # empty.pack(fill="x", pady=1)
    # seed_progress.pack(fill="x", pady=1)
    # try_progress.pack(fill="x")

    i = -1
    for seed in range(0, max_seed_number_fr):
        a = FastRandom(seed)
        curr_seed_lbl_fr.config(text=f"seed      ={seed}")
        # seed_progress.config(value=seed)
        for tries in range(0, max_tries_fr):
            _randfloat_fr = a.randint()
            curr_try_lbl_fr.config(text=f"try       ={tries}")
            randfloat_lbl_fr.config(text=f"_randfloat={_randfloat_fr}")
            if highest_fr is None:
                highest_fr = _randfloat_fr
                highest_lbl_fr.config(text=f"highest   ={highest_fr};s={seed};t={tries}")
            # print(f"Seed {seed} | Try {tries} | {_randfloat_fr}")
            if _randfloat_fr > highest_fr:
                highest_fr = _randfloat_fr
                highest_lbl_fr.config(text=f"highest   ={highest_fr};s={seed};t={tries}")
            i += 1
            # try_progress.config(value=tries)
            progress_fr.config(value=i)
            fast_rand_root.update()
    fast_rand_root.mainloop()
