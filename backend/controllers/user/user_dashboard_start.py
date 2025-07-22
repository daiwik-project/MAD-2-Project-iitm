from models.model import  Level, Subject, Chapter, Quiz, Question, db


def use_dash_level_view():
    level_info = Level.query.with_entities(Level.name, Level.description, Level.uuid).all()

    result = []

    for level in level_info:
        level_data = [level.name, level.description, level.uuid]
        result.append(level_data)
    return result

def use_dash_subject_view(level_id_list):
    for level_id in level_id_list:
        subject = Subject.query.filter_by(level_uuid=level_id).all()
        result = []
        for sub in subject:
            subject_data = [sub.uuid, sub.name, sub.description]
            result.append(subject_data)