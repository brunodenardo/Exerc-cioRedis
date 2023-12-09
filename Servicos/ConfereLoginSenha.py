from Servicos.EscolheColecao import EscolheColecao

class ConfereLoginSenha:

    colecaoUsuario = EscolheColecao()

    def validacaoLogin(self, login, senha):
        colecao = self.colecaoUsuario.escolher("Usuário")
        usuario = colecao.find_one({"usuario_login":login})
        if(usuario is not None):
            if(usuario.get("usuario_nome") == senha):
                return usuario.get("_id")
            return 0
        return 0

