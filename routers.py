from fastapi import APIRouter
from routes.login import login_router
from routes.trades import trades_router
from routes.users import users_router
from routes.workers import workers_router
from routes.suppliers import suppliers_router
from routes.materials_categories import materials_categories_router
from routes.materials import materials_router
from routes.supplies import supplies_router
from routes.warehouse_materials import warehouse_materials_router
from routes.files import files_router
from routes.customers import customers_router
from routes.products_categories import products_categories_router
from routes.products import products_router
from routes.stages import stages_router
from routes.works import works_router
from routes.cells import cells_router
from routes.taking_materials import taking_materials_router
from routes.stage_works import stage_works_router
from routes.expenses import expenses_router
from routes.incomes import incomes_router


api = APIRouter()


api.include_router(login_router)
api.include_router(users_router)
api.include_router(workers_router)
api.include_router(suppliers_router)
api.include_router(materials_categories_router)
api.include_router(materials_router)
api.include_router(supplies_router)
api.include_router(warehouse_materials_router)
api.include_router(files_router)
api.include_router(customers_router)
api.include_router(products_categories_router)
api.include_router(products_router)
api.include_router(stages_router)
api.include_router(works_router)
api.include_router(cells_router)
api.include_router(taking_materials_router)
api.include_router(trades_router)
api.include_router(stage_works_router)
api.include_router(expenses_router)
api.include_router(incomes_router)
