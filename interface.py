import tkinter as tk
from tkinter import messagebox, Toplevel
import numpy as np
import gerar_matrizes
import janela_resultados

np.set_printoptions(suppress=True)

# ---------------------------
# Variáveis globais (iniciam vazias)
# ---------------------------
coordenadas = []   # numpy array após preenchimento
incidencia = []    # numpy array após preenchimento (nó1, nó2, material_index (1-based))
dados_elem = []    # numpy array após preenchimento (A, E, rho)
apoios = []        # numpy array após preenchimento (no, rx, ry)
cargas = []        # numpy array após preenchimento (no, Fx, Fy)

# ---------------------------
# Funções de janelas de entrada
# ---------------------------

def abrir_janela_nos():
    try:
        num_nos = int(entrada_num_nos.get())
        if num_nos <= 0:
            raise ValueError
    except Exception:
        messagebox.showwarning("Aviso", "Digite um número válido e positivo de nós.")
        return

    janela_nos = Toplevel(janela)
    janela_nos.title("Coordenadas dos Nós")
    janela_nos.geometry(f"300x{60 + num_nos * 30}")
    tk.Label(janela_nos, text="Insira as coordenadas (x, y) de cada nó:").pack(pady=5)

    entradas = []
    for i in range(num_nos):
        frame = tk.Frame(janela_nos)
        frame.pack(pady=2)
        tk.Label(frame, text=f"Nó {i+1} (x, y):").pack(side=tk.LEFT)
        entrada_x = tk.Entry(frame, width=7); entrada_x.pack(side=tk.LEFT, padx=2)
        entrada_y = tk.Entry(frame, width=7); entrada_y.pack(side=tk.LEFT, padx=2)
        entradas.append((entrada_x, entrada_y))

    def salvar():
        global coordenadas
        try:
            coords = []
            for ex, ey in entradas:
                x = float(ex.get())
                y = float(ey.get())
                coords.append([x, y])
            coordenadas = np.array(coords)
            messagebox.showinfo("Sucesso", "Coordenadas salvas com sucesso.")
            janela_nos.destroy()
        except Exception:
            messagebox.showwarning("Erro", "Digite apenas números válidos para as coordenadas.")

    tk.Button(janela_nos, text="Salvar", command=salvar).pack(pady=10)


def abrir_janela_incidencia():
    try:
        num_elem = int(entrada_num_elem.get())
        if num_elem <= 0:
            raise ValueError
    except Exception:
        messagebox.showwarning("Aviso", "Digite um número válido e positivo de elementos.")
        return

    janela_incidencia = Toplevel(janela)
    janela_incidencia.title("Matriz de Incidência")
    janela_incidencia.geometry(f"350x{80 + num_elem * 30}")
    tk.Label(janela_incidencia, text="Digite (nó 1, nó 2, índice do material) para cada elemento:").pack(pady=5)

    entradas = []
    for i in range(num_elem):
        frame = tk.Frame(janela_incidencia)
        frame.pack(pady=2)
        tk.Label(frame, text=f"Elemento {i+1}:").pack(side=tk.LEFT)
        e1 = tk.Entry(frame, width=6); e1.pack(side=tk.LEFT, padx=2)
        e2 = tk.Entry(frame, width=6); e2.pack(side=tk.LEFT, padx=2)
        e3 = tk.Entry(frame, width=6); e3.pack(side=tk.LEFT, padx=2)
        entradas.append((e1, e2, e3))

    def salvar():
        global incidencia
        try:
            inc = []
            for e1, e2, e3 in entradas:
                n1 = int(e1.get())
                n2 = int(e2.get())
                mat = int(e3.get())
                inc.append([n1, n2, mat])
            incidencia = np.array(inc, dtype=int)
            messagebox.showinfo("Sucesso", "Matriz de incidência salva com sucesso.")
            janela_incidencia.destroy()
        except Exception:
            messagebox.showwarning("Erro", "Digite apenas números inteiros válidos para a incidência.")

    tk.Button(janela_incidencia, text="Salvar", command=salvar).pack(pady=10)


