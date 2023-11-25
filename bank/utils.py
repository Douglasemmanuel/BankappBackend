import random

def generate_account_number():
    return ''.join([str(random.randint(0,9))for _ in range(10)])


def generate_bvn_number():
    return ''.join([str(random.randint(0,11))for _ in range(12)])