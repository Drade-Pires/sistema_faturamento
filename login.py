# login.py
def validar_login(usuario, senha):
    usuarios = {
        "cliente1": "senha123",
        "cliente2": "minhasenha"
    }
    return usuarios.get(usuario) == senha
