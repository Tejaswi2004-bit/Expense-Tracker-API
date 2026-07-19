from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.expense import router as expense_router
from routes.budget import router as budget_router
from routes.reports import router as reports_router

app = FastAPI()

app = FastAPI(
    title="EXPENSE TRACKER",
    description="Expense Tracker API",
    version="0.1.0"
)


app.include_router(auth_router)
app.include_router(expense_router)
app.include_router(budget_router)
app.include_router(reports_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to Expense Tracker API"
    }
