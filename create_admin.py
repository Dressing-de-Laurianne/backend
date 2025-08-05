### content of "create_user.py" file
from django.contrib.auth import get_user_model

# Global admin user parameters
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="admin"

# see ref. below
UserModel = get_user_model()

print(f"Creating admin user: {ADMIN_USERNAME}")
# Create the admin user if it does not exist
if not UserModel.objects.filter(username=ADMIN_USERNAME).exists():
    user=UserModel.objects.create_user(ADMIN_USERNAME, password=ADMIN_PASSWORD)
    user.is_superuser=True
    user.is_staff=True
    user.save()
    print(f"Admin user {ADMIN_USERNAME} created successfully.")
else:
    print(f"Admin user {ADMIN_USERNAME} already exists.")