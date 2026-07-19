from fastapi import APIRouter, Depends
from database import expense_collection
from auth import get_current_user

router = APIRouter()

@router.get("/expenses/summary")
async def expense_summary(
    current_user=Depends(get_current_user)
):

    pipeline = [
        {
            "$match": {
                "user_id": current_user["_id"]
            }
        },
        {
            "$group": {
                "_id": None,
                "total_expense": {
                    "$sum": "$amount"
                }
            }
        }
    ]

    result = await expense_collection.aggregate(
        pipeline
    ).to_list(length=1)

    if not result:
        return {
            "total_expense": 0
        }

    return {
        "total_expense": result[0]["total_expense"]
    }


@router.get("/expenses/category-summary")
async def category_summary(
    current_user=Depends(get_current_user)
):

    pipeline = [
        {
            "$match": {
                "user_id": current_user["_id"]
            }
        },
        {
            "$group": {
                "_id": "$category",
                "total": {
                    "$sum": "$amount"
                }
            }
        }
    ]

    result = await expense_collection.aggregate(
        pipeline
    ).to_list(length=None)

    summary = []

    for item in result:
        summary.append(
            {
                "category": item["_id"],
                "total": item["total"]
            }
        )

    return summary

@router.get("/expenses/monthly-summary")
async def monthly_summary(
    current_user=Depends(get_current_user)
):

    pipeline = [
        {
            "$match": {
                "user_id": current_user["_id"]
            }
        },
        {
            "$group": {
                "_id": {
                    "$month": "$date"
                },
                "total": {
                    "$sum": "$amount"
                }
            }
        }
    ]

    result = await expense_collection.aggregate(
        pipeline
    ).to_list(length=None)

    summary = []

    for item in result:
        summary.append(
            {
                "month": item["_id"],
                "total": item["total"]
            }
        )

    return summary


@router.get("/expenses/highest")
async def highest_expense(
    current_user=Depends(get_current_user)
):

    pipeline = [
        {
            "$match": {
                "user_id": current_user["_id"]
            }
        },
        {
            "$sort": {
                "amount": -1
            }
        },
        {
            "$limit": 1
        }
    ]

    result = await expense_collection.aggregate(
        pipeline
    ).to_list(length=1)

    if not result:
        return {
            "message": "No expenses found"
        }

    expense = result[0]

    expense["_id"] = str(expense["_id"])
    expense["user_id"] = str(expense["user_id"])

    return expense

@router.get("/expenses/lowest")
async def lowest_expense(
    current_user=Depends(get_current_user)
):

    pipeline = [
        {
            "$match": {
                "user_id": current_user["_id"]
            }
        },
        {
            "$sort": {
                "amount": 1
            }
        },
        {
            "$limit": 1
        }
    ]

    result = await expense_collection.aggregate(
        pipeline
    ).to_list(length=1)

    if not result:
        return {
            "message": "No expenses found"
        }

    expense = result[0]

    expense["_id"] = str(expense["_id"])
    expense["user_id"] = str(expense["user_id"])

    return expense


@router.get("/expenses/average")
async def average_expense(
    current_user=Depends(get_current_user)
):

    pipeline = [
        {
            "$match": {
                "user_id": current_user["_id"]
            }
        },
        {
            "$group": {
                "_id": None,
                "average_expense": {
                    "$avg": "$amount"
                }
            }
        }
    ]

    result = await expense_collection.aggregate(
        pipeline
    ).to_list(length=1)

    if not result:
        return {
            "average_expense": 0
        }

    return {
        "average_expense": result[0]["average_expense"]
    }
