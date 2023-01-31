from exts import db



class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    img = db.Column(db.String(255), nullable=False)

    def __init__(self, title, subtitle, date, img):
        self.title = title
        self.subtitle = subtitle
        self.date = date
        self.img = img

    def __repr__(self):
        return f"<Post {self.title} >"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, title, subtitle, date, img):
        self.title = title
        self.subtitle = subtitle
        self.date = date
        self.img= img
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True )
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, username, password):
        self.username = username
        self.email = email
        self.password = password
    
    def __repr__(self):
        return f"<User {self.username} >"

    def save(self):
        db.session.add(self)
        db.session.commit()