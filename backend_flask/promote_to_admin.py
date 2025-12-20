"""
Script to promote a user to admin role
Usage: python promote_to_admin.py <email>
"""

import sys
from app import create_app
from app.models import User
from app.extensions import db

def promote_to_admin(email):
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"❌ User with email '{email}' not found")
            return False
        
        if user.role == 'admin':
            print(f"✓ User '{email}' is already an admin")
            return True
        
        user.role = 'admin'
        db.session.commit()
        print(f"✅ Successfully promoted '{email}' to admin role")
        return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python promote_to_admin.py <email>")
        sys.exit(1)
    
    email = sys.argv[1].strip().lower()
    promote_to_admin(email)
