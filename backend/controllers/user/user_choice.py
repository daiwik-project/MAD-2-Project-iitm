"""This module handles user choices and updates their level in the database."""


import json
from models.model import Level, Subject, User
from database import db



def user_selected_level(user_id, user_level):
    user = User.query.filter_by(uuid=user_id).first()
    user.user_level = json.dumps(user_level)
    db.session.commit()
    return user.user_level



def init_sub_list_of_user_sel_level(user_lev):
    result = {}

    for level in user_lev:
        level_entry = Level.query.filter_by(uuid = level).first()
        level_name = level_entry.name

        sub_entries = Subject.query.filter_by(level_uuid=level).all()
        if sub_entries:
            subject_sets = []
            for sub in sub_entries:
                subject_sets.append([sub.uuid, sub.name, sub.description])
            result[level_name] = subject_sets
        else:
            result[level_name] = []
    return result


def user_selected_sub(user_id, user_level):
    user = User.query.filter_by(uuid=user_id).first()

    user.user_selected_subject= json.dumps(user_level)

    db.session.commit()
    return user.user_selected_subject
