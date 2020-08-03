# 2А + B , B - A, and etc 25 tasks for sum and difference, totaly 50 tasks and 5 mintues time_limit
# В первой шапке может быть и
# А - 2B
# и все комбинации с плюсами и минусами и одно из значений удвоенное

import datetime
import os
import random
import sys
import time
import threading

import matplotlib.pyplot as plt


def timer(tik, tok, time_limit=300):
    elapsed_time = tok-tik
    if elapsed_time < time_limit:
        return True
    else:
        return False


def timesup():
    print(f'\n\033[1m  Time\'s up  \033[0m')


def generate_expression(positive='random', random_coef=False):
    if not random_coef:
        a, b = 1, 1
    elif random.random() > 0.5:
        a, b = 1, 2
    else:
        a, b = 2, 1
    if positive == 'random':
        if random.random() > 0.5:
            expression = f'{a}A + {b}B'.replace('1', '')
            sign = '+'
        else:
            expression = f'{a}A - {b}B'.replace('1', '')
            sign = '-'
    elif positive == 'yes':
        expression = f'{a}A + {b}B'.replace('1', '')
        sign = '+'
    elif positive == 'no':
        expression = f'{a}A - {b}B'.replace('1', '')
        sign = '-'
    return a, b, expression, sign


def print_test_statistic(start_time, right_answers, total_number_of_tests, expressions):
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    headers = ('date', 'tests completed', '% of right answers', 'elapsed time (minutes)', 'exp1', 'exp2')
    print(f'\n'
          f'{headers[0]:16} | '
          f'{headers[1]:15} | '
          f'{headers[2]:19} | '
          f'{headers[3]:22} | '
          f'{headers[4]:7} | '
          f'{headers[5]:7} | ')
    print(f'{datetime.datetime.now():%Y/%m/%d %H:%M} | '
          f'{str(right_answers) + "/" + str(total_number_of_tests):15} | '
          f'{int(right_answers / total_number_of_tests * 100):19} | '
          f'{str(int(elapsed_time // 60)) + ":" + str(int(elapsed_time % 60)):22} | '
          f'{expressions[0]:7} | ', end='')
    try:
        print(f'{expressions[1]:7} |')
    except IndexError:
        print()
    return statistic_log(right_answers, total_number_of_tests, elapsed_time, expressions)


def statistic_log(right_answers, total_number_of_tests, elapsed_time, expressions):
    if 'result_loggining.csv' not in os.listdir():
        with open('result_loggining.csv', 'a') as f:
            f.write('date, tests completed, % of right answers, elapsed time %m:%s, exp1, exp2\n')
    with open('result_loggining.csv', 'a') as f:
        f.write(f'{datetime.datetime.now():%Y/%m/%d %H:%M}, '
                f'{right_answers}/{total_number_of_tests}, '
                f'{int(right_answers / total_number_of_tests * 100)}, '
                f'{int(elapsed_time // 60)}:{int(elapsed_time % 60)}, '
                f'{expressions[0]}')
        try:
            f.write(f', {expressions[1]}\n')
        except IndexError:
            f.write(f'\n')


def show_plot():
    with open('result_loggining.csv') as data:
        headers = data.readline().split(', ')
        date_of_test = []
        test_completed = []
        percent_of_right_answers = []
        elapsed_time = []
        for line in data.readline():
            print(line.split(', '))
            temp = line.split(', ')
            date_of_test.append(temp[0])
            test_completed.append(temp[1])
            percent_of_right_answers.append(temp[2])
            elapsed_time.append(temp[3])
        fig, axs = plt.subplots(1, 1, figsize=(9, 3), sharey=True)
        axs[0].plot(percent_of_right_answers, elapsed_time)
        fig.suptitle('Categorical Plotting')


def main(digits_from=5, digits_to=99, total_number_of_tests=50, time_limit=300):
    total_number_of_tests = total_number_of_tests // 2 * 2
    right_answers = 0
    start_time = time.monotonic()
    expressions = []
    for random_coef in (True, False):
        a, b, expression, sign = generate_expression(random_coef=random_coef)
        expressions.append(expression)
        print(f'\n\033[1m  {expression}  \033[0m\n\n')
        for i in range(total_number_of_tests//2):
            if timer(start_time, time.monotonic(), time_limit):
                if random_coef:
                    A = random.randrange(digits_from, digits_to)
                    B = random.randrange(digits_from, digits_to)
                else:
                    A = random.randrange(digits_from, eval(str(digits_to) + '99')) / 100
                    B = random.randrange(digits_from, eval(str(digits_to) + '99')) / 100
                sys.stdout.write(f'\u001b[1A'
                                 f'\u001b[2D'
                                 f'{A}, {B}:           \u001b[10D')
                sys.stdout.flush()
                temp = round(eval(f'{a * A} {sign} {b * B}'), 2)
                try:
                    if temp == round(float(input()), 2):
                        right_answers += 1
                except ValueError:
                    continue
            else:
                timesup()
                print_test_statistic(start_time, right_answers, total_number_of_tests, expressions)
                return None
    print_test_statistic(start_time, right_answers, total_number_of_tests, expressions)
    # show_plot()


if __name__ == '__main__':
    # threading.Timer(5, print('hello world')).start()
    main(digits_from=5, digits_to=99, total_number_of_tests=50, time_limit=300)
