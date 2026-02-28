from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from prediction import predictions


app = FastAPI()
templates = Jinja2Templates(directory=".")



FEATURES = [
    "Age",
    "Income",
    "LoanAmount",
    "NumCreditLines",
    "InterestRate"
]


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
    Education: str = Form(...), 
    LoanPurpose: str = Form(...)
    ):
    df = pd.DataFrame([{
        "Age": Age,
        "Income": Income,
        "LoanAmount": LoanAmount,
        "Education": Education,
        "LoanPurpose": LoanPurpose
    }])

    
    result = predictions.pred(df)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "form": df.iloc[0].to_dict()
        }
    )

