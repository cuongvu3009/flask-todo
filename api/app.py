from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:123456@localhost/flask-todo'
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
          return f"Event: {self.description}"
    
    def __init__(self, description):
         self.description = description

def formatEvent(event):
     return {
          "description": event.description,
          "id": event.id,
          "created_at": event.created_at
     } 

@app.route('/')
def index():
    return "Hello World!"

@app.route('/events', methods=['POST'])
def create_event():
     description = request.json['description']
     event = Event(description)
     db.session.add(event)
     db.session.commit()
     return formatEvent(event)

@app.route('/events', methods=['GET'])
def get_events():
     events = Event.query.all()
     event_list = []
     for event in events:
          event_list.append(formatEvent(event))
     return {"event_list": event_list}

@app.route('/events/<int:id>', methods=['GET'])
def get_event(id):
     event = Event.query.filter_by(id=id).first()
     return formatEvent(event)

@app.route('/events/<int:id>', methods=['DELETE'])
def delete_events(id):
     event = Event.query.filter_by(id=id).first()
     db.session.delete(event)
     db.session.commit()
     return {"message": f"Event id:{id} has been deleted successfully!"}

@app.route('/events/<int:id>', methods=['PUT'])
def update_events(id):
     event = Event.query.filter_by(id=id)
     new_description = request.json['description']
     event.update(dict(description = new_description, created_at = datetime.utcnow()))
     db.session.commit()
     return {"event": formatEvent(event.first())}

if __name__ == '__main__':
    app.run(debug=True)