try:
    # Tentar abrir um arquivo que não existe
    file = open('arquivo_inexistente.txt', 'r')
    file_content = file.read()
except FileNotFoundError as e:
    # Capturar a exceção de arquivo não encontrado
    print(f"Erross: {e}")
else:
    # Executado se não houver exceção
    print("Arquivo lido com sucesso")
    print(file_content)
finally:
    # Executado sempre, independentemente de exceção
    print("Bloco finally executado")
