from Servicos.EscolheColecao import EscolheColecao
import json
from Redis.RedisConexao import RedisConexao

class RedisFavoritos:

    escolheColecao = EscolheColecao()
    redis = RedisConexao()

    def __init__(self):
        self.colecao = self.escolheColecao.escolher("Favoritos")


    def pegaFavoritosMongo(self, login, id):
        usuarioFavoritos = self.colecao.find_one({"usuario_id":id})
        favoritos = usuarioFavoritos["usuario_favoritos"]
        for favorito in favoritos:
            nomeLista = f"favoritos{login}"
            favoritoInserido = json.dumps(favorito)
            self.redis.conexao.rpush(nomeLista, favoritoInserido)


    def reinsereFavoritosMongo(self, login, id):
        favoritosRedis = self.redis.conexao.lrange(f"favoritos{login}", 0, -1)
        print(f"favoritosRedis: {favoritosRedis}")
        favoritos = []
        for favorito in favoritosRedis:
            favoritos.append(json.loads(favorito))
        print(f"favoritos depois do loads: {favoritos}")
        self.colecao.update_one({"usuario_id":id}, {"$set": {"usuario_favoritos": favoritos}})
        self.redis.conexao.delete(f"favoritos{login}")


    def adicionarFavorito(self, produto, login):
        favoritos = self.redis.conexao.lrange(f"favoritos{login}", 0, -1)
        if produto not in [favorito.decode('utf-8') for favorito in favoritos]:
            self.redis.conexao.rpush(f"favoritos{login}", produto)
            print("Adicionado com Sucesso")
        else:
            print("Produto já está nos favoritos")


    def selecionarListaFavorito(self, login):
        favoritos = self.redis.conexao.lrange(f"favoritos{login}", 0, -1)
        return favoritos
    
    def apagarFavorito(self, login, favoritos):
        numero = 0
        favoritos = list(favoritos)
        print(type(favoritos))
        for favorito in favoritos:
            manipulador = favoritos[numero].decode('utf-8')
            manipulador = json.loads(manipulador)
            favoritos[numero] = manipulador
            favoritos[numero]["numero"] = numero
            
            print(favoritos[numero])
            numero += 1
        
        numero = input("Escolha número do produto que você quer apagar: ")

        if numero.isdigit() and int(numero) < len(favoritos):
            favorito = favoritos[int(numero)]
            del favorito["numero"]
            self.redis.conexao.lrem(f"favoritos{login}", 0, json.dumps(favorito))