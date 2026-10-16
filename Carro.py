
import pygame
import random
import sys

pygame.init()

tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
LARGURA, ALTURA = tela.get_size()

pygame.display.set_caption("Corrida Radical")

relogio = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 36)
fonte_grande = pygame.font.SysFont(None, 58)

BRANCO = (255, 255, 255)
PRETO = (20, 20, 20)
VERDE = (35, 145, 65)
CINZA = (65, 65, 70)
AMARELO = (255, 220, 40)
AZUL = (30, 140, 255)
VERMELHO = (235, 45, 45)

estrada_x = 70
estrada_largura = 340

jogador = pygame.Rect(210, 640, 60, 100)
inimigos = []
linhas = [i * 150 for i in range(7)]

velocidade = 6
pontos = 0
fim_de_jogo = False
movimento = 0
contador = 0


def desenhar_carro(ret, cor):
    pygame.draw.rect(tela, cor, ret, border_radius=12)
    pygame.draw.rect(
        tela, (180, 225, 255),
        (ret.x + 10, ret.y + 15, 40, 25),
        border_radius=5
    )
    pygame.draw.rect(
        tela, (40, 40, 45),
        (ret.x + 8, ret.y + 53, 44, 25),
        border_radius=5
    )
    pygame.draw.rect(
        tela, PRETO,
        (ret.x - 5, ret.y + 18, 8, 22),
        border_radius=3
    )
    pygame.draw.rect(
        tela, PRETO,
        (ret.x + ret.width - 3, ret.y + 18, 8, 22),
        border_radius=3
    )


def reiniciar():
    global pontos, velocidade, fim_de_jogo
    global inimigos, contador, movimento

    jogador.x = 210
    inimigos = []
    pontos = 0
    velocidade = 6
    contador = 0
    movimento = 0
    fim_de_jogo = False


while True:
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if fim_de_jogo and evento.key in (
                pygame.K_SPACE, pygame.K_RETURN
            ):
                reiniciar()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos

            if fim_de_jogo:
                if y > 450:
                    reiniciar()
            elif y > 680:
                if x < LARGURA // 2:
                    movimento = -1
                else:
                    movimento = 1

        if evento.type == pygame.MOUSEBUTTONUP:
            movimento = 0

        if evento.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0] and not fim_de_jogo:
                x, y = evento.pos
                if y > 680:
                    movimento = -1 if x < LARGURA // 2 else 1

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        movimento = -1
    elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        movimento = 1
    elif not pygame.mouse.get_pressed()[0]:
        movimento = 0

    tela.fill(VERDE)

    pygame.draw.rect(
        tela, CINZA,
        (estrada_x, 0, estrada_largura, ALTURA)
    )

    pygame.draw.rect(
        tela, BRANCO,
        (estrada_x, 0, 6, ALTURA)
    )
    pygame.draw.rect(
        tela, BRANCO,
        (estrada_x + estrada_largura - 6, 0, 6, ALTURA)
    )

    for i in range(len(linhas)):
        pygame.draw.rect(
            tela, AMARELO,
            (236, linhas[i], 8, 75)
        )
        if not fim_de_jogo:
            linhas[i] += velocidade
            if linhas[i] > ALTURA:
                linhas[i] = -100

    if not fim_de_jogo:
        jogador.x += movimento * 7
        jogador.x = max(
            estrada_x + 12,
            min(jogador.x, estrada_x + estrada_largura - 72)
        )

        contador += 1

        if contador > max(20, 55 - pontos // 5):
            x = random.choice([115, 205, 295, 345])
            inimigos.append(
                pygame.Rect(x, -110, 60, 100)
            )
            contador = 0

        for carro in inimigos[:]:
            carro.y += velocidade

            if carro.y > ALTURA:
                inimigos.remove(carro)
                pontos += 1

            elif jogador.colliderect(carro):
                fim_de_jogo = True

        velocidade = min(12, 6 + pontos // 10)

    desenhar_carro(jogador, AZUL)

    for carro in inimigos:
        desenhar_carro(carro, VERMELHO)

    texto = fonte.render(
        f"Pontos: {pontos}", True, BRANCO
    )
    tela.blit(texto, (15, 15))

    pygame.draw.rect(
        tela, (35, 35, 35), (0, 700, 240, 100)
    )
    pygame.draw.rect(
        tela, (45, 45, 45), (240, 700, 240, 100)
    )

    esquerda = fonte_grande.render("<", True, BRANCO)
    direita = fonte_grande.render(">", True, BRANCO)

    tela.blit(esquerda, (100, 725))
    tela.blit(direita, (340, 725))

    if fim_de_jogo:
        sombra = pygame.Surface((LARGURA, ALTURA))
        sombra.set_alpha(190)
        sombra.fill(PRETO)
        tela.blit(sombra, (0, 0))

        texto_fim = fonte_grande.render(
            "FIM DE JOGO", True, VERMELHO
        )
        texto_pontos = fonte.render(
            f"Pontuacao: {pontos}", True, BRANCO
        )
        texto_reiniciar = fonte.render(
            "Toque para jogar novamente", True, AMARELO
        )

        tela.blit(
            texto_fim,
            texto_fim.get_rect(center=(240, 320))
        )
        tela.blit(
            texto_pontos,
            texto_pontos.get_rect(center=(240, 385))
        )
        tela.blit(
            texto_reiniciar,
            texto_reiniciar.get_rect(center=(240, 465))
        )

    pygame.display.flip()
