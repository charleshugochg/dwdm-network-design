from __future__ import print_function, unicode_literals
import regex
import pandas as pd

import six
import os
clear = lambda: os.system('cls')
from tabulate import tabulate
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict, Separator)

from utils import log, generate_questions

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})

class NumChannelValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end
        if not 40 <= int(document.text) <= 88:
            raise ValidationError(
                message='Number of channel must be between 40 and 88',
                cursor_position=len(document.text))

class NumberRangeValidator(Validator):
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def validate(self, document):
        # TODO: validator of number within range
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end
        if not self.min <= int(document.text) <= self.max:
            raise ValidationError(
                message='Out of range',
                cursor_position=len(document.text))  # Move cursor to end

class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

def askFiberSpec():
    df_fiber_spec = pd.DataFrame({
        'Fiber Type': ['Single Mode (SM)'],
        'Attenuation (dB/km)': [0.275],
        'Dispersion coefficient (ps/nm-km)': [17]
    })
    log("")
    log("Fiber Specification", color="green")
    log("This table shows the general value of SM fiber specification.")
    log("")
    log(tabulate(df_fiber_spec.to_numpy(), headers=df_fiber_spec.columns, tablefmt='orgtbl'), color="blue")
    log("")
    answers = prompt(generate_questions(df_fiber_spec, [1,2]), style=style)
    print(answers)

def main():
    clear()
    log("Power Budget", color="blue", figlet=True)
    log("Welcome to power budget", color="green")
    log("This program is for calculating power budget of DWDM transmission Link (Distance of 80 km to 220 km)", color="white")
    log("")
    log("In Basic DWDM long distance link, transceiver, MDU, Directionless ROADM and Degree ROADM are both on the Transmitting and Receiving Sites.", color="white")
    log("B is a booster amplifier.")
    log("P is a pree amplifier.")
    log("")
    log("There is an add/drop station between the transmission link. The length of the L2 should be equal or longer than the L1.")
    log("")
    log("Before the calculation starts, please choose and input the specification value of the devices.")
    askFiberSpec()

if __name__ == "__main__":
    main()