from fastapi import APIRouter, Depends, HTTPException

from schemas import Budget
from database import budget_collection, expense_collection
from auth import get_current_user

router = APIRouter()

@router.post("/budget")
async def set_budget(
    budget: Budget,
    current_user=Depends(get_current_user)
):
    budget_dict = budget.model_dump()
    budget_dict["user_id"] = current_user["_id"]
    result = await budget_collection.insert_one(
    budget_dict
)
    return {
    "message": "Budget Saved Successfully",
    "budget_id": str(result.inserted_id)
}

@router.get("/budget")
async def get_budget(
    current_user=Depends(get_current_user)
):

    budget = await budget_collection.find_one(
        {
            "user_id": current_user["_id"]
        }
    )

    if budget is None:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    pipeline = [
        {
            "$match": {
                "user_id": current_user["_id"]
            }
        },
        {
            "$group": {
                "_id": None,
                "spent": {
                    "$sum": "$amount"
                }
            }
        }
    ]

    result = await expense_collection.aggregate(
        pipeline
    ).to_list(length=1)

    spent = 0

    if result:
        spent = result[0]["spent"]

    remaining = budget["budget"] - spent

    status = "Within Budget"

    if remaining < 0:
        status = "Budget Exceeded"

    return {
        "budget": budget["budget"],
        "spent": spent,
        "remaining": remaining,
        "status": status
    }