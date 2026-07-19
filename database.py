from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_URL)

database = client["ExpenseTrackerDB"]

user_collection = database["users"]

expense_collection = database.expenses

budget_collection = database["budgets"]

