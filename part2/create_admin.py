#!/usr/bin/python3

from app.services.facade import HBnBFacade
from app.models.user import User

facade = HBnBFacade()

admin_data = {

    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com",
    "password": "admin_password"
}

admin_user = User(**admin_data)

admin_user.is_admin = True

facade.user_repo.add(admin_user)

print("Admin user created with id:", admin_user.id)