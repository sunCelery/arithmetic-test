# 2А + B , B - A, and etc 25 tasks for sum and difference, totaly 50 tasks and 5 mintues timer
# В первой шапке может быть и
# А - 2B
# и все комбинации с плюсами и минусами и одно из значений удвоенное

import csv
import datetime
import os
import random
import time

import matplotlib.pyplot as plt


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


def ftimer(tik, tok, time_limit=300):
    elapsed_time = tok-tik
    if elapsed_time < time_limit:
        return "Time's up"
    else:
        return None


def statistic_log(right_answers, total_number_of_tests, elapsed_time):
    if 'result_loggining.csv' not in os.listdir():
        with open('result_loggining.csv', 'a') as f:
            f.write('date, tests completed, % of right answers, elapsed time %m:%s\n')
    with open('result_loggining.csv', 'a') as f:
        f.write(f'{datetime.datetime.now():%Y/%m/%d %H:%M:%S}, '
                f'{right_answers}/{total_number_of_tests}, '
                f'{int(right_answers / total_number_of_tests * 100)}, '
                f'{int(elapsed_time // 60)}:{int(elapsed_time % 60)}\n')


def print_test_statistic(start_time, right_answers, total_number_of_tests):
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    print(f'\n'
          f'time elapsed: {int(elapsed_time//60)} minutes, {int(elapsed_time%60)} seconds\n'
          f'tests completed: {right_answers}/{total_number_of_tests}, {int(right_answers/total_number_of_tests*100)}%')
    return statistic_log(right_answers, total_number_of_tests, elapsed_time)


def timesup():
    print(f'\n\033[1m  Time\'s up  \033[0m')
    print_test_statistic(start_time, right_answers, total_number_of_tests)


def show_plot():
    with open('result_loggining.csv') as data:
        headers = data.readline().split(', ')  # datetime, tests completed, % of right answers, elapsed time %m:%s
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

        # add here csv reader bla bal bla


def main(digits_from=5, digits_to=99, total_number_of_tests=50, timer=300):
    total_number_of_tests = total_number_of_tests // 2 * 2
    right_answers = 0
    start_time = time.monotonic()
    for random_coef in (True, False):
        a, b, expression, sign = generate_expression(random_coef=random_coef)
        print(f'\n\033[1m  {expression}  \033[0m\n')
        for i in range(total_number_of_tests//2):
            if ftimer(start_time, time.monotonic(), timer):
                if random_coef:
                    A = random.randrange(digits_from, digits_to)
                    B = random.randrange(digits_from, digits_to)
                else:
                    A = random.randrange(digits_from, eval(str(digits_to) + '99')) / 100
                    B = random.randrange(digits_from, eval(str(digits_to) + '99')) / 100
                print(f'{A}, {B}: ', end='')
                temp = round(eval(f'{a * A} {sign} {b * B}'), 2)
                try:
                    if temp == round(float(input()), 2):
                        right_answers += 1
                    else:
                        print(f' <right answer: {temp}> ', end=' ')
                except ValueError:
                    continue
            else:
                timesup()
                return None
    print_test_statistic(start_time, right_answers, total_number_of_tests)
    show_plot()


if __name__ == '__main__':
    main(digits_from=5, digits_to=99, total_number_of_tests=2, timer=300)
