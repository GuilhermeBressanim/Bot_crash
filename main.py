import threading
import os


def inicia_programa(nome_arquivo):
    os.system('python -u "{}"'.format(nome_arquivo))


if __name__ == "__main__":
    # cwd = os.getcwd()
    arquivos = [
        "c:\/Users\/guilh\/OneDrive\/Área de Trabalho\/Projetos\/Projeto2\/banco\/main.py", "C:\/Users\/guilh\/OneDrive\/Área de Trabalho\/Projetos\/Projeto2\/bot_notifica\/main.py"]

    processos = []
    for arquivo in arquivos:
        processos.append(threading.Thread(
            target=inicia_programa, args=(arquivo,)))

    for processo in processos:
        processo.start()
