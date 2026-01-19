"""
Script to list all users in the database
"""

from app import create_app
from app.models import User

def list_users():
    app = create_app()
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print("No users found in the database")
            return
        
        print(f"\n{'='*80}")
        print(f"{'ID':<5} {'Email':<30} {'Role':<10} {'Auth Provider':<15} {'Name':<20}")
        print(f"{'='*80}")
        
        for user in users:
            print(f"{user.id:<5} {user.email:<30} {user.role:<10} {user.auth_provider:<15} {user.full_name or 'N/A':<20}")
        
        print(f"{'='*80}\n")
        print(f"Total users: {len(users)}")
        print(f"Students: {len([u for u in users if u.role == 'student'])}")
        print(f"Admins: {len([u for u in users if u.role == 'admin'])}")

if __name__ == '__main__':
    list_users()
