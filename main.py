import tkinter as tk
from tkinter import ttk
from card_aleatorio import CardAleatorio
from card_grafos import CardGrafos
from card_moderno import CardModerno
from card_notas_musicais import CardNotasMusicais
from card_preto import CardPreto

class CardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Cards")
        
        # Lista de cards disponíveis
        self.cards = {
            "Aleatório": CardAleatorio,
            "Grafos": CardGrafos,
            "Moderno": CardModerno,
            "Notas Musicais": CardNotasMusicais,
            "Preto": CardPreto
        }
        
        # Variável para armazenar o card selecionado
        self.card_selecionado = tk.StringVar()
        self.card_selecionado.set("Aleatório")  # Valor padrão
        
        # Interface
        self.criar_interface()

    def criar_interface(self):
        # Frame principal
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Label e Combobox para seleção do card
        ttk.Label(frame, text="Escolha o tipo de card:").grid(row=0, column=0, sticky=tk.W)
        self.combobox = ttk.Combobox(frame, textvariable=self.card_selecionado)
        self.combobox['values'] = list(self.cards.keys())
        self.combobox.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Entrada para o título do card
        ttk.Label(frame, text="Título do card:").grid(row=1, column=0, sticky=tk.W)
        self.titulo_entry = ttk.Entry(frame, width=40)
        self.titulo_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        # Entrada para o texto do card
        ttk.Label(frame, text="Texto do card:").grid(row=2, column=0, sticky=tk.W)
        self.texto_entry = tk.Text(frame, height=10, width=40)
        self.texto_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))
        
        # Botão para gerar o card
        ttk.Button(frame, text="Gerar Card", command=self.gerar_card).grid(row=3, column=0, columnspan=2)
        
        # Frame para exibir o card gerado
        self.card_frame = ttk.Frame(frame, padding="10")
        self.card_frame.grid(row=4, column=0, columnspan=2)

    def gerar_card(self):
        # Limpa o frame do card anterior
        for widget in self.card_frame.winfo_children():
            widget.destroy()
        
        # Obtém o título e o texto inseridos pelo usuário
        titulo = self.titulo_entry.get().strip()
        texto = self.texto_entry.get("1.0", tk.END).strip()
        
        if not titulo or not texto:
            tk.messagebox.showwarning("Aviso", "Por favor, insira o título e o texto do card.")
            return
        
        # Obtém a classe do card selecionado
        card_class = self.cards[self.card_selecionado.get()]
        
        # Cria o card selecionado
        card = card_class(titulo, texto)
        
        # Gera o card e salva a imagem
        nome_arquivo = f"card_{self.card_selecionado.get().lower().replace(' ', '_')}.png"
        card.create_card(nome_arquivo)
        
        # Exibe uma mensagem de sucesso
        tk.messagebox.showinfo("Sucesso", f"Card gerado e salvo como {nome_arquivo}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CardApp(root)
    root.mainloop()
