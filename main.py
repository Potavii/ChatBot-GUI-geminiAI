#bibliotecas
#tkinter para interface gráfica
import tkinter as tk
from tkinter import scrolledtext, messagebox
#treading para não travar a interface enquanto a IA processa a resposta
import threading
#dotenv para carregar chaves de ambiente
import os
from dotenv import load_dotenv
#gemini para acessar a API do Gemini Pro
import google.generativeai as genai
#especificações para cores e fontes
from especificacoes import COLORS, FONT_MAIN, FONT_BOLD

# Carrega chaves de ambiente
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Classe principal do aplicativo
class GeminiChatApp:
    # Inicialização da interface e configuração do modelo
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini Assistant Pro")
        self.root.geometry("500x700")
        
        # Estado inicial do tema
        self.current_theme = "light"
        
        # Inicializa o modelo da IA
        # customização da interface
        self.setup_ui()
        self.apply_theme()
        # Configuração do modelo com "instruções de sistema"
        self.model = genai.GenerativeModel(
            model_name='models/gemini-3-flash-preview', # Versão do gemini(escolha a que achar melhor a partir das versões que sua key permite)
            system_instruction="Você é um assistente amigável e profissional chamado Gemini Pro. Ajude o usuário com respostas claras e diretas."
        )
        self.chat = self.model.start_chat(history=[])

    def setup_ui(self):
        """Constrói a estrutura Header, Body, Footer"""
        
        # --- HEADER ---
        self.header = tk.Frame(self.root, height=60)
        self.header.pack(fill="x")
        #titulo do aplicativo
        self.lbl_title = tk.Label(self.header, text=" Gemini AI Desktop Assistant", font=FONT_BOLD, fg="white")
        self.lbl_title.pack(side="left", padx=20, pady=15)
        #alterar tema
        self.btn_theme = tk.Button(self.header, text="🌓 Tema", command=self.toggle_theme, relief="flat")
        self.btn_theme.pack(side="right", padx=20)

        # --- BODY (Chat Area) ---
        self.chat_area = scrolledtext.ScrolledText(self.root, font=FONT_MAIN, state='disabled', wrap=tk.WORD)
        self.chat_area.pack(expand=True, fill="both", padx=10, pady=10)

        # --- FOOTER ---
        self.footer = tk.Frame(self.root, height=80)
        self.footer.pack(fill="x", side="bottom", padx=10, pady=10)
        #campo de entrada para mensagens
        self.entry_msg = tk.Entry(self.footer, font=FONT_MAIN, relief="flat")
        self.entry_msg.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.entry_msg.bind("<Return>", lambda e: self.start_send_thread()) # Envia com Enter
        #botão de enviar
        self.btn_send = tk.Button(self.footer, text="Enviar", font=FONT_BOLD, command=self.start_send_thread, relief="flat", cursor="hand2")
        self.btn_send.pack(side="right", ipadx=20, ipady=5)

    def apply_theme(self):
        """Aplica as cores do dicionário aos widgets"""
        theme = COLORS[self.current_theme]
        #configurações de cores para cada parte da interface
        self.root.configure(bg=theme["bg"])
        self.header.configure(bg=theme["header_bg"])
        self.lbl_title.configure(bg=theme["header_bg"])
        self.footer.configure(bg=theme["bg"])
        #cores do chat e entrada de mensagem
        self.chat_area.configure(bg=theme["bg"], fg=theme["text"], insertbackground=theme["text"])
        self.entry_msg.configure(bg=theme["bubble_ai"], fg=theme["text"])
        #cor dos botões
        self.btn_send.configure(bg=theme["btn_bg"], fg=theme["btn_fg"])
        self.btn_theme.configure(bg=theme["btn_bg"], fg=theme["btn_fg"])
        # Configuração das TAGS de cores usuario e bot
        self.chat_area.tag_configure("user_name", foreground=theme["name_user"], font=FONT_BOLD)
        self.chat_area.tag_configure("ai_name", foreground=theme["name_ai"], font=FONT_BOLD)
        self.chat_area.tag_configure("user_msg", background=theme["user_msg_bg"])
    #função para alternar entre temas claro e escuro
    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    def append_message(self, sender, message):
        self.chat_area.configure(state='normal')
        
        if sender == "Você":
            # Insere o nome com a cor do usuário
            self.chat_area.insert(tk.END, f"\n{sender}: ", "user_name")
            # Insere a mensagem com o fundo destacado
            self.chat_area.insert(tk.END, f"{message}\n", "user_msg")
        else:
            # Insere o nome do Gemini com a cor da IA
            self.chat_area.insert(tk.END, f"\n{sender}: ", "ai_name")
            # Insere a mensagem da IA com o texto padrão (sem destaque pesado)
            self.chat_area.insert(tk.END, f"{message}\n")

        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def start_send_thread(self):
        #Inicia a Thread para não travar a UI
        user_text = self.entry_msg.get().strip()
        if not user_text:
            return
        #mostra a mensagem do usuário imediatamente
        self.append_message("Você", user_text)
        self.entry_msg.delete(0, tk.END)
        
        # Criamos a thread para a IA pensar em segundo plano
        thread = threading.Thread(target=self.get_ai_response, args=(user_text,))
        thread.daemon = True
        thread.start()

    def get_ai_response(self, text):
        """Lógica que comunica com os servidores do Google"""
        try:
            # 1. Envia a mensagem para a API e espera resposta
            response = self.chat.send_message(text)
            
            # 2. Verifica se a resposta tem conteúdo (segurança)
            if response.text:
                # 3. Usa o 'after' para voltar para a thread principal e atualizar a tela
                self.root.after(0, self.append_message, "Gemini", response.text)
            else:
                self.root.after(0, self.append_message, "Erro", "A IA não gerou uma resposta válida.")

        except Exception as e:
            # Tratamento de erro com feedback pro usuario
            error_msg = f"Erro de conexão: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Falha na API", error_msg))
# Ponto de entrada do aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    app = GeminiChatApp(root)
    root.mainloop()
