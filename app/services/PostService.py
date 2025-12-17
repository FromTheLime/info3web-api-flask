import io
from ..models import Post, Imagem
from flask import jsonify, send_file
from ..repositories import PostRepository, HashtagRepository, Usuario_PostsCurtidosRepository
from ..utils import *
from ..config.db import db

def listar_posts():
    try:
        posts_do_banco = PostRepository.list_posts()

        posts = serializar_itens(posts_do_banco)
        if not posts:
            return jsonify({"detail": "Nenhum post encontrado"}), 204
        
        return jsonify(posts), 200
    except Exception as e:
        return jsonify({"detail": f"Erro desconhecido ao listar posts: {e}"}), 500

def listar_posts_por_autor(id):
    try:
        posts_do_banco = PostRepository.find_by_autor(id)

        posts = serializar_itens(posts_do_banco)

        if not posts:
            return jsonify({"detail": "Nenhum post encontrado"}), 204
        
        return jsonify(posts), 200
    except Exception as e:
        return jsonify({"detail": f"Erro desconhecido ao listar posts: {e}"}), 500


def listar_por_hashtag(hashtag):
    try:
      posts_do_banco = PostRepository.find_by_hashtag(hashtag)

      posts = serializar_itens(posts_do_banco)
      if not posts:
          return jsonify({"detail": "Nenhum post encontrado"}), 404
      
      return jsonify(posts), 200
    except Exception as e:
      return jsonify({"detail": f"Erro desconhecido ao listar posts por hashtag: {e}"}), 500

def criar_post(data, imagens):
    try:
      if not validar_dados(data, Post.campos_obrigatorios()):
        return jsonify({"detail": "Preencha os campos obrigatórios"}), 400

      novoPost = Post(data)
      if (data.get("hashtags")):
        lidar_com_hashtags([hashtag.strip() for hashtag in data.get("hashtags").split(",")], novoPost)

      lidar_com_imagens(imagens, novoPost)

      PostRepository.save(novoPost)
      return jsonify({"detail":"Post criado com sucesso!"}), 200
    except Exception as e:
      return jsonify({"detail": f"Erro desconhecido ao criar post: {e}"}), 500
                                                                  
def deletar_post(id):
    try:
      post = PostRepository.find_by_id(id)
      usuario_logado = get_usuario_logado()

      if not post:
          return jsonify({"detail": "Nenhum post encontrado"}), 404

      if post.autor_id != usuario_logado:
          return jsonify({"detail": "Você não tem permissão para deletar o post de outra pessoa"}), 403
      
      PostRepository.delete(post)
      return jsonify({"detail": "Post deletado com sucesso"}), 200
    except Exception as e:
      return jsonify({"detail": f"Erro desconhecido ao deletar post: {e}"}), 500
 
def editar_post(id, data):
    
    try:
      post = PostRepository.find_by_id(id)
      usuario_logado = get_usuario_logado()

      if not post:
          return jsonify({"detail": "Nenhum post encontrado"}), 404
      
      if post.autor_id != usuario_logado:
          return jsonify({"detail": "Você não tem permissão para editar o post de outra pessoa"}), 403

      if not validar_dados(data, Post.campos_obrigatorios()):
          return jsonify({"detail": "Preencha os campos obrigatórios"}), 400

      editar_dados(Post.campos_editaveis(), data, post)
      if (data.get("hashtags")):
         lidar_com_hashtags(data.get("hashtags"), post)

      PostRepository.save(post)
      return jsonify({"detail": "Post atualizado com sucesso"}), 200
    except Exception as e:
      return jsonify({"detail": f"Erro desconhecido ao atualizar post: {e}"}), 500

def lidar_com_hashtags(hashtags_strings, post):
    hashtags_entidades = HashtagRepository.processar_hashtags(hashtags_strings)

    if hashtags_entidades:
        post.hashtags = hashtags_entidades

def lidar_com_imagens(imagens, post):
   imagens_do_post = []
   for imagem in imagens:
      imagem_obj = Imagem(imagem.read())
      post.imagens.append(imagem_obj)
      imagens_do_post.append(imagem_obj)

   db.session.add_all(imagens_do_post)

def buscar_id_imagem(id):
    imagem = db.session.query(Imagem).filter_by(id=id).first()
    
    return send_file(
        io.BytesIO(imagem.imagem),
        mimetype="image/jpeg"
    )

def avaliar_post(post_id, user_id):
    usuario = UsuarioRepository.find_by_id(user_id)

    post = PostRepository.find_by_id(post_id)
    posts_curtidos = Usuario_PostsCurtidosRepository.find_liked_posts_by_user_id(user_id)
    
    if (post in usuario.posts_curtidos):
      post.curtidas -= 1; 
      PostRepository.save(post)
      usuario.posts_curtidos.remove(post)
      UsuarioRepository.save(usuario)

      return("Post descurtido com sucesso!")
    
    post.curtidas += 1 
    PostRepository.save(post)

    usuario.posts_curtidos.append(post)
    UsuarioRepository.save(usuario)
    return ("Post curtido com sucesso!")
