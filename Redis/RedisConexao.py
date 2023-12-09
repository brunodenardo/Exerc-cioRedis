import redis
from Servicos.ConfereLoginSenha import ConfereLoginSenha


class RedisConexao:

    validador = ConfereLoginSenha()

    def __init__(self):
        self.conexao = redis.Redis(
            host='redis-15706.c308.sa-east-1-1.ec2.redns.redis-cloud.com',
            port=15706,
            password='4lzFEzLchhq0mcTOfikEIpwxdH6lsDYS')

    def login(self, login, senha):
        validade = self.validador.validacaoLogin(login, senha)
        if(validade):
            self.conexao.set(login, senha, ex=120)
            return validade
        return validade

    def deslogar(self, login):
        self.conexao.delete(login)
        self.conexao.delete(f"compras{login}")
        self.conexao.delete(f"favoritos{login}")


        