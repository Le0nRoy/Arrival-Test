from random import randint


def get_random_float(a, b) -> float:
    return float(str(randint(a, b)) + "." + str(randint(0, 9)) + str(randint(1, 9)))
