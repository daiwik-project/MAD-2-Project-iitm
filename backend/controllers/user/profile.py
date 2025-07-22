from models.model import User, Level, Subject, Chapter, Quiz, Question
import json
from database import db


def user_prof(user_id):
   user = User.query.filter_by(uuid=user_id).first()
   profile_info = {}

   profile_info['user_id'] = user.uuid
   profile_info['username'] = user.username
   profile_info['email'] = user.email
   profile_info['joined_on'] = user.created_at.strftime('%Y-%m-%d ')
   user_level = []
   user_level_json = json.loads(user.user_level)
   for i in user_level_json:
      lev = Level.query.filter_by(uuid=i).first()
      user_level.append([lev.uuid, lev.name])
   profile_info['user_level'] = user_level
   user_selected_subject = []
   user_selected_subject_json = json.loads(user.user_selected_subject)
   for i in user_selected_subject_json:
      sub = Subject.query.filter_by(uuid=i).first()
      user_selected_subject.append([sub.uuid, sub.name])
   profile_info['user_selected_subject'] = user_selected_subject
   
   print(profile_info)
    
   return profile_info


def update_user_profile(userid, username,email, password):
   user = User.query.filter_by(uuid=userid).first()
   user.username = username
   user.email = email
   user.password = password
   db.session.commit()
   return True

def delete_user(user_id):
   user = User.query.filter_by(uuid=user_id).first()
   db.session.delete(user)
   db.session.commit()
   return True