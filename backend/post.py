from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from models import Post
from flask import request


post_ns = Namespace('post', description="A namespace for Posts")


# Schema
post_model = post_ns.model(
    "Post",
    {
        "id": fields.Integer(),
        "title": fields.String(),
        "subtitle": fields.String(),
        "date": fields.String(),
        "img": fields.String()
    }
)




@post_ns.route('/posts')
class PostResources(Resource):
    @post_ns.marshal_list_with(post_model)
    def get(self):
        posts = Post.query.all()

        return posts

    @post_ns.marshal_with(post_model)
    @post_ns.expect(post_model)
    @jwt_required()
    def post(self):
       title = request.json['title']
       subtitle = request.json['subtitle']
       date = request.json['date']
       img = request.json['img']
       new_post = Post(title=title, subtitle=subtitle, date=date, img=img)
       new_post.save()
       return new_post, 201


@post_ns.route('/posts/<int:id>')
class PostResources(Resource):
    @post_ns.marshal_with(post_model)
    def get(self, id):
        posts = Post.query.get_or_404(id)

        return posts

    @post_ns.marshal_with(post_model)
    @jwt_required
    def put(self, id):
        update_post = Post.query.get_or_404(id)
        title = request.json['title']
        subtitle = request.json['subtitle']
        date = request.json['date']
        img = request.json['img']

        update_post.update(title, subtitle, date, img)

        return update_post
    
    @post_ns.marshal_with(post_model)
    @jwt_required()
    def delete(self, id):
        delete_post = Post.query.get_or_404(id)

        delete_post.delete()

        return delete_post