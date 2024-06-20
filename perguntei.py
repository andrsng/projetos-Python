# ----------------------------------------------------------------------------
# Created By  : andrsng
# Created Date: 20/06/2024
# version = '1.0'
# ---------------------------------------------------------------------------
# Este programa utiliza como base a API do Gemini do Google. Foi desenvolvido por mim, com apoio de IA, quando eu precisava facilitar algumas pesquisas rapidas sem ter que acessar o navegador
# Ele me ajudou muito, e resolvi compartilhar o código para quem quiser testar.
# Para utilizar basta gerar uma API Key no link https://ai.google.dev/gemini-api/docs/api-key?hl=pt-br e utilizar a mesma na linha 17 entre as aspas de api_key=""
# Em Regras padrão na linha 26, você pode brincar e colocar uma regra para as respostas como o exemplo já inserido no código. Se não quiser, pode deixar apenas como default_regras = ""
# Em personalidade da IA criei algumas regras bem genéricas para dar um pouco de vida, linha 23, defina o nome, sexo e ação que quer que a ia faça. Sera repetido em todas as consultas, bem como no título.

import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import time

# Configuração da API key
genai.configure(api_key="SUA API KEY AQUI") #Exemplo AIsaSrBmytW79ka0dl0s3faWTIZbc80cL7df0eB

# Criar modelo da API GenerativeModel
model = genai.GenerativeModel('gemini-1.0-pro-latest')

#Personalidade da IA
nome = "Seu Francisco"
sexo = "masculino" #masculino, feminino
acao = "Fale como caipira e finja ser um caipira raiz, com gírias."

# Regras padrão
default_regras = (f"Regras de respostas: Apenas respostas curtas em português do Brasil. Seu nome é {nome}, do genero {sexo}. {acao}")
#default_regras = ""

# Inicializar a aplicação Tkinter
app = tk.Tk()
app.title("Perguntei - By andrsng")

# Widget para entrada de questões
tk.Label(app, text=f"Faça uma pergunta para {nome}:").pack()
question_textbox = scrolledtext.ScrolledText(app, width=60, height=10, wrap="word")
question_textbox.pack()

# Frame para os botões (alinhados horizontalmente)
button_frame = tk.Frame(app)
button_frame.pack(pady=10)

def obterRespostas_Gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro ao buscar resposta do Gemini: {e}")
        return "Erro. Refaça a questão que a API tem dessas." #Erro ao buscar resposta

def obterRespostas():
    pergunta = question_textbox.get("1.0", tk.END).strip()  # Remove extra spaces
    prompt = f"{default_regras} {pergunta}"  # Adicionar regras ao prompt
    resposta1 = obterRespostas_Gemini(prompt)

    results_textbox.delete("1.0", tk.END)  # Clear previous results
    results_textbox.tag_configure("estilo", foreground="green")
    results_textbox.insert(tk.END, f"{nome}: ", "estilo")
    # Simular máquina de escrever
    for char in resposta1:
        results_textbox.insert(tk.END, char)
        app.update()  # Atualizar a interface para mostrar o próximo caractere
        time.sleep(0.02)  # Atraso de 50ms entre cada caractere
    results_textbox.insert(tk.END, "\n")  # Adicionar quebra de linha no final

def limparCampos():
    question_textbox.delete("1.0", tk.END)
    results_textbox.delete("1.0", tk.END)

def consultaInicial():
    initial_query = ""
    response = obterRespostas_Gemini(f"{default_regras} {initial_query}")
    limparCampos()  # Limpar campos após a busca inicial

# Botão para obter respostas
tk.Button(button_frame, text="Obter respostas", command=obterRespostas).pack(side=tk.LEFT, padx=5)

# Botão para limpar campos
tk.Button(button_frame, text="Limpar", command=limparCampos).pack(side=tk.LEFT, padx=5)

# Label para exibir as respostas
tk.Label(app, text="Respostas:").pack()
results_textbox = scrolledtext.ScrolledText(app, width=60, height=10, wrap="word")
results_textbox.pack()
tk.Label(app, text="Criado por andrsng").pack()

# Chamada da busca inicial após a criação dos widgets necessários
consultaInicial()

# Iniciar o loop principal
app.mainloop()
