from Menus.MenuPrincipal import MenuPrincipal


class Login:
    key = 0
    menuPrincipal = MenuPrincipal()


    def login(self):
        while key != "V":
            print("Menu de login")
            print("1 - Login de usuário")
            print("2 - Entrar como administrador")
            key = input("Escolha uma das opções: ")
            if key == 1:
                print("logar")
            elif key == 2:
                self.menuPrincipal.menu()