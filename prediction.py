import joblib
from threading import Lock
from lightgbm import LGBMClassifier
import pandas as pd


class Predictions:
    def __init__(self):
        self.lock = Lock()

    def pred(self, data, flag):
        model = joblib.load("model.pkl")
        LoanTerm = data['LoanTerm'].iloc[0]

        data = data.drop('LoanTerm', axis = 1)

        education_mapping = {
            "Высшее образование (бакалавр)": 0,
            "Высшее образование (магистр)": 1,
            "Полное среднее образование": 2,
            "Учёная степень": 3
        }
        data['Education'] = data["Education"].map(education_mapping)
        data['LoanPurpose_Auto'] = False
        data['LoanPurpose_Business'] = False
        data['LoanPurpose_Education'] = False
        data['LoanPurpose_Home'] = False

        if data['LoanPurpose'].iloc[0] == 'Автомобиль': data['LoanPurpose_Auto'] = True
        elif data['LoanPurpose'].iloc[0] == 'Бизнес': data['LoanPurpose_Business'] = True 
        elif data['LoanPurpose'].iloc[0] == 'Образование': data['LoanPurpose_Education'] = True 
        elif data['LoanPurpose'].iloc[0] == 'Недвижимость': data['LoanPurpose_Home'] = True

        data = data.drop(['LoanPurpose'], axis = 1)

        data['Inc*LoanAmount'] = data['Income'] * data['LoanAmount']
        data['Inc*age'] = data['Income'] * data['Age']
        data['LoanAmount*age'] = data['LoanAmount'] * data['Age']


        age = data['Age'].iloc[0]
        income = data['Income'].iloc[0]
        loan = data['LoanAmount'].iloc[0]
        if (
            18 <= age <= 100 and
            income >= 20000 and
            500000 <= loan <= 25000000 and
            12 <= LoanTerm <= 480
        ):
            return int(model.predict_proba(data)[0][1] >= flag)
        else:
            return -1


predictions = Predictions()
