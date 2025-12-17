from flask import request, Blueprint
from ..services import PostService
from flask_jwt_extended import jwt_required

postBP = Blueprint("post", __name__, url_prefix="/post")

@postBP.route("/listar", methods=["GET"])
@jwt_required()
def listar_posts():
    return PostService.listar_posts()

@postBP.route("/listar_por_autor_id/<int:id>", methods=["GET"])
@jwt_required()
def listar_posts_por_autor(id):
    return PostService.listar_posts_por_autor(id)

@postBP.route("/listar_por_hashtag/<string:hashtag>", methods=["GET"])
def listar_por_hashtag(hashtag):
    return PostService.listar_por_hashtag(hashtag)

@postBP.route("/criar", methods=["POST"])
@jwt_required()
def criar_post():
    data = request.form
    files = request.files.getlist("imagens")
    return PostService.criar_post(data, files)

@postBP.route("/imagem/<int:id>")
def imagem(id):
    return PostService.buscar_id_imagem(id)
    

@postBP.route("/deletar/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_post(id):
    return PostService.deletar_post(id)

@postBP.route("/editar/<int:id>", methods=["PATCH"])
@jwt_required()
def editar_post(id):
    return PostService.editar_post(id, request.get_json())

@postBP.route("/avaliar/<int:post_id>/<int:user_id>", methods=["PATCH"])
@jwt_required()
def avaliar_post(post_id, user_id):
    return PostService.avaliar_post(post_id, user_id)

