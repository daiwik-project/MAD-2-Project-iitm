
from models.model import User, db
from sqlalchemy import or_

def find_usr(searchpattern):
    print(searchpattern)
    match_usr = User.query.filter((User.username == searchpattern)| (User.email == searchpattern) | (User.uuid == searchpattern)).all()
    user_list = []
    for user in match_usr:
        user_list.append({
            "uuid": user.uuid,
            "username": user.username,
            "email": user.email,
            "block_status": user.is_active,
        })
    print(user_list)
    return user_list


def block_user(user_id):
    user = User.query.filter_by(uuid=user_id).first()
    if user:
        user.is_active = False
        db.session.commit()


def unblock_user(user_id):
    user = User.query.filter_by(uuid=user_id).first()
    if user:
        user.is_active = True
        db.session.commit()