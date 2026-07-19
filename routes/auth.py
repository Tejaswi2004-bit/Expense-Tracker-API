from fastapi import APIRouter, HTTPException, Depends
from schemas import LoginRequest
from schemas import User
from database import user_collection
from utils import hash_password, verify_password
from auth import create_access_token, get_current_user

router = APIRouter()



@router.post("/register")
async def register(user: User):

    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user.password)

    result = await user_collection.insert_one(user_dict)

    return {
        "message": "User Registered Successfully",
        "id": str(result.inserted_id)
    }




@router.post("/login")
async def login(
     login_data: LoginRequest
):

    user = await user_collection.find_one(
        {
            "email": login_data.email
        }
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        login_data.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    token = create_access_token(
        {
            "sub": user["email"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }



@router.get("/me")
async def get_me(
    current_user=Depends(get_current_user)
):

    current_user["_id"] = str(
        current_user["_id"]
    )
    current_user.pop("password", None)
    return current_user