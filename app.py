from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from prediction import predictions
from money_validation import valid


app = FastAPI()
templates = Jinja2Templates(directory=".")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": None,
            "form": {}
        }
    )


@app.post("/predict", response_class=HTMLResponse)
def predict(
    request: Request,
    Age: int = Form(...),
    Income: float = Form(...),
    LoanAmount: float = Form(...),
    LoanTerm: int = Form(...),
    Education: str = Form(...), 
    LoanPurpose: str = Form(...)
    ):
    mon = [None, None, None, None]
    df = pd.DataFrame([{
        "Age": Age,
        "Income": Income,
        "LoanAmount": LoanAmount,
        "LoanTerm": LoanTerm*12,
        "Education": Education,
        "LoanPurpose": LoanPurpose
    }])

    
    result = predictions.pred(df, 0.3)
    if result == 0:
        mon = valid.compil(df)


    df['LoanTerm'] = df['LoanTerm'].apply(lambda x:x//12)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "rate": mon[3],
            "total_payment": mon[1],
            "monthly_payment": mon[0],
            "first_payment": mon[2],
            "form": df.iloc[0].to_dict()
        }
    )
