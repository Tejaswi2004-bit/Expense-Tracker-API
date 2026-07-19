from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from bson import ObjectId
from datetime import datetime
from schemas import Expense
from database import expense_collection
from auth import get_current_user

router = APIRouter()

@router.post("/expenses")
async def add_expense(
    expense: Expense,
    current_user=Depends(get_current_user)
):
    expense_dict = expense.model_dump()
    expense_dict["date"] = datetime.combine(
        expense_dict["date"],
        datetime.min.time()
    )

    expense_dict["user_id"] = current_user["_id"]

    result = await expense_collection.insert_one(
        expense_dict
    )

    return {
        "message": "Expense Added Successfully",
        "expense_id": str(result.inserted_id)
    }


@router.get("/expenses")
async def get_expenses(
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    sort_by: str = "date",
    order: str = "desc",
    page: int = 1,
    limit: int = 5,
    current_user=Depends(get_current_user)
):

    query = {
        "user_id": current_user["_id"]
    }

    if category:
        query["category"] = category

    if start_date and end_date:
        query["date"] = {
        "$gte": datetime.combine(start_date, datetime.min.time()),
        "$lte": datetime.combine(end_date, datetime.max.time())
    }
    
    if min_amount is not None and max_amount is not None:
        query["amount"] = {
        "$gte": min_amount,
        "$lte": max_amount
    }

    sort_order = -1 if order == "desc" else 1

    skip = (page - 1) * limit

    expenses = await expense_collection.find(query)\
    .sort(sort_by, sort_order)\
    .skip(skip)\
    .limit(limit)\
    .to_list(length=limit)

    for expense in expenses:
        expense["_id"] = str(expense["_id"])
        expense["user_id"] = str(expense["user_id"])

    return expenses

@router.get("/expense/{expense_id}")
async def get_expense(
    expense_id: str,
    current_user=Depends(get_current_user)
):

    expense = await expense_collection.find_one(
        {
            "_id": ObjectId(expense_id),
            "user_id": current_user["_id"]
        }
    )

    if expense is None:

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    expense["_id"] = str(expense["_id"])

    expense["user_id"] = str(expense["user_id"])

    return expense

@router.put("/expense/{expense_id}")
async def update_expense(
    expense_id: str,
    expense: Expense,
    current_user=Depends(get_current_user)
):

    expense_dict = expense.model_dump()
    expense_dict["date"] = datetime.combine(
        expense_dict["date"],
        datetime.min.time()
    )

    result = await expense_collection.update_one(
        {
            "_id": ObjectId(expense_id),
            "user_id": current_user["_id"]
        },
        {
            "$set": expense_dict
        }
    )

    if result.matched_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense Updated Successfully"
    }



@router.delete("/expense/{expense_id}")
async def delete_expense(
    expense_id: str,
    current_user=Depends(get_current_user)
):

    result = await expense_collection.delete_one(
        {
            "_id": ObjectId(expense_id),
            "user_id": current_user["_id"]
        }
    )

    if result.deleted_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense Deleted Successfully"
    }