def abrir_janela_cargas():
    try:
        num_nos_carga = int(entrada_num_cargas.get())
        if num_nos_carga < 0:
            raise ValueError
    except Exception:
        messagebox.showwarning("Aviso", "Digite um número válido de nós com carga (0 ou mais).")
        return

    janela_cargas = Toplevel(janela)
    janela_cargas.title("Cargas aplicadas")
    janela_cargas.geometry(f"360x{80 + num_nos_carga * 30}")
    tk.Label(janela_cargas, text="Digite o nó e as cargas (Fx, Fy) em N:").pack(pady=5)

    entradas = []
    for i in range(num_nos_carga):
        frame = tk.Frame(janela_cargas)
        frame.pack(pady=2)
        tk.Label(frame, text=f"Entrada {i+1} - Nó:").pack(side=tk.LEFT)
        e_node = tk.Entry(frame, width=6); e_node.pack(side=tk.LEFT, padx=2)
        tk.Label(frame, text=" Fx:").pack(side=tk.LEFT)
        e_fx = tk.Entry(frame, width=8); e_fx.pack(side=tk.LEFT, padx=2)
        tk.Label(frame, text=" Fy:").pack(side=tk.LEFT)
        e_fy = tk.Entry(frame, width=8); e_fy.pack(side=tk.LEFT, padx=2)
        entradas.append((e_node, e_fx, e_fy))

    def salvar():
        global cargas
        try:
            cgs = []
            for enode, efx, efy in entradas:
                n = int(enode.get())
                fx = float(efx.get())
                fy = float(efy.get())
                cgs.append([n, fx, fy])
            cargas = np.array(cgs, dtype=float)
            messagebox.showinfo("Sucesso", "Cargas salvas com sucesso.")
            janela_cargas.destroy()
        except Exception:
            messagebox.showwarning("Erro", "Digite apenas números válidos para as cargas (nó inteiro, forças numéricas).")

    tk.Button(janela_cargas, text="Salvar", command=salvar).pack(pady=10)


def abrir_janela_apoios():
    try:
        num_apoios = int(entrada_num_apoios.get())
        if num_apoios < 0:
            raise ValueError
    except Exception:
        messagebox.showwarning("Aviso", "Digite um número válido de nós com apoio (0 ou mais).")
        return

    janela_apoios = Toplevel(janela)
    janela_apoios.title("Apoios")
    janela_apoios.geometry(f"380x{80 + num_apoios * 40}")
    tk.Label(janela_apoios, text="Digite o nó e marque graus de liberdade restringidos:").pack(pady=5)

    entradas = []
    for i in range(num_apoios):
        frame = tk.Frame(janela_apoios)
        frame.pack(pady=2)
        tk.Label(frame, text=f"Apoio {i+1} - Nó:").pack(side=tk.LEFT)
        e_node = tk.Entry(frame, width=6); e_node.pack(side=tk.LEFT, padx=2)
        var_x = tk.IntVar(); var_y = tk.IntVar()
        tk.Checkbutton(frame, text="X", variable=var_x).pack(side=tk.LEFT, padx=6)
        tk.Checkbutton(frame, text="Y", variable=var_y).pack(side=tk.LEFT, padx=6)
        entradas.append((e_node, var_x, var_y))

    def salvar():
        global apoios
        try:
            aps = []
            for enode, vx, vy in entradas:
                n = int(enode.get())
                aps.append([n, int(vx.get()), int(vy.get())])
            apoios = np.array(aps, dtype=int)
            messagebox.showinfo("Sucesso", "Apoios salvos com sucesso.")
            janela_apoios.destroy()
        except Exception:
            messagebox.showwarning("Erro", "Digite apenas números inteiros válidos para os nós dos apoios.")

    tk.Button(janela_apoios, text="Salvar", command=salvar).pack(pady=10)


