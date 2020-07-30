# 2А + B , B - A, and etc 25 tasks for sum and difference, totaly 50 tasks and 50 mintues timer
# В первой шапке может быть и
# А - 2B
# и все комбинации с плюсами и минусами и одно из значений удвоенное

import random
import time


def generate_expression(positive=True):
    if random.random() > 0.5:
        a, b = 1, 2
    else:
        a, b = 2, 1
    if positive:
        expression = f'{a}A + {b}B'.replace('1', '')
        sign = '+'
    else:
        expression = f'{a}A - {b}B'.replace('1', '')
        sign = '-'
    return a, b, expression, sign


def main(digits_from=10, digits_to=99, total_number_of_tests=50):
    total_number_of_tests = total_number_of_tests // 2 * 2
    right_answers = 0
    start_time = time.monotonic()

    for positiveness in (True, False):
        a, b, expression, sign = generate_expression(positiveness)
        print(f'\n\033[1m  {expression}  \033[0m\n')
        for i in range(total_number_of_tests//2):
            A, B = random.randrange(digits_from, digits_to), random.randrange(digits_from, digits_to)
            print(f'{A}, {B}: ', end='')
            try:
                if eval(f'{a*A} {sign} {b*B}') == int(input()):
                    right_answers += 1
            except ValueError:
                continue

    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    print(f'\n'
          f'time elapsed: {int(elapsed_time//60)} minutes, {int(elapsed_time%60)} seconds\n'
          f'tests completed: {right_answers}/{total_number_of_tests}, {right_answers/total_number_of_tests*100}%')


if __name__ == '__main__':
    main(10, 99, 5)
