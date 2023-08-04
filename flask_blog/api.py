import os
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_blog.models import Post
from flask_blog import create_app
from flask_cors import CORS

app = create_app()
api = Api(app)
CORS(app)  # Enable CORS for your app

class AllPostsResource(Resource):
    def get(self):
        posts = Post.query.all()
        data = []
        for post in posts:
            data.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author': post.author.username,
                'date_posted': post.date_posted.strftime('%Y-%m-%d %H:%M:%S')
            })
        return {'posts': data}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('content', type=str, required=True, help='Content is required')
        args = parser.parse_args()

        # Create a new post using the parsed data
        post = Post(title=args['title'], content=args['content'], author='YourDefaultAuthor')
        post.save()

        # Return the created post data in the response
        return {'id': post.id, 'title': post.title, 'content': post.content, 'author': post.author.username,
                'date_posted': post.date_posted.strftime('%Y-%m-%d %H:%M:%S')}, 201

class SinglePostResource(Resource):
    def get(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return {'error': 'Post not found'}, 404
        return {'id': post.id, 'title': post.title, 'content': post.content, 'author': post.author.username,
                'date_posted': post.date_posted.strftime('%Y-%m-%d %H:%M:%S')}

    def put(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return {'error': 'Post not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('content', type=str, required=True, help='Content is required')
        args = parser.parse_args()

        post.title = args['title']
        post.content = args['content']
        post.save()

        return {'id': post.id, 'title': post.title, 'content': post.content, 'author': post.author.username,
                'date_posted': post.date_posted.strftime('%Y-%m-%d %H:%M:%S')}

    def delete(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return {'error': 'Post not found'}, 404
        post.delete()
        return {'message': 'Post deleted successfully'}, 200

api.add_resource(AllPostsResource, '/api/posts')
api.add_resource(SinglePostResource, '/api/posts/<int:post_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))  # Use the Heroku-assigned port