def abrir_janela_materiais():
    try:
        num_mat = int(entrada_num_mat.get())
        if num_mat <= 0:
            raise ValueError
    except Exception:
        messagebox.showwarning("Aviso", "Digite uma quantidade válida e positiva de materiais.")
        return

    janela_mat = Toplevel(janela)
    janela_mat.title("Materiais")
    janela_mat.geometry(f"420x{90 + num_mat * 30}")
    tk.Label(janela_mat, text="Digite os dados (A [m²], E [N/m²], ρ [kg/m³]) para cada material:").pack(pady=5)

    entradas = []
    for i in range(num_mat):
        frame = tk.Frame(janela_mat)
        frame.pack(pady=2)
        tk.Label(frame, text=f"Material {i+1}:").pack(side=tk.LEFT)
        eA = tk.Entry(frame, width=8); eA.pack(side=tk.LEFT, padx=2)
        eE = tk.Entry(frame, width=12); eE.pack(side=tk.LEFT, padx=2)
        erho = tk.Entry(frame, width=8); erho.pack(side=tk.LEFT, padx=2)
        entradas.append((eA, eE, erho))

    def salvar():
        global dados_elem
        try:
            mats = []
            for ea, eE, erho in entradas:
                A = float(ea.get())
                E = float(eE.get())
                rho = float(erho.get())
                mats.append([A, E, rho])
            dados_elem = np.array(mats, dtype=float)
            messagebox.showinfo("Sucesso", "Dados dos materiais salvos com sucesso.")
            janela_mat.destroy()
        except Exception:
            messagebox.showwarning("Erro", "Digite apenas números válidos para A, E e ρ.")

    tk.Button(janela_mat, text="Salvar", command=salvar).pack(pady=10)


# ---------------------------
# Função utilitária para construir matriz de materiais usada pelos elementos
# ---------------------------
def construir_matriz_materiais():
    if len(incidencia) == 0 or len(dados_elem) == 0:
        messagebox.showerror("Erro", "Incidência ou materiais não definidos.")
        return None
    try:
        ordem = [int(e[2]) - 1 for e in incidencia]  # espera material index 1-based
        mats = [dados_elem[i] for i in ordem]
        return np.array(mats, dtype=float)
    except Exception:
        messagebox.showerror("Erro", "Falha ao construir matriz de materiais. Verifique índices de materiais na incidência.")
        return None


# ---------------------------
# Função principal de execução (checa entradas e chama rotinas)
# ---------------------------
def resultado_gerar_matrizes():
    try:
        # Verifica campos numéricos principais
        campos = {
            "Número de materiais": entrada_num_mat.get(),
            "Número de nós": entrada_num_nos.get(),
            "Número de elementos": entrada_num_elem.get(),
            "Número de nós com carga": entrada_num_cargas.get(),
            "Número de apoios": entrada_num_apoios.get(),
            "Δt": entrada_delta_t.get(),
            "Tempo final": entrada_tempo_final.get()
        }
        for nome, valor in campos.items():
            if valor is None or str(valor).strip() == "":
                messagebox.showwarning("Aviso", f"Preencha o campo: {nome}.")
                return

        # Converte e valida alguns valores básicos
        try:
            num_mat = int(entrada_num_mat.get())
            num_nos = int(entrada_num_nos.get())
            num_elem = int(entrada_num_elem.get())
            num_cargas = int(entrada_num_cargas.get())
            num_apoios = int(entrada_num_apoios.get())
            dt = float(entrada_delta_t.get())
            t_final = float(entrada_tempo_final.get())
        except Exception:
            messagebox.showwarning("Aviso", "Alguns campos numéricos estão inválidos. Verifique os valores.")
            return

        # Verificações de consistência dos dados carregados pelas janelas
        erros = []
        if len(coordenadas) == 0:
            erros.append("Coordenadas não foram inseridas.")
        else:
            if coordenadas.shape[0] != num_nos:
                erros.append(f"Número de coordenadas ({coordenadas.shape[0]}) difere do número de nós ({num_nos}).")

        if len(incidencia) == 0:
            erros.append("Matriz de incidência não foi inserida.")
        else:
            if incidencia.shape[0] != num_elem:
                erros.append(f"Número de elementos na incidência ({incidencia.shape[0]}) difere do informado ({num_elem}).")

        if len(dados_elem) == 0:
            erros.append("Dados dos materiais não foram inseridos.")
        else:
            if dados_elem.shape[0] != num_mat:
                erros.append(f"Número de materiais inseridos ({dados_elem.shape[0]}) difere do informado ({num_mat}).")

        if len(apoios) == 0:
            erros.append("Apoios não foram inseridos.")
        if len(cargas) == 0:
            erros.append("Cargas não foram inseridas.")

        if dt <= 0 or t_final <= 0:
            erros.append("Δt e Tempo final devem ser maiores que zero.")
        if t_final <= dt:
            erros.append("Tempo final deve ser maior que Δt.")

        if erros:
            messagebox.showwarning("Aviso - Dados incompletos/consistentes", "\n".join(erros))
            return

        # Construir matriz de materiais por elemento
        materiais = construir_matriz_materiais()
        if materiais is None:
            return

        # Chama rotina externa para montar matrizes
        K, M, frequencias, C = gerar_matrizes.gerar_matrizes_trelica(
            num_nos=num_nos,
            num_elem=num_elem,
            coordenadas=coordenadas,
            incidencia=incidencia,
            materiais=materiais,
            cargas=cargas,
            apoios=apoios,
            usar_amortecimento=usar_amortecimento.get())

        # Parâmetros para integração temporal
        metodo = metodo_integracao.get()
        funcao = funcao_temporal.get()
        params_forca = {
            "amplitude": amplitude_valor.get(),
            "ti": ti_valor.get(),
            "tf": tf_valor.get(),
            "omega": omega_valor.get(),
            "phi": phi_valor.get()}

        # Chama o integrador escolhido (presume-se que os módulos existam)
        if metodo == "newmark":
            import newmark
            desloc, vel, acel = newmark.executar(K, M, C, cargas, apoios, dt, t_final, funcao, params_forca=params_forca)
        elif metodo == "bathe":
            import bathe
            desloc, vel, acel = bathe.executar(K, M, C, cargas, apoios, dt, t_final, funcao, params_forca=params_forca)
        elif metodo == "diferencas":
            import diferencascentrais
            desloc, vel, acel = diferencascentrais.executar(K, M, C, cargas, apoios, dt, t_final, funcao, params_forca=params_forca)
        else:
            messagebox.showerror("Erro", "Método de integração desconhecido.")
            return

        # Envia resultados para a janela de resultados (presume-se assinatura compatível)
        janela_resultados.funcao_janela_resultados(
            ndof=K.shape[0],
            desloc=desloc,
            vel=vel,
            acel=acel,
            tempo=np.arange(0, t_final + dt, dt),
            K=K,
            M=M,
            C=C,
            frequencias=frequencias)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante a execução:\n{e}")

