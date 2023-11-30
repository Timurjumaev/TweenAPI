from datetime import date
from fastapi import APIRouter, Depends
from models.cells import Cells
from models.suppliers import Suppliers
from models.warehouse_materials import WarehouseMaterials
from utils.role_verification import role_verification
import inspect
from sqlalchemy.orm import Session
from models.customers import Customers
from models.expenses import Expenses
from models.incomes import Incomes
from schemas.users import CreateUser
from routes.login import get_current_active_user
from db import database

statistics_router = APIRouter(
    prefix="/statistics",
    tags=["Statistics operation"]
)


@statistics_router.get("/expenses")
def get_expenses(start: date = date.today(), end: date = date.today(), current_user:
                 CreateUser = Depends(get_current_active_user), db: Session = Depends(database)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    expenses = db.query(Expenses).filter(Expenses.date <= end, Expenses.date >= start).all()
    money = 0
    for expense in expenses:
        money += expense.money
    return money


@statistics_router.get("/incomes")
def get_incomes(start: date = date.today(), end: date = date.today(), current_user:
                CreateUser = Depends(get_current_active_user), db: Session = Depends(database)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    incomes = db.query(Incomes).filter(Incomes.date <= end, Incomes.date >= start).all()
    money = 0
    for income in incomes:
        money += income.money
    return money


@statistics_router.get("/customers_loans")
def get_customers_loans(current_user: CreateUser = Depends(get_current_active_user), db: Session = Depends(database)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    customers = db.query(Customers).filter(Customers.balance < 0).all()
    loan = 0
    for customer in customers:
        loan += customer.balance
    return -loan


@statistics_router.get("/warehouse_products")
def get_warehouse_products(current_user: CreateUser = Depends(get_current_active_user),
                           db: Session = Depends(database)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    cells = db.query(Cells).all()
    total_sum = 0
    for cell in cells:
        total_sum = total_sum + cell.amount * cell.price
    return total_sum


@statistics_router.get("/warehouse_materials")
def get_warehouse_materials(current_user: CreateUser = Depends(get_current_active_user),
                            db: Session = Depends(database)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    warehouse_materials = db.query(WarehouseMaterials).all()
    total_sum = 0
    for warehouse_material in warehouse_materials:
        total_sum = total_sum + warehouse_material.amount * warehouse_material.price
    return total_sum


@statistics_router.get("/suppliers_loans")
def get_suppliers_loans(current_user: CreateUser = Depends(get_current_active_user), db: Session = Depends(database)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    suppliers = db.query(Suppliers).filter(Suppliers.balance > 0).all()
    loan = 0
    for supplier in suppliers:
        loan += supplier.balance
    return loan


