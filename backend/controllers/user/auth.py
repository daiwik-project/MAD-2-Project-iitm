from models.model import User, db

def register_user(id, username, email, hashed_password):
    new_user = User(uuid=id, username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return True

def user_password(identifier):
    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    if user:
        return user.password  # Return the hashed password
    return None  # User does not exist

def store_the_token(user_id, token):
    user = User.query.filter_by(uuid = user_id).first()
    if user:
        user.access_token = token
        db.session.commit()
        return True
    return False


def check_token_in_user(token):
    user = User.query.filter_by(access_token = token).first()
    if user:
        return user.uuid
    return None