# ---------------------------
# Interface Principal
# ---------------------------
janela = tk.Tk()
janela.title("Análise Dinâmica de Treliça")
janela.geometry("500x480")

# Variáveis para função temporal / amortecimento
ti_valor = tk.DoubleVar(value=0.0)
tf_valor = tk.DoubleVar(value=0.0)
amplitude_valor = tk.DoubleVar(value=0.0)
omega_valor = tk.DoubleVar(value=0.0)
phi_valor = tk.DoubleVar(value=0.0)
usar_amortecimento = tk.BooleanVar(value=False)

# Labels e entradas principais
tk.Label(janela, text="Número de materiais:").place(x=20, y=20)
entrada_num_mat = tk.Entry(janela); entrada_num_mat.place(x=160, y=20)

tk.Label(janela, text="Número de nós:").place(x=20, y=60)
entrada_num_nos = tk.Entry(janela); entrada_num_nos.place(x=160, y=60)

tk.Label(janela, text="Número de elementos:").place(x=20, y=100)
entrada_num_elem = tk.Entry(janela); entrada_num_elem.place(x=160, y=100)

tk.Checkbutton(janela, text="Usar amortecimento de Rayleigh", variable=usar_amortecimento).place(x=20, y=135)

tk.Label(janela, text="Número de nós \ncom carga:").place(x=20, y=175)
entrada_num_cargas = tk.Entry(janela); entrada_num_cargas.place(x=160, y=182)

tk.Label(janela, text="Número de apoios:").place(x=20, y=225)
entrada_num_apoios = tk.Entry(janela); entrada_num_apoios.place(x=160, y=225)

tk.Label(janela, text="Método de integração no tempo:").place(x=20, y=270)

tk.Label(janela, text="Intervalo de tempo (s):").place(x=20, y=305)
entrada_delta_t = tk.Entry(janela); entrada_delta_t.place(x=160, y=305)

tk.Label(janela, text="Tempo final (s):").place(x=20, y=340)
entrada_tempo_final = tk.Entry(janela); entrada_tempo_final.place(x=160, y=340)

tk.Label(janela, text="Função temporal:").place(x=20, y=375)

# Botões para abrir janelas
tk.Button(janela, text="Registrar materiais", command=abrir_janela_materiais).place(x=320, y=17)
tk.Button(janela, text="Inserir coordenadas", command=abrir_janela_nos).place(x=320, y=57)
tk.Button(janela, text="Inserir incidência", command=abrir_janela_incidencia).place(x=320, y=97)
tk.Button(janela, text="Inserir cargas", command=abrir_janela_cargas).place(x=320, y=180)
tk.Button(janela, text="Inserir apoios", command=abrir_janela_apoios).place(x=320, y=222)

