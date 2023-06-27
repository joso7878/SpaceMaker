import pygame
import tkinter as tk
from tkinter import simpledialog
import math

pygame.init()

# Definindo as dimensões da tela
largura = 1070
altura = 720
caminho_icone = "assets/icon.png"
caminho_imagem_fundo = "assets/sky.jpg"
caminho_musica_fundo = "assets/music.mp3"
caminho_arquivo_marcacoes = "marcacoes_salvas.txt"
tela = pygame.display.set_mode((largura, altura))

# Iniciando a janela do pygame
pygame.display.set_caption("Space Maker")
screen = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()

# Iniciando a janela do tkinter para diálogos
root = tk.Tk()
root.withdraw()

# Carregamento das marcações
marcacoes = []
caminho_icone = "assets/icon.png"

# Carregar a fonte para o texto
fonte = pygame.font.Font(None, 20)

def manipular_clique(pos):
    # Verificar se o clique ocorre na parte superior da tela
    if pos[1] < altura - altura // 5:
        item = simpledialog.askstring("Space", "Nome da estrela:")
        if item is None:
            item = "desconhecido_" + str(pos)

        # Marcar o nome da estrela e a posição
        marca = {
            "nome": item,
            "posicao": pos
        }

        # Adicionar a marcação à lista de marcações
        marcacoes.append(marca)

        print("Nome da estrela:", item)
        print("Posição:", pos)

def salvar_marcacoes():
    with open(caminho_arquivo_marcacoes, "w") as arquivo:
        for marca in marcacoes:
            nome = marca["nome"]
            posicao = marca["posicao"]
            linha = f"{nome},{posicao[0]},{posicao[1]}\n"
            arquivo.write(linha)

    print("Marcações salvas com sucesso!")

def carregar_marcacoes():
    marcacoes.clear()
    try:
        with open(caminho_arquivo_marcacoes, "r") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    dados = linha.split(",")
                    if len(dados) == 3:
                        nome = dados[0]
                        posicao = (int(dados[1]), int(dados[2]))
                        marca = {
                            "nome": nome,
                            "posicao": posicao
                        }
                        marcacoes.append(marca)

            print("Marcações carregadas com sucesso!")
    except FileNotFoundError:
        print("Nenhum arquivo de marcações encontrado.")

def deletar_marcacoes():
    marcacoes.clear()
    print("Todas as marcações foram excluídas!")

def ao_fechar():
    salvar_marcacoes()
    pygame.quit()
    root.destroy()

# Carregar ícone do aplicativo
icone = pygame.image.load(caminho_icone)
pygame.display.set_icon(icone)

# Carregar imagem de fundo
imagem_fundo = pygame.image.load(caminho_imagem_fundo)

# Configurar música de fundo em looping
pygame.mixer.music.load(caminho_musica_fundo)
pygame.mixer.music.play(-1)

# Função para calcular a distância entre duas coordenadas
def calcular_distancia(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distancia

executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ao_fechar()
            elif evento.key == pygame.K_F10:
                salvar_marcacoes()
            elif evento.key == pygame.K_F11:
                carregar_marcacoes()
            elif evento.key == pygame.K_F12:
                deletar_marcacoes()

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = pygame.mouse.get_pos()
            manipular_clique(pos)

    # Desenhar o fundo
    screen.blit(imagem_fundo, (0, 0))

    # Desenhar as marcações existentes
    for i, marca in enumerate(marcacoes):
        posicao = marca["posicao"]
        pygame.draw.circle(screen, (255, 255, 255), posicao, 5)

        # Desenhar linhas entre os pontos
        if i > 0:
            posicao_anterior = marcacoes[i - 1]["posicao"]
            pygame.draw.line(screen, (255, 255, 255), posicao_anterior, posicao)

            # Calcular distância entre as coordenadas
            distancia = calcular_distancia(posicao, posicao_anterior)

            # Exibir a distância como texto sobre a linha
            texto_distancia = fonte.render(f"Distância: {distancia:.2f}", True, (255, 255, 255))
            retangulo_texto_distancia = texto_distancia.get_rect()
            retangulo_texto_distancia.center = (
            (posicao[0] + posicao_anterior[0]) // 2, (posicao[1] + posicao_anterior[1]) // 2)
            screen.blit(texto_distancia, retangulo_texto_distancia)

        texto = fonte.render(marca["nome"], True, (255, 255, 255))
        retangulo_texto = texto.get_rect()
        retangulo_texto.topleft = (posicao[0] + 10, posicao[1])
        screen.blit(texto, retangulo_texto)

    # Exibir texto no canto superior esquerdo
    texto_salvar = fonte.render("Pressione F10 para salvar os pontos", True, (9, 209, 227))
    retangulo_texto_salvar = texto_salvar.get_rect()
    retangulo_texto_salvar.topleft = (10, 10)
    screen.blit(texto_salvar, retangulo_texto_salvar)

    texto_carregar = fonte.render("Pressione F11 para carregar os pontos", True, (9, 209, 227))
    retangulo_texto_carregar = texto_carregar.get_rect()
    retangulo_texto_carregar.topleft = (10, 35)
    screen.blit(texto_carregar, retangulo_texto_carregar)

    texto_deletar = fonte.render("Pressione F12 para deletar os pontos", True, (9, 209, 227))
    retangulo_texto_deletar = texto_deletar.get_rect()
    retangulo_texto_deletar.topleft = (10, 60)
    screen.blit(texto_deletar, retangulo_texto_deletar)

    pygame.display.flip()
    clock.tick(60)

# A janela do tkinter não será exibida, mas é necessária para os diálogos
root.mainloop()
