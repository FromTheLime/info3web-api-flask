from ...config.db import db

usuarios_posts_curtidos = db.Table('usuarios_posts_curtidos',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)