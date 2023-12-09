from Menus.MenuPrincipal import MenuPrincipal
from Redis.RedisConexao import RedisConexao
from Menus.MenuUsuarioLogado import MenuUsuarioLogado

class Login:
    
    menuPrincipal = MenuPrincipal()
    redis = RedisConexao()
    menuLogado = MenuUsuarioLogado()

    def login(self):
        key = 0
        while key != "V":
            print("Menu de login")
            print("1 - Login de usuário")
            print("2 - Entrar como administrador")
            key = input("Escolha uma das opções: ")
            if key == "1":
                login = input("Insira o seu login: ")
                senha = input("Insira sua senha: ")
                id = self.redis.login(login, senha)
                if id:
                    print("\nLogin realizado com sucesso\n")
                    self.menuLogado.menu(id, login, senha)
                else:
                    print("\nCredenciais inválidas\n")
            elif key == "2":
                self.menuPrincipal.menu()