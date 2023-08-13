from __init__ import AllWhatsPy



awp = AllWhatsPy()

# awp.conexao(server_host=True, popup=False)
# awp.ctt.encontrar_usuario(21959061623)
# awp.ctt.encontrar_usuario(21959061623)
# awp.ctt.encontrar_usuario(2195906162464893)
# awp.ctt.encontrar_usuario(21959061623)
# awp.ctt.encontrar_usuario(21984273613)
# awp.ctt.encontrar_usuario(91469414144944)
# awp.ctt.encontrar_usuario(21959061623)

# # awp.ctt.encontrar_contato('Lucas Lourenço')
# # awp.ctt.encontrar_contato('Lucas Lourenço')

# mensagem = """
# Olá!
# Sou o Lucas, criador do AWP.
# """
# # awp.msg.enviar_mensagem_paragrafada(mensagem)

# # awp.msg.enviar_mensagem('lucas é lindo')
# awp.msg.enviar_mensagem(mensagem)

# for i in range(2):
#     awp.ctt.chat_abaixo()
#     awp.ctt.chat_acima()

# # awp.utilidade.arquivar_chat()


# print(awp.InferenciaAWP.contato)
# print(awp.InferenciaAWP.lista_contatos)
# print(awp.InferenciaAWP.contatosInexistentes)
# print(awp.InferenciaAWP.mensagem)
# # input()
# # awp.desconectar()

# awp.ctt.encontrar_usuario(91469414144944)
# awp.ctt.encontrar_usuario(21959061623)
# awp.msg.enviar_mensagem([texto, texto_descrip])

texto = 'Lucas e o criador do AWP, AllWhatsPy'
key = 5

with awp.criptografia.CifraDeCaesar(texto, key, 'c') as caesarC:
    texto_caesar_c = caesarC.fetch()

with awp.criptografia.CifraDeCaesar(texto_caesar_c, key, 'd') as caesarD:
    texto_caesar_d = caesarD.fetch()

print(texto_caesar_c)
print(texto_caesar_d)


textolegal = 'lucas é legalzao, po!'
with awp.criptografia.CifraDeVigenere(textolegal, 'lalaland','c') as vigenereC:
    texto_vigenere_c = vigenereC.fetch()

with awp.criptografia.CifraDeVigenere(texto_vigenere_c, 'lalaland','d') as vigenereD:
    texto_vigenere_d = vigenereD.fetch()

print(texto_vigenere_c)
print(texto_vigenere_d)