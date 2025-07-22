from models.model import User, db

# Register
def verify_pre_user(username, email):
    user = User.query.filter_by(username=username, email=email).first()
    if user:
        return False  # User already exists
    return None  # User does not exist

# Login
def verify_login_user(identifier):
    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    print(user)
    if user:
        if user.is_active==True:
            return True  # User exists
        return False  # User is not active
    return None  # User does not exist

def user_id_function(identifier):
    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    return user.uuid  

def login_att(user_id):
    user = User.query.filter_by(uuid=user_id).first()
    if user:
        attempt = user.login_attempts
        user.login_attempts += 1
        db.session.commit()
        return attempt  # User exists
    return None  # User does not exist