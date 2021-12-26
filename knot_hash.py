from copy import deepcopy


class KnotHash:
    @classmethod
    def encrypt(cls, orig_numbers, data, rounds=1):
        ptr = 0
        skip_size = 0
        numbers = deepcopy(orig_numbers)
        n = len(numbers)
        for r in range(rounds):
            for s in data:
                cls.dump_numbers(numbers, ptr)
                stripe = list(reversed([*numbers, *numbers][ptr:ptr + s]))
                for i in range(s):
                    numbers[(ptr + i) % n] = stripe[i]
                ptr = (ptr + s + skip_size) % n
                skip_size += 1
            print(f"After round {r + 1}")
            cls.dump_numbers(numbers, ptr)
        return numbers

    @classmethod
    def dump_numbers(cls, numbers, ptr):
        print(', '.join([str(d) if ptr is None or i != ptr else f"[{d}]" for i, d in enumerate(numbers)]))