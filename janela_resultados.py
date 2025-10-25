import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import newmark
import bathe
import diferencascentrais

def funcao_janela_resultados(ndof, desloc, vel, acel, tempo, K, M, C, frequencias):

    def obter_dados_selecionados():
        tipo = combo_tipo.get()
        direcao = combo_dir.get()
        no = int(combo_no.get()) - 1

        idx = 2 * no + (0 if direcao == "X" else 1)
        if tipo == "Deslocamento":
            dados = desloc[:, idx]
        elif tipo == "Velocidade":
            dados = vel[:, idx]
        else:
            dados = acel[:, idx]
        return tipo, direcao, no, dados

    # ------------------- Funções dos botões -------------------
    def plotar():
        tipo, direcao, no, dados = obter_dados_selecionados()
        plt.figure()
        plt.plot(tempo, dados, label=f"{tipo} - Nó {no + 1} ({direcao})")
        plt.xlabel("Tempo (s)")
        if tipo == "Deslocamento":
            plt.ylabel("Deslocamento (m)")
        elif tipo == "Velocidade":
            plt.ylabel("Velocidade (m/s)")
        else:
            plt.ylabel("Aceleração (m/s²)")
        plt.title(f"{tipo} em {direcao} - Nó {no + 1}")
        plt.grid(True)
        plt.legend()
        plt.show()

    # def comparar_metodos():
    #         tipo, direcao, no, _ = obter_dados_selecionados()

    #         # Seleciona índice global (X=0, Y=1)
    #         idx = 2 * no + (0 if direcao == "X" else 1)

    #         # --- Executar os três métodos ---
    #         desloc_new, vel_new, acel_new = newmark.executar(K, M, C, cargas, apoios, dt, t_final, tipo_forca, params_forca)
    #         desloc_bat, vel_bat, acel_bat = bathe.executar(K, M, C, cargas, apoios, dt, t_final, tipo_forca, params_forca)
    #         desloc_dif, vel_dif, acel_dif = diferencascentrais.executar(K, M, C, cargas, apoios, dt, t_final, tipo_forca, params_forca)

    #         # Garantir mesmo tamanho de vetor tempo e deslocamento
    #         n = min(len(tempo), len(desloc_new))
    #         tempo_plot = tempo[:n]
    #         tempo_dif = tempo - dt/2

    
    #         # --- Plotar ---
    #         plt.figure()
    #         plt.plot(tempo_plot, desloc_new[:n, idx], label="Newmark")
    #         plt.plot(tempo_plot, desloc_dif[:n, idx], label="Diferenças Centrais")
    #         plt.plot(tempo_plot, desloc_bat[:n, idx], label="Bathe")

    #         plt.xlabel("Tempo (s)")
    #         plt.ylabel("Deslocamento (m)")
    #         plt.title(f"Comparação - Deslocamento {direcao} - Nó {no + 1}")
    #         plt.legend()
    #         plt.grid(True)
    #         plt.show()

    #         plt.figure()
    #         plt.plot(tempo_plot, vel_new[:n, idx], label="Newmark")
    #         plt.plot(tempo_plot, vel_dif[:n, idx], label="Diferenças Centrais")
    #         plt.plot(tempo_plot, vel_bat[:n, idx], label="Bathe")

    #         plt.xlabel("Tempo (s)")
    #         plt.ylabel("Velocidade (m/s)")
    #         plt.title(f"Comparação - Velocidade {direcao} - Nó {no + 1}")
    #         plt.legend()
    #         plt.grid(True)
    #         plt.show()

    #         plt.figure()
    #         plt.plot(tempo_plot, acel_new[:n, idx], label="Newmark")
    #         plt.plot(tempo_plot, acel_dif[:n, idx], label="Diferenças Centrais")
    #         plt.plot(tempo_plot, acel_bat[:n, idx], label="Bathe")

    #         plt.xlabel("Tempo (s)")
    #         plt.ylabel("Aceleração (m/s²)")
    #         plt.title(f"Comparação - Aceleração {direcao} - Nó {no + 1}")
    #         plt.legend()
    #         plt.grid(True)
    #         plt.show()

    def mostrar_valores():
        tipo, direcao, no, dados = obter_dados_selecionados()

        janela_valores = tk.Toplevel(janela_plot)
        janela_valores.title(f"{tipo} - Nó {no+1} ({direcao})")
        janela_valores.geometry("460x420")

        texto = tk.Text(janela_valores, wrap="none", font=("Courier", 10))
        texto.pack(fill=tk.BOTH, expand=True)

        texto.insert(tk.END, f"{'Tempo (s)':>12} | {tipo:>15}\n")
        texto.insert(tk.END, "-" * 30 + "\n")

        for t, val in zip(tempo, dados):
            texto.insert(tk.END, f"{t:12.6f} | {val:15.6e}\n")

        texto.config(state=tk.DISABLED)

    def ver_matrizes():
        janela_matrizes = tk.Toplevel(janela_plot)
        janela_matrizes.title("Matrizes de Rigidez, Massa e Amortecimento")
        janela_matrizes.geometry("700x500")

        texto = tk.Text(janela_matrizes, wrap="none", font=("Courier", 10))
        texto.pack(fill=tk.BOTH, expand=True)

        def formatar_matriz(nome, matriz):
            texto.insert(tk.END, f"{nome}:\n")
            for linha in matriz:
                texto.insert(tk.END, " ".join(f"{v:10.3e}" for v in linha) + "\n")
            texto.insert(tk.END, "\n")

        formatar_matriz("Matriz de Rigidez (K)", K)
        formatar_matriz("Matriz de Massa (M)", M)
        if C is not None:
            formatar_matriz("Matriz de Amortecimento (C)", C)
        else:
            texto.insert(tk.END, "Amortecimento não utilizado.\n")

        texto.config(state=tk.DISABLED)

    def ver_frequencias():
        janela_freq = tk.Toplevel(janela_plot)
        janela_freq.title("Frequências Naturais")
        janela_freq.geometry("400x300")

        texto = tk.Text(janela_freq, wrap="none", font=("Courier", 10))
        texto.pack(fill=tk.BOTH, expand=True)

        texto.insert(tk.END, f"{'Modo':>5} | {'ω (rad/s)':>12} | {'f (Hz)':>10}\n")
        texto.insert(tk.END, "-" * 35 + "\n")

        try:
            for i, (omega, freq) in enumerate(frequencias, start=1):
                texto.insert(tk.END, f"{i:5d} | {omega:12.3f} | {freq:10.3f}\n")
        except Exception as e:
            texto.insert(tk.END, f"Erro ao exibir frequências:\n{e}\n")

        texto.config(state=tk.DISABLED)

    # ------------------- Janela principal -------------------
    janela_plot = tk.Tk()
    janela_plot.title("Visualização de Resultados")
    janela_plot.geometry("420x290")

    tk.Label(janela_plot, text="Tipo de resultado:").pack(pady=3)
    combo_tipo = ttk.Combobox(janela_plot, values=["Deslocamento", "Velocidade", "Aceleração"])
    combo_tipo.current(0)
    combo_tipo.pack()

    tk.Label(janela_plot, text="Direção:").pack(pady=3)
    combo_dir = ttk.Combobox(janela_plot, values=["X", "Y"])
    combo_dir.current(0)
    combo_dir.pack()

    tk.Label(janela_plot, text="Nó:").pack(pady=3)
    num_nos = ndof // 2
    combo_no = ttk.Combobox(janela_plot, values=[str(i+1) for i in range(num_nos)])
    combo_no.current(0)
    combo_no.pack()

    frame_botoes = tk.Frame(janela_plot)
    frame_botoes.pack(pady=15)

    tk.Button(frame_botoes, text="Plotar", command=plotar, bg="lightblue", width=10).grid(row=0, column=0, padx=5, pady=3)
    tk.Button(frame_botoes, text="Mostrar Valores", command=mostrar_valores, bg="lightgreen", width=15).grid(row=0, column=1, padx=5, pady=3)
    tk.Button(frame_botoes, text="Ver Matrizes", command=ver_matrizes, bg="khaki", width=12).grid(row=1, column=0, padx=5, pady=3)
    tk.Button(frame_botoes, text="Ver Frequências", command=ver_frequencias, bg="plum", width=15).grid(row=1, column=1, padx=5, pady=3)
    # tk.Button(frame_botoes, text="Comparar Métodos", command=comparar_metodos, bg="lightcoral", width=15).grid(row=2, column=0, columnspan=2, pady=5)

    janela_plot.mainloop()