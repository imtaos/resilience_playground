from flask import Blueprint, jsonify, request
from ..models.blog import Blog
from .. import db
from tenacity import retry, stop_after_attempt, wait_exponential

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/blogs', methods=['GET'])
def get_blogs():
    blogs = Blog.query.all()
    return jsonify([blog.to_dict() for blog in blogs])

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=8),
)
@blog_bp.route('/blogs/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return jsonify(blog.to_dict())

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=8),
)
@blog_bp.route('/blogs', methods=['POST'])
def create_blog():
    data = request.get_json()
    blog = Blog(
        title=data['title'],
        content=data['content'],
        author=data['author'],
        status=data.get('status', 'draft')
    )
    db.session.add(blog)
    db.session.commit()
    return jsonify(blog.to_dict()), 201

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=8),
)
@blog_bp.route('/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    data = request.get_json()
    
    blog.title = data.get('title', blog.title)
    blog.content = data.get('content', blog.content)
    blog.author = data.get('author', blog.author)
    blog.status = data.get('status', blog.status)
    
    db.session.commit()
    return jsonify(blog.to_dict())

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=8),
)
@blog_bp.route('/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return '', 204
