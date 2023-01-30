from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
api = Api(app, doc='/docs')


# db configure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///facebook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Migrate
migrate = Migrate(app, db)

# JWT
JWTManager(app)

# Models

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


with app.app_context():
    db.create_all()

# Schema
post_model = api.model(
    "Post",
    {
        "id": fields.Integer(),
        "title": fields.String(),
        "subtitle": fields.String(),
        "date": fields.String(),
        "img": fields.String()
    }
)


signup_model = api.model(
    "SignUp",
    {
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String()
    }
)

login_model = api.model(
    "Login",
    {
        "username": fields.String(),
        "password": fields.String()
    }
)

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Post": Post,
        "user": User
    }


@api.route('/signup')
class SignUp(Resource):

    @api.expect(signup_model)
    def post(self):
        username = request.json['username']

        db_user = User.query.filter_by(username=username).first()
        if db_user is not None:
            return jsonify({"message": f"Username with this {username} is alreadt exits"})
        email = request.json['email']
        password = generate_password_hash(request.json['password'])
        new_user = User(username=username, email=email, password=password)
        new_user.save()

        return jsonify({"message": "User Created Suceesfully"})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        username = request.json['username']
        password = request.json['password']

        db_user = User.query.filter_by(username=username).first()
        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)

            return jsonify(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            )


@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return jsonify({"message": "Hello world"})


@api.route('/posts')
class PostResources(Resource):
    @api.marshal_list_with(post_model)
    def get(self):
        posts = Post.query.all()

        return posts

    @api.marshal_with(post_model)
    @api.expect(post_model)
    @jwt_required()
    def post(self):
       title = request.json['title']
       subtitle = request.json['subtitle']
       date = request.json['date']
       img = request.json['img']
       new_post = Post(title=title, subtitle=subtitle, date=date, img=img)
       new_post.save()
       return new_post, 201


@api.route('/posts/<int:id>')
class PostResources(Resource):
    @api.marshal_with(post_model)
    def get(self, id):
        posts = Post.query.get_or_404(id)

        return posts

    @api.marshal_with(post_model)
    @jwt_required
    def put(self, id):
        update_post = Post.query.get_or_404(id)
        title = request.json['title']
        subtitle = request.json['subtitle']
        date = request.json['date']
        img = request.json['img']

        update_post.update(title, subtitle, date, img)

        return update_post
    
    @api.marshal_with(post_model)
    @jwt_required()
    def delete(self, id):
        delete_post = Post.query.get_or_404(id)

        delete_post.delete()

        return delete_post


if __name__ == "__main__":
    app.run(debug=True)
