# login.py
def validar_login(usuario, senha):
    usuarios = {
        "adm": "adm001",
        "cliente2": "minhasenha"
    }
    return usuarios.get(usuario) == senha
