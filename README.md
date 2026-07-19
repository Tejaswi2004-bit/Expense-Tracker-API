# Expense Tracker API

A secure and scalable Expense Tracker REST API built using FastAPI and MongoDB. This project allows users to register, authenticate using JWT, manage expenses, set budgets, and generate expense reports with filtering, sorting, pagination, and analytics.

## Features

- User Registration
- User Login with JWT Authentication
- Protected API Endpoints
- Add, View, Update and Delete Expenses
- Budget Management
- Expense Summary
- Category-wise Summary
- Monthly Expense Summary
- Highest Expense
- Lowest Expense
- Average Expense
- Filter Expenses by Category
- Filter Expenses by Date Range
- Filter Expenses by Amount Range
- Sorting (Ascending & Descending)
- Pagination
- MongoDB Aggregation Pipelines
- Modular Project Structure

## Technologies Used

- Python
- FastAPI
- MongoDB
- Motor (Async MongoDB Driver)
- Pydantic
- JWT Authentication
- Uvicorn
- Git & GitHub

## Project Structure

```
ExpenseTrackerAPI/
│
├── routes/
│   ├── auth.py
│   ├── expense.py
│   ├── budget.py
│   └── reports.py
│
├── auth.py
├── database.py
├── schemas.py
├── utils.py
├── main.py
├── requirements.txt
└── README.md
```

## API Endpoints

### Authentication

- POST /register
- POST /login
- GET /me

### Expenses

- POST /expenses
- GET /expenses
- GET /expense/{expense_id}
- PUT /expense/{expense_id}
- DELETE /expense/{expense_id}

### Reports

- GET /expenses/summary
- GET /expenses/category-summary
- GET /expenses/monthly-summary
- GET /expenses/highest
- GET /expenses/lowest
- GET /expenses/average

### Budget

- Create Budget
- View Budget
- Update Budget
- Delete Budget

## How to Run

1. Clone the repository

```
git clone https://github.com/Tejaswi2004-bit/Expense-Tracker-API.git
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Start the server

```
uvicorn main:app --reload
```

4. Open Swagger UI

```
http://127.0.0.1:8000/docs
```

## Future Improvements

- Expense Charts & Graphs
- Email Notifications
- Export Reports to PDF/Excel
- Frontend using HTML, CSS and JavaScript
- Docker Deployment

## Author

**Tejaswi**