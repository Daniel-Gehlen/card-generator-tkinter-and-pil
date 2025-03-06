from PIL import Image, ImageDraw, ImageFont
import random
import colorsys

class CardGrafos:
    def __init__(self, titulo, texto, largura=500, altura=500):
        self.titulo = titulo
        self.texto = texto
        self.largura = largura
        self.altura = altura

    def create_card(self, nome_arquivo='card_grafos.png'):
        # Gerar paleta monocromática
        paleta = self.gerar_paleta_monocromatica()
        cor_fundo = paleta[0]
        cor_grafos = (255, 255, 255)  # Linhas dos grafos em branco

        # Garantir que a cor do texto seja mais brilhante que o fundo
        cor_texto = (255, 255, 0) if cor_fundo[0] < 128 else (0, 0, 0)  # Texto em amarelo se fundo escuro, ou em preto

        # Criar a imagem
        img = Image.new('RGB', (self.largura, self.altura), cor_fundo)
        draw = ImageDraw.Draw(img)

        # Carregar fontes
        try:
            fonte_titulo = ImageFont.truetype("Poppins-Bold.ttf", 32)
            fonte_texto = ImageFont.truetype("Poppins-Regular.ttf", 18)
        except IOError:
            fonte_titulo = ImageFont.load_default()
            fonte_texto = ImageFont.load_default()

        # Desenhar borda ao redor da janela
        espessura_borda = 4
        draw.rectangle([0, 0, self.largura, self.altura], outline=(0, 0, 0), width=espessura_borda)

        # Quebrar o título em múltiplas linhas
        linhas_titulo = self.quebrar_titulo(self.titulo, self.largura - 40, fonte_titulo, draw)

        # Calcular a altura da barra de título
        altura_titulo_barra = max(50, (len(linhas_titulo) * fonte_titulo.getbbox("A")[3]) + 20)

        # Cor do fundo do título
        cor_fundo_titulo = (255, 215, 0) if cor_texto == (0, 0, 0) else (0, 128, 255)  # Amarelo se texto escuro, azul se texto claro
        draw.rectangle([0, 0, self.largura, altura_titulo_barra], fill=cor_fundo_titulo, outline=(0, 0, 0))

        # Desenhar o título
        y_titulo = (altura_titulo_barra - (len(linhas_titulo) * fonte_titulo.getbbox("A")[3])) // 2
        for linha in linhas_titulo:
            largura_linha, altura_linha = draw.textbbox((0, 0), linha, font=fonte_titulo)[2:]
            x_titulo = (self.largura - largura_linha) // 2
            draw.text((x_titulo, y_titulo), linha, font=fonte_titulo, fill=(0, 0, 0))
            y_titulo += altura_linha

        # Desenhar grafos no fundo
        self.desenhar_grafos(draw, self.largura, self.altura, altura_titulo_barra)

        # Formatar e desenhar o texto
        espacamento = 10
        linhas_texto = self.formatar_texto(self.texto, self.largura, 20, fonte_texto, draw)
        y_texto = altura_titulo_barra + 20

        # Cor do fundo do texto
        cor_fundo_texto = (240, 240, 240) if cor_texto == (0, 0, 0) else (50, 50, 50)  # Cinza claro se texto escuro, cinza escuro se texto claro

        # Aumentar a margem abaixo do corpo do texto
        margem_extra_abaixo = 30  # Margem adicional abaixo do texto

        # Coordenadas do retângulo de fundo
        x1 = 30 - 10  # Margem à esquerda
        y1 = y_texto - 10  # Margem acima
        x2 = self.largura - 30 + 10  # Margem à direita
        y2 = y_texto + (len(linhas_texto) * (fonte_texto.getbbox("A")[3] + espacamento)) + margem_extra_abaixo  # Margem abaixo

        # Desenhar o retângulo de fundo
        draw.rectangle([x1, y1, x2, y2], fill=cor_fundo_texto)

        # Desenhar o texto sobre o fundo
        for linha in linhas_texto:
            draw.text((30, y_texto), linha, font=fonte_texto, fill=cor_texto)
            y_texto += fonte_texto.getbbox(linha)[3] + espacamento

        # Salvar a imagem
        img.save(nome_arquivo)
        print(f"Card gerado e salvo como '{nome_arquivo}'.")

    def gerar_paleta_monocromatica(self):
        hue = random.random()
        paleta = []
        for i in range(5):
            cor = colorsys.hsv_to_rgb(hue, random.uniform(0.5, 1.0), random.uniform(0.2, 0.6))
            cor_rgb = tuple(int(x * 255) for x in cor)
            paleta.append(cor_rgb)
        return paleta

    def desenhar_grafos(self, draw, largura, altura, altura_titulo_barra):
        num_linhas = random.randint(20, 50)
        for _ in range(num_linhas):
            pontos = [(random.randint(0, largura), random.randint(altura_titulo_barra, altura)) for _ in range(random.randint(3, 6))]
            cor_linha = (255, 255, 255)  # Branco
            largura_linha = random.randint(1, 3)
            for i in range(len(pontos) - 1):
                draw.line([pontos[i], pontos[i + 1]], fill=cor_linha, width=largura_linha)

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

    def formatar_texto(self, texto, largura, margem_lateral, fonte, draw):
        linhas = []
        palavras = texto.split(' ')
        linha_atual = ""
        largura_maxima = largura - 2 * margem_lateral - 10
        for palavra in palavras:
            if draw.textbbox((0, 0), linha_atual + palavra + " ", font=fonte)[2] <= largura_maxima:
                linha_atual += palavra + " "
            else:
                if linha_atual.strip():
                    linhas.append(linha_atual.strip())
                linha_atual = palavra + " "
        if linha_atual:
            linhas.append(linha_atual.strip())
        return linhas
