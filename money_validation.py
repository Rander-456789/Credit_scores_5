import pandas as pd
from threading import Lock
import random


import random

def annuity_credit(S, n, rate, purpose):

    if purpose == "Образование":
        first_payment = 0
    else:
        first_payment = S * 0.07

    S = S - first_payment

    r_year = rate / 100
    r = r_year / 12

    K = (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    A = S * K

    total = A * n + first_payment

    return [round(A,0), round(total,0), round(first_payment,0), rate]


def rate_comp(LoanPurpose):
        if LoanPurpose == 'Автомобиль': return random.randint(160, 210) / 10
        elif LoanPurpose == 'Бизнес': return random.randint(210, 330) / 10 
        elif LoanPurpose == 'Образование': return random.randint(30, 100) / 10
        elif LoanPurpose == 'Недвижимость': return random.randint(160, 180) / 10
        return random.randint(180, 300) / 10

class Valid:
    def __init__(self):
        self.lock = Lock()

    def compil(self, data):

        rate = rate_comp(data['LoanPurpose'].iloc[0])
        return annuity_credit(
                data['LoanAmount'].iloc[0],
                data['LoanTerm'].iloc[0],
                rate,
                data['LoanPurpose'].iloc[0]
            )
    

valid = Valid()