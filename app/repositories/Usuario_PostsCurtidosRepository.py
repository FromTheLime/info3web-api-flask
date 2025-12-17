from ..config.db import db
from ..models import Usuario
from ..models import Post
from ..models.tables.usuario_posts_curtidos import usuarios_posts_curtidos

def find_liked_posts_by_user_id(usuario_id): 
    posts_curtidos = db.session.query(usuarios_posts_curtidos).filter_by(usuario_id=usuario_id).all()
    return posts_curtidos