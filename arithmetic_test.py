import datetime
import os
import random
import sys
import time


class WrongAnswerError(Exception):
    pass


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


def print_test_statistic(start_time, right_answers, total_number_of_tests, expressions, time_limit, wrong_answers):
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    elapsed_time = elapsed_time if elapsed_time <= time_limit else time_limit
    headers = ('date', 'tests completed', '% of right answers', 'elapsed time (minutes)', 'exp1', 'exp2')
    elapsed_time_str = f'{int(elapsed_time // 60):02}:{int(elapsed_time % 60):02}'
    print(f'\n'
          f'{headers[0]:16} | '
          f'{headers[1]:15} | '
          f'{headers[2]:19} | '
          f'{headers[3]:22} | '
          f'{headers[4]:6} | '
          f'{headers[5]:6} | ')
    print(f'{datetime.datetime.now():%Y/%m/%d %H:%M} | '
          f'{str(right_answers) + "/" + str(total_number_of_tests):>15} | '
          f'{round(right_answers / total_number_of_tests * 100):>19} | '
          f'{elapsed_time_str:>22} | '
          f'{expressions[0]:6} | ', end='')
    try:
        print(f'{expressions[1]:6} |\n')
    except IndexError:
        print('\n')
    [print(f'{key:15}: right answer: {wrong_answers[key][0]:7}, given answer: '
           f'{wrong_answers[key][1]:7}') for key in wrong_answers]
    return statistic_log(right_answers, total_number_of_tests, elapsed_time, expressions)


def statistic_log(right_answers, total_number_of_tests, elapsed_time, expressions):
    if 'result_loggining.csv' not in os.listdir():
        with open('result_loggining.csv', 'a') as f:
            f.write('date, tests completed, % of right answers, elapsed time %m:%s, exp1, exp2\n')
    with open('result_loggining.csv', 'a') as f:
        f.write(f'{datetime.datetime.now():%Y/%m/%d %H:%M}, '
                f'{right_answers}/{total_number_of_tests}, '
                f'{round(right_answers / total_number_of_tests * 100)}, '
                f'{int(elapsed_time // 60):02}:{int(elapsed_time % 60):02}, '
                f'{expressions[0]}')
        try:
            f.write(f', {expressions[1]}\n')
        except IndexError:
            f.write(f'\n')


def main(digits_from=5, digits_to=99, total_number_of_tests=50, time_limit=300):
    total_number_of_tests = total_number_of_tests // 2 * 2
    right_answers = 0
    start_time = time.monotonic()
    expressions = []
    wrong_answers = {}
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
                right_answer = round(eval(f'{a * A} {sign} {b * B}'), 2)
                try:
                    given_answer = round(float(input()), 2)
                    if right_answer == given_answer and timer(start_time, time.monotonic(), time_limit):
                        right_answers += 1
                    elif right_answer != given_answer:
                        raise WrongAnswerError
                except ValueError:
                    given_answer = ''
                    wrong_answers[f'{expression} ({A}, {B})' ] = (right_answer, given_answer)
                    continue
                except WrongAnswerError:
                    wrong_answers[f'{expression} ({A}, {B})' ] = (right_answer, given_answer)
                    continue
            else:
                timesup()
                print_test_statistic(start_time, right_answers, total_number_of_tests,
                                     expressions, time_limit, wrong_answers)
                return None
    print_test_statistic(start_time, right_answers, total_number_of_tests,
                         expressions, time_limit, wrong_answers)


if __name__ == '__main__':
    main(digits_from=5, digits_to=99, total_number_of_tests=50, time_limit=10)
