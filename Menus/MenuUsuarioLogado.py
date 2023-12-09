import json
from Servicos.ConfereLoginSenha import ConfereLoginSenha
from Redis.RedisFavoritos import RedisFavoritos
from Redis.RedisCompras import RedisCompras
from MongoDB.Crud.CrudProduto import CrudProduto
from Servicos.SelecionadorIds import SelecionadorIds
from Redis.RedisConexao import RedisConexao


class MenuUsuarioLogado:


    validador = ConfereLoginSenha()
    redisFavoritos = RedisFavoritos()
    redisCompras = RedisCompras()
    redisConexao = RedisConexao()
    crudProduto = CrudProduto()
    selecionadorIds = SelecionadorIds()


    def menu(self, id, login, senha):
        key = 0
        self.redisFavoritos.pegaFavoritosMongo(login, id)
        self.redisCompras.pegaComprasMongo(login, id)
        while key != "V":
            print("Menu de Usuário Logado")
            print("1 - Adicionar Favoritos")
            print("2 - Deletar Favoritos")
            print("3 - Comprar Produto")
            print("4 - Ver Favoritos")
            print("5 - Ver Compras")
            print("6 - Deslogar")
            key = input("Escolha uma das opções: ")
            if key == "1" and self.validador.validacaoLogin(login, senha):
                produto = self.selecionadorIds.selecionar("Produto", "inserir um produto nos favoritos desse usuário")
                if produto == "C":
                    print("\nOperação cancelada\n")
                elif produto == "Não há produtos cadastrado":
                    print(produto)
                else:
                    produto = self.crudProduto.Find(produto)
                    produto = "{" + f'"produto_id": "{produto["_id"]}", "produto_nome": "{produto["produto_nome"]}", "produto_oferta": {produto["produto_oferta"]}, "produto_preco": {produto["produto_preco"]}' + "}"
                    self.redisFavoritos.adicionarFavorito(produto, login)

            elif key == "2" and self.validador.validacaoLogin(login, senha):
                listaFavoritos = self.redisFavoritos.selecionarListaFavorito(login)
                self.redisFavoritos.apagarFavorito(login, listaFavoritos)

            elif key == "3" and self.validador.validacaoLogin(login, senha):
                produto = self.selecionadorIds.selecionar("Produto", "inserir um produto nas compras desse usuário")
                if produto == "C":
                    print("\nOperação cancelada\n")
                elif produto == "Não há produtos cadastrado":
                    print(produto)
                else:
                    produto = self.crudProduto.Find(produto)
                    produto = "{" + f'"produto_id": "{produto["_id"]}", "produto_nome": "{produto["produto_nome"]}", "produto_oferta": {produto["produto_oferta"]}, "produto_preco": {produto["produto_preco"]}' + "}"
                    self.redisCompras.adicionaCompra(produto, login)
            
            elif key == "4" and self.validador.validacaoLogin(login, senha):
                lista = self.redisConexao.conexao.lrange(f"favoritos{login}", 0, -1)
                for produto in lista:
                    print(produto)

            elif key == "5" and self.validador.validacaoLogin(login, senha):
                print(self.redisConexao.conexao.lrange(f"compras{login}", 0, -1))


            elif key == "6" and self.validador.validacaoLogin(login, senha):
                self.redisCompras.reinsereComprasMongo(login, id)
                self.redisFavoritos.reinsereFavoritosMongo(login, id)
                self.redisConexao.deslogar(login)
                break
            else:
                self.redisCompras.reinsereComprasMongo(login, id)
                self.redisFavoritos.reinsereFavoritosMongo(login, id)
                self.redisConexao.deslogar(login)
                break
