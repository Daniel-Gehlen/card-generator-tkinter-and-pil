from PIL import Image, ImageDraw, ImageFont
import random

class CardAleatorio:
    def __init__(self, titulo, texto, largura=500, altura=500, cor_fundo=(200, 200, 200), cor_borda=(0, 0, 0), cor_texto=(0, 0, 0)):
        self.titulo = titulo
        self.texto = texto
        self.largura = largura
        self.altura = altura
        self.cor_fundo = cor_fundo
        self.cor_borda = cor_borda
        self.cor_texto = cor_texto

    def create_card(self, nome_arquivo='card_aleatorio.png'):
        # Criando a imagem
        img = Image.new('RGB', (self.largura, self.altura), self.cor_fundo)
        draw = ImageDraw.Draw(img)

        # Carregando fontes (Arial)
        try:
            fonte_titulo = ImageFont.truetype("Poppins-Bold.ttf", 24)  # Fonte para o título
            fonte_texto = ImageFont.truetype("Poppins-Regular.ttf", 16)   # Fonte para o texto
        except IOError:
            # Se a fonte Arial não estiver disponível, usa uma fonte padrão
            fonte_titulo = ImageFont.load_default()
            fonte_texto = ImageFont.load_default()

        # Desenhando borda ao redor da janela
        espessura_borda = 4
        draw.rectangle([0, 0, self.largura, self.altura], outline=self.cor_borda, width=espessura_borda)

        # Desenhando barra de título no topo
        altura_titulo_barra = 50
        draw.rectangle([0, 0, self.largura, altura_titulo_barra], fill=(180, 180, 180), outline=self.cor_borda)

        # Centralizando o título na barra de título
        largura_titulo, altura_titulo = draw.textbbox((0, 0), self.titulo, font=fonte_titulo)[2:4]
        posicao_titulo = ((self.largura - largura_titulo) // 2, (altura_titulo_barra - altura_titulo) // 2)
        draw.text(posicao_titulo, self.titulo, font=fonte_titulo, fill=self.cor_texto)

        # Função para formatar o texto como blocos de código ou poema
        def formatar_texto(texto, largura, margem_lateral, fonte):
            linhas = []
            palavras = texto.split(' ')
            linha_atual = ""
            largura_maxima = largura - 2 * margem_lateral
            pontuacoes = {'.', '!', '?'}

            # Variáveis para indentação
            indentacao = ' ' * 4  # 4 espaços de indentação
            nova_linha = True  # Identifica se é o início de uma nova linha

            for palavra in palavras:
                largura_linha_atual = draw.textbbox((0, 0), linha_atual + palavra, font=fonte)[2]

                if largura_linha_atual <= largura_maxima:
                    if nova_linha:
                        linha_atual += palavra + " "
                        nova_linha = False  # Depois da primeira palavra, não é mais nova linha
                    else:
                        linha_atual += palavra + " "
                else:
                    if linha_atual.strip():
                        linhas.append(linha_atual.strip())
                    linha_atual = indentacao + palavra + " "  # Adiciona indentação no início da nova linha
            if linha_atual:
                linhas.append(linha_atual.strip())

            # Adiciona uma linha em branco entre frases que terminam com pontuação
            linhas_formatadas = []
            for linha in linhas:
                linhas_formatadas.append(linha)
                if linha and linha[-1] in pontuacoes:
                    linhas_formatadas.append("")  # Adiciona uma linha em branco após a frase

            return linhas_formatadas

        # Dividindo o texto em múltiplas linhas formatadas
        margem_lateral = 30
        espacamento = 10  # Ajustado para o espaçamento entre linhas
        y_texto = altura_titulo_barra + espacamento
        linhas_texto = formatar_texto(self.texto, self.largura, margem_lateral, fonte_texto)

        # Posicionar e desenhar o corpo do texto
        for linha in linhas_texto:
            largura_linha, altura_linha = draw.textbbox((0, 0), linha, font=fonte_texto)[2:4]
            draw.text(((self.largura - largura_linha) // 2, y_texto), linha, font=fonte_texto, fill=self.cor_texto)
            y_texto += altura_linha + espacamento

        # Calcular posição inferior do texto
        y_final_texto = y_texto

        # Função para desenhar linhas de partitura
        def desenhar_partitura(draw, x, y, largura):
            espaçamento = 10  # Espaçamento entre as linhas
            for i in range(5):  # 5 linhas de partitura
                draw.line([x, y + i * espaçamento, largura, y + i * espaçamento], fill=(0, 0, 0), width=2)

        # Função para desenhar uma clave de sol
        def desenhar_clave_de_sol(draw, x, y):
            draw.line([x, y, x, y + 60], fill=(0, 0, 0), width=2)  # Linha vertical da clave de sol
            draw.arc([x - 15, y, x + 15, y + 60], start=180, end=360, fill=(0, 0, 0), width=2)  # Parte superior
            draw.arc([x - 10, y + 10, x + 10, y + 70], start=180, end=360, fill=(0, 0, 0), width=2)  # Parte média
            draw.arc([x - 5, y + 20, x + 5, y + 80], start=180, end=360, fill=(0, 0, 0), width=2)  # Parte inferior

        # Função para desenhar notas musicais
        def desenhar_nota(draw, x, y):
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], outline=(0, 0, 0), fill=(0, 0, 0))  # Nota como círculo

        # Função para desenhar escalas musicais aleatórias
        def desenhar_escala_aleatoria(draw, x_inicio, y_inicio, largura, altura):
            x = x_inicio
            y = y_inicio

            # Limitar a altura até o final da área útil do card
            while x < largura:
                desenhar_nota(draw, x, y)
                x += 20  # Próxima nota mais à direita

                # Muda aleatoriamente a direção da nota (ascendente ou descendente)
                direcao = random.choice([-1, 1])
                y += direcao * 10  # Sobe ou desce de forma aleatória

                # Não ultrapassar os limites do pentagrama
                if y < y_inicio - 40:
                    y = y_inicio + random.randint(0, 40)
                elif y > y_inicio + 40:
                    y = y_inicio - random.randint(0, 40)

        # Desenhando múltiplos pentagramas abaixo do texto, começando a partir do limite inferior do texto
        espaco_entre_pentagramas = 60
        y_inicial_partitura = y_final_texto + 20  # Começa logo abaixo do texto
        while y_inicial_partitura + espaco_entre_pentagramas < self.altura:
            desenhar_partitura(draw, 20, y_inicial_partitura, self.largura - 40)
            desenhar_clave_de_sol(draw, 50, y_inicial_partitura)
            desenhar_escala_aleatoria(draw, 100, y_inicial_partitura + 5, self.largura - 100, self.altura)
            y_inicial_partitura += espaco_entre_pentagramas

        # Salvando a imagem
        img.save(nome_arquivo)
        print(f"Card salvo como {nome_arquivo}")
