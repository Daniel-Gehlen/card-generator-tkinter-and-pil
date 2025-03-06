from PIL import Image, ImageDraw, ImageFont
import random
import colorsys

class CardModerno:
    def __init__(self, titulo, texto, largura=500, altura=500):
        self.titulo = titulo
        self.texto = texto
        self.largura = largura
        self.altura = altura

    def create_card(self, nome_arquivo='card_moderno.png'):
        # Criar imagem com gradiente moderno
        img, (r, g, b) = self.gerar_gradiente_moderno(self.largura, self.altura)
        draw = ImageDraw.Draw(img)

        # Carregar fontes
        try:
            fonte_titulo = ImageFont.truetype("Poppins-Bold.ttf", 36)  # Fonte maior para o título
            fonte_texto = ImageFont.truetype("Poppins-Regular.ttf", 22)   # Fonte maior para o texto
        except IOError:
            fonte_titulo = ImageFont.load_default()
            fonte_texto = ImageFont.load_default()

        # Calcular altura do título
        largura_max_titulo = self.largura - 100  # Margem para os botões
        linhas_titulo = self.quebrar_titulo(self.titulo, largura_max_titulo, fonte_titulo, draw)
        altura_titulo_barra = max(60, (len(linhas_titulo) * fonte_titulo.getbbox("A")[3]) + 30)

        # Barra de título com gradiente mais escuro e contrastante
        for y in range(altura_titulo_barra):
            cor = (int(r * (0.1 + y / altura_titulo_barra * 0.4)),
                   int(g * (0.1 + y / altura_titulo_barra * 0.4)),
                   int(b * (0.1 + y / altura_titulo_barra * 0.4)))
            draw.line([(0, y), (self.largura, y)], fill=cor)

        # Desenhar botões
        self.desenhar_botoes_janela(draw, self.largura, altura_titulo_barra)

        # Desenhar título
        y_titulo = (altura_titulo_barra - (len(linhas_titulo) * fonte_titulo.getbbox("A")[3])) // 2
        for linha in linhas_titulo:
            largura_linha = draw.textbbox((0, 0), linha, font=fonte_titulo)[2]
            x_titulo = (self.largura - largura_linha) // 2
            draw.text((x_titulo + 1, y_titulo + 1), linha, font=fonte_titulo, fill=(int(r * 1.2), int(g * 1.2), int(b * 1.2)))
            draw.text((x_titulo, y_titulo), linha, font=fonte_titulo, fill=(int(r * 1.4), int(g * 1.4), int(b * 1.4)))
            y_titulo += fonte_titulo.getbbox("A")[3] + 5

        # Desenhar grafos modernos no fundo
        self.desenhar_grafos_modernos(draw, self.largura, self.altura, altura_titulo_barra)

        # Preparar o texto
        palavras = self.texto.split()
        linhas = []
        linha_atual = ""
        largura_maxima = self.largura - 60

        for palavra in palavras:
            if draw.textbbox((0, 0), linha_atual + palavra + " ", font=fonte_texto)[2] <= largura_maxima:
                linha_atual += palavra + " "
            else:
                linhas.append(linha_atual.strip())
                linha_atual = palavra + " "
        if linha_atual:
            linhas.append(linha_atual.strip())

        # Desenhar caixas de texto com efeito moderno
        y_texto = altura_titulo_barra + 30
        for linha in linhas:
            largura_linha = draw.textbbox((0, 0), linha, font=fonte_texto)[2]
            altura_linha = fonte_texto.getbbox("A")[3]

            # Caixa principal
            x1, y1 = 30, y_texto - 5
            x2, y2 = self.largura - 30, y_texto + altura_linha + 5

            # Efeito de profundidade moderno
            gradiente_steps = 5
            for i in range(gradiente_steps):
                offset = i * 2
                alpha = 100 - (i * 20)
                cor = (int(r * (1 - i / gradiente_steps * 0.5)),
                       int(g * (1 - i / gradiente_steps * 0.5)),
                       int(b * (1 - i / gradiente_steps * 0.5)), alpha)
                draw.rectangle([x1 + offset, y1 + offset, x2 + offset, y2 + offset], fill=cor)

            # Caixa principal com borda suave
            draw.rectangle([x1, y1, x2, y2], fill=(int(r * 0.2), int(g * 0.2), int(b * 0.2)),
                          outline=(int(r * 0.3), int(g * 0.3), int(b * 0.3)))

            # Texto com brilho e neon
            draw.text((35, y_texto + 1), linha, font=fonte_texto, fill=(int(r * 1.2), int(g * 1.2), int(b * 1.2)))
            draw.text((34, y_texto), linha, font=fonte_texto, fill=(int(r * 1.4), int(g * 1.4), int(b * 1.4)))

            y_texto += altura_linha + 20

        # Salvar a imagem
        img.save(nome_arquivo)
        print(f"Card salvo como {nome_arquivo}")

    def gerar_gradiente_moderno(self, largura, altura):
        imagem = Image.new('RGB', (largura, altura))
        draw = ImageDraw.Draw(imagem)

        # Gerar uma cor aleatória no espaço de cor HSV
        h = random.random()
        s = 0.8  # Saturação fixa em 80%
        v = 0.9  # Valor (brilho) fixo em 90%
        r, g, b = [int(255 * c) for c in colorsys.hsv_to_rgb(h, s, v)]

        return imagem, (r, g, b)

    def desenhar_botoes_janela(self, draw, largura, altura_titulo_barra):
        botao_tamanho = 12
        espacamento_botao = 6
        y = 8

        # Botão fechar (vermelho com X)
        x_fechar = largura - botao_tamanho - espacamento_botao - 8
        draw.ellipse([x_fechar, y, x_fechar + botao_tamanho, y + botao_tamanho], fill=(255, 95, 87))
        offset = 3
        draw.line([x_fechar + offset, y + offset, x_fechar + botao_tamanho - offset, y + botao_tamanho - offset], fill=(75, 25, 22), width=1)
        draw.line([x_fechar + botao_tamanho - offset, y + offset, x_fechar + offset, y + botao_tamanho - offset], fill=(75, 25, 22), width=1)

        # Botão maximizar (amarelo com quadrado)
        x_maximizar = x_fechar - (botao_tamanho + espacamento_botao)
        draw.ellipse([x_maximizar, y, x_maximizar + botao_tamanho, y + botao_tamanho], fill=(255, 189, 46))
        offset = 3
        draw.rectangle([x_maximizar + offset, y + offset, x_maximizar + botao_tamanho - offset, y + botao_tamanho - offset], outline=(75, 55, 12), width=1)

        # Botão minimizar (verde com traço)
        x_minimizar = x_maximizar - (botao_tamanho + espacamento_botao)
        draw.ellipse([x_minimizar, y, x_minimizar + botao_tamanho, y + botao_tamanho], fill=(39, 201, 63))
        offset = 3
        y_linha = y + (botao_tamanho // 2)
        draw.line([x_minimizar + offset, y_linha, x_minimizar + botao_tamanho - offset, y_linha], fill=(12, 55, 15), width=1)

    def desenhar_grafos_modernos(self, draw, largura, altura, altura_titulo_barra):
        num_linhas = random.randint(15, 30)
        for _ in range(num_linhas):
            opacidade = random.randint(30, 50)
            pontos = [(random.randint(0, largura), random.randint(altura_titulo_barra, altura)) for _ in range(random.randint(2, 4))]
            for i in range(len(pontos) - 1):
                x1, y1 = pontos[i]
                x2, y2 = pontos[i + 1]
                cx = (x1 + x2) // 2
                cy = random.randint(min(y1, y2), max(y1, y2))
                for t in range(0, 100, 2):
                    t = t / 100
                    x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t ** 2 * x2
                    y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t ** 2 * y2
                    draw.point((int(x), int(y)), fill=(40, 40, 40, opacidade))

    def quebrar_titulo(self, titulo, largura_maxima, fonte, draw):
        palavras = titulo.split(' ')
        linhas = []
        linha_atual = ""
        for palavra in palavras:
            largura_linha_atual = draw.textbbox((0, 0), linha_atual + palavra + " ", font=fonte)[2]
            if largura_linha_atual <= largura_maxima:
                linha_atual += palavra + " "
            else:
                linhas.append(linha_atual.strip())
                linha_atual = palavra + " "
        if linha_atual:
            linhas.append(linha_atual.strip())
        return linhas
