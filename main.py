import pygame
import tkinter as tk
from tkinter import simpledialog

pygame.init()

#Definindo as dimensões da tela
largura = 1070
altura = 720
icon_path = "assets/space.ico"
background_image_path = "assets/sky.jpg"
background_music_path = "assets/music.mp3"
marcacoes_file_path = ""
tela = pygame.display.set_mode((largura, altura))

#Iniciando a janela do pygame
pygame.display.set_caption("Space Maker")
screen = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()

#Iniciação da janela do tkinter para dialogo
root = tk.Tk()
root.withdraw()

#Carregamento das marcação
marcacoes = []
icon_path = "assets/icon.jpg"

#Carregar a fonte para o texto
font = pygame.font.Font(None, 20)

def click_handler(pos) :
    item = simpledialog.askstring("Space", "Nome da estrela:")
    if item is None:
        item = "desconhecido_" + str(pos)

#Marcando nome da estrela e posição
marca = {
    "nome": item,
    "posicao": pos 
}

#Marcando a lista de marcalções
marcacoes.append(marca)

print("Nome da estrela:", item)
print("Posição:", pos)

def save_marks():
    with open(marcacoes_file_path, "w") as file:
        for marca in marcacoes:
            nome = marca ["nome"]
            posicao = marca ["posicao"]
            line = f"{nome},{posicao[0]},{posicao[1]}\n"
            file.write(line)
    
    print("Marcações salvas com sucesso!")

def load_marks():
    marcacoes.clear()
    try:
        with open(marcacoes_file_path, "r") as file:
            for line in line:
                line = line.strip()
                if line:
                    data = line.split(",")
                    if len(data) == 3:
                        nome = data[0]
                        posicao = (int(data[1]), int(data[2]))
                        marca = {
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

#Carregar ícone de aplicação
icon = pygame.imaage.load(icon_path)
pygame.display.set.icom(icon)

#Carregar imagem de background
background_image = pygame.image.load(background_image_path)

        
    
            

  