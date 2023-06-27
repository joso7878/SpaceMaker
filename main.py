import pygame
import tkinter as tk
from tkinter import simpledialog
import math

pygame.init()

# Definindo as dimensões da tela
largura = 1070
altura = 720
icon_path = "assets/space.ico"
background_image_path = "assets/sky.jpg"
background_music_path = "assets/music.mp3"
marcacoes_file_path = ""
tela = pygame.display.set_mode((largura, altura))

# Iniciando a janela do pygame
pygame.display.set_caption("Space Maker")
screen = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()

# Iniciação da janela do tkinter para diálogo
root = tk.Tk()
root.withdraw()

# Carregamento das marcações
marcacoes = []
icon_path = "assets/icon.jpg"

# Carregar a fonte para o texto
font = pygame.font.Font(None, 20)

def click_handler(pos):
    item = simpledialog.askstring("Space", "Nome da estrela:")
    if item is None:
        item = "desconhecido_" + str(pos)

    # Marcando nome da estrela e posição
    marca = {
        "nome": item,
        "posicao": pos
    }

    # Marcando a lista de marcações
    marcacoes.append(marca)

    print("Nome da estrela:", item)
    print("Posição:", pos)

def save_marks():
    with open(marcacoes_file_path, "w") as file:
        for marca in marcacoes:
            nome = marca["nome"]
            posicao = marca["posicao"]
            line = f"{nome},{posicao[0]},{posicao[1]}\n"
            file.write(line)

    print("Marcações salvas com sucesso!")

def load_marks():
    marcacoes.clear()
    try:
        with open(marcacoes_file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    data = line.split(",")
                    if len(data) == 3:
                        nome = data[0]
                        posicao = (int(data[1]), int(data[2]))
                        marca = {
                            "nome": nome,
                            "posicao": posicao
                        }
                        marcacoes.append(marca)

            print("Marcações carregadas com sucesso!")
    except FileNotFoundError:
        print("Nenhum arquivo de marcações encontrado.")

def delete_marks():
    marcacoes.clear()
    print("Todas as marcações foram excluídas!")

def on_closing():
    save_marks()
    pygame.quit()
    root.destroy()

# Carregar ícone de aplicação
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

# Carregar imagem de background
background_image = pygame.image.load(background_image_path)

# Configurar música de fundo em looping
pygame.mixer.music.load(background_music_path)
pygame.mixer.music.play(-1)

# Função para calcular a distância entre duas coordenadas
def calculate_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                on_closing()
            elif event.key == pygame.K_F10:
                save_marks()
            elif event.key == pygame.K_F11:
                load_marks()
            elif event.key == pygame.K_F12:
                delete_marks()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            click_handler(pos)

    # Desenhar o background
    screen.blit(background_image, (0, 0))

    # Desenhar as marcações existentes
    for i, marca in enumerate(marcacoes):
        posicao = marca["posicao"]
        pygame.draw.circle(screen, (255, 255, 255), posicao, 5)

        # Desenhar linhas entre os pontos
        if i > 0:
            posicao_anterior = marcacoes[i - 1]["posicao"]
            pygame.draw.line(screen, (255, 255, 255), posicao_anterior, posicao)

            # Calcular distância entre as coordenadas
            distance = calculate_distance(posicao, posicao_anterior)

            # Exibir a distância como texto sobre a linha
            text_distance = font.render(f"Distância: {distance:.2f}", True, (255, 255, 255))
            text_distance_rect = text_distance.get_rect()
            text_distance_rect.center = (
            (posicao[0] + posicao_anterior[0]) // 2, (posicao[1] + posicao_anterior[1]) // 2)
            screen.blit(text_distance, text_distance_rect)

        text = font.render(marca["nome"], True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topright = (posicao[0] + 10, posicao[1])
        screen.blit(text, text_rect)

    # Exibir o texto no canto superior direito
    text_save = font.render("Pressione F10 para salvar os pontos", True, (255, 255, 255))
    text_save_rect = text_save.get_rect()
    text_save_rect.topright = (largura - 10, 10)
    screen.blit(text_save, text_save_rect)

    text_load = font.render("Pressione F11 para carregar os pontos", True, (255, 255, 255))
    text_load_rect = text_load.get_rect()
    text_load_rect.topright = (largura - 10, 35)
    screen.blit(text_load, text_load_rect)

    text_delete = font.render("Pressione F12 para deletar os pontos", True, (255, 255, 255))
    text_delete_rect = text_delete.get_rect()
    text_delete_rect.topright = (largura - 10, 60)
    screen.blit(text_delete, text_delete_rect)

    pygame.display.flip()
    clock.tick(60)

# Janela do tkinter não será exibida, mas é necessária para os diálogos
root.mainloop()