# Método de integração
metodo_integracao = tk.StringVar(value="newmark")

def abrir_janela_metodo():
    janela_metodo = Toplevel(janela)
    janela_metodo.title("Escolher Método de Integração")
    janela_metodo.geometry("300x180")
    tk.Label(janela_metodo, text="Selecione o método de integração no tempo:").pack(pady=10)
    tk.Radiobutton(janela_metodo, text="Newmark", variable=metodo_integracao, value="newmark").pack(anchor="w", padx=20)
    tk.Radiobutton(janela_metodo, text="Bathe", variable=metodo_integracao, value="bathe").pack(anchor="w", padx=20)
    tk.Radiobutton(janela_metodo, text="Diferenças Centrais", variable=metodo_integracao, value="diferencas").pack(anchor="w", padx=20)
    tk.Button(janela_metodo, text="OK", command=janela_metodo.destroy).pack(pady=10)

tk.Button(janela, text="Escolher Método", command=abrir_janela_metodo).place(x=320, y=269)

# Função temporal
funcao_temporal = tk.StringVar(value="rampa")

def abrir_janela_funcao_temporal():
    janela_funcao = Toplevel(janela)
    janela_funcao.title("Escolher Função Temporal")
    janela_funcao.geometry("360x320")
    tk.Label(janela_funcao, text="Selecione a função temporal:").pack(pady=10)
    tk.Radiobutton(janela_funcao, text="Constante", variable=funcao_temporal , value="constante").pack(anchor="w", padx=20)
    tk.Radiobutton(janela_funcao, text="Rampa", variable=funcao_temporal, value="rampa").pack(anchor="w", padx=20)
    tk.Radiobutton(janela_funcao, text="Harmônica", variable=funcao_temporal, value="harmonico").pack(anchor="w", padx=20)

    frame_tempos = tk.Frame(janela_funcao)
    frame_tempos.pack(pady=10)

    tk.Label(frame_tempos, text="Tempo inicial (s)").pack(side="left", padx=5)
    ti_entry = tk.Entry(frame_tempos, width=8); ti_entry.insert(0, str(ti_valor.get())); ti_entry.pack(side="left", padx=5)
    tk.Label(frame_tempos, text="Tempo final (s)").pack(side="left", padx=5)
    tf_entry = tk.Entry(frame_tempos, width=8); tf_entry.insert(0, str(tf_valor.get())); tf_entry.pack(side="left", padx=5)

    tk.Label(janela_funcao, text="Amplitude").pack(anchor="w", padx=20)
    amplitude_entry = tk.Entry(janela_funcao); amplitude_entry.insert(0, str(amplitude_valor.get())); amplitude_entry.pack(anchor="w", padx=20)

    tk.Label(janela_funcao, text="Frequência ω (rad/s)").pack(anchor="w", padx=20)
    omega_entry = tk.Entry(janela_funcao); omega_entry.insert(0, str(omega_valor.get())); omega_entry.pack(anchor="w", padx=20)

    tk.Label(janela_funcao, text="Fase φ (rad)").pack(anchor="w", padx=20)
    phi_entry = tk.Entry(janela_funcao); phi_entry.insert(0, str(phi_valor.get())); phi_entry.pack(anchor="w", padx=20)

    def salvar():
        try:
            ti_valor.set(float(ti_entry.get()))
            tf_valor.set(float(tf_entry.get()))
            amplitude_valor.set(float(amplitude_entry.get()))
            omega_valor.set(float(omega_entry.get()))
            phi_valor.set(float(phi_entry.get()))
            janela_funcao.destroy()
        except Exception:
            messagebox.showwarning("Erro", "Digite valores numéricos válidos para ti, tf, amplitude, ω e φ.")

    tk.Button(janela_funcao, text="OK", command=salvar).pack(pady=10)

tk.Button(janela, text="Escolher Função", command=abrir_janela_funcao_temporal).place(x=320, y=375)

# Botão executar
tk.Button(
    janela,
    text="Executar",
    command=resultado_gerar_matrizes,
    bg="lightblue",
    font=("Arial", 10, "bold"),
    width=15,
    height=2
).place(x=175, y=420)

# Inicia interface
if __name__ == "__main__":
    janela.mainloop()