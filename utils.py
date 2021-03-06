import six
from time import sleep
from tabulate import tabulate
from pyfiglet import figlet_format
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict, Separator)

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

g_delay = True
def init(is_delay):
    global g_delay
    g_delay = is_delay

def log(string, color="white", font="slant", figlet=False, delay=True):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)
    # wait to read by user
    if delay and g_delay:
        sleep(len(string)*0.05)

def log_df(df, flag='tmp'):
    if flag == 'tmp': 
        log(tabulate(df, headers='keys', tablefmt='orgtbl'), color="white", delay=False)
    elif flag == 'pmt':
        log(tabulate(df, headers='keys', tablefmt='orgtbl'), color="yellow", delay=False)
    else:
        log("log_df error : unknown flag", color="red")

def generate_questions(df):
    choices = []
    for i in df.index:
        choices.append(Separator(f'== {i} =='))
        choices = choices + [{'name': f'{col}', 'value': f'{i} {col}'} for col in df.columns]

    questions = [
        {
            'type': 'checkbox',
            'name': 'checkbox',
            'message': 'Select:',
            'choices': choices
        }
    ]

    for col in df.columns:
        for i in df.index:
            questions.append({
                'type': 'input',
                'name': lambda i=i, col=col: (i, col),
                'message': f'{i} > {col}',
                # TODO: update message
                'default': f'{df.loc[i, col]}',
                'when': lambda answers, col=col, i=i: f'{i} {col}' in answers.get('checkbox')
                # TODO: update filter and validate
            })
    return questions

def update_answers(df, answers):
    for a in answers:
        if callable(a):
            i, col = a()
            df.loc[i, col] = answers[a]