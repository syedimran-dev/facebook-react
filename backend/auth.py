from flask_restx import Resource, Namespace, fields
from models import User
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, request, jsonify, make_response


auth_ns = Namespace('auth', description="A namespace for our authentication")

signup_model = auth_ns.model(
    "SignUp",
    {
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String()
    }
)

login_model = auth_ns.model(
    "Login",
    {
        "username": fields.String(),
        "password": fields.String()
    }
)



@auth_ns.route('/signup')
class SignUp(Resource):

    @auth_ns.expect(signup_model)
    def post(self):
        username = request.json['username']

        db_user = User.query.filter_by(username=username).first()
        if db_user is not None:
            return jsonify({"message": f"Username with this {username} is alreadt exits"})
        email = request.json['email']
        password = generate_password_hash(request.json['password'])
        new_user = User(username=username, email=email, password=password)
        new_user.save()

        return make_response(jsonify({"message": "User Created Suceesfully"}), 201)



@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
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
        else:
            return jsonify({"message": "Incorrect Cradentials"})    




@auth_ns.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_tokken=create_access_token(identity=current_user)

        return make_response(jsonify({"access_token": new_access_tokken}), 200)

