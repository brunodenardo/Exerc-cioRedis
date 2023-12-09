from Servicos.EscolheColecao import EscolheColecao
import json
from Redis.RedisConexao import RedisConexao

class RedisCompras:

    escolheColecao = EscolheColecao()
    redis = RedisConexao()

    def __init__(self):
        self.colecao = self.escolheColecao.escolher("Compras")


    def pegaComprasMongo(self, login, id):
        usuarioCompras = self.colecao.find_one({"usuario_id":id})
        compras = usuarioCompras["usuario_compras"]
        print(compras)
        for compra in compras: 
            print(compra)
            nomeLista = f"compras{login}"
            compraInserido = json.dumps(compra)
            self.redis.conexao.rpush(nomeLista, compraInserido)


    def reinsereComprasMongo(self, login, id):
        comprasRedis = self.redis.conexao.lrange(f"compras{login}", 0, -1)
        print(f"comprasRedis: {comprasRedis}")
        compras = []
        for compra in comprasRedis:
            compras.append(json.loads(compra))
        self.colecao.update_one({"usuario_id":id}, {"$set": {"usuario_compras": compras}})
        self.redis.conexao.delete(f"compras{login}")

    def adicionaCompra(self, produto, login):
        self.redis.conexao.rpush(f"compras{login}", produto)
        print("Adicionado com Sucesso")

        

    def selecionarListaCompras(self, login):
        return self.redis.conexao.lrange(f"compras{login}", 0, -1)