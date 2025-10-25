"""
Arquivo auxiliar para geração de matrizes de rigidez, massa e amortecimento.
"""

from scipy.linalg import eigh

def gerar_matrizes_trelica(num_nos, num_elem, coordenadas, incidencia, materiais, cargas, apoios, usar_amortecimento=False):
    import numpy as np
    import matplotlib.pyplot as plt
    np.set_printoptions(suppress=True)

    # Ajuste para permitir nós numerados a partir de 1
    # (se os números de nós da incidência, cargas e apoios começarem em 1)
    if np.min(incidencia[:, :2]) >= 1:
        incidencia = incidencia.copy()
        incidencia[:, :2] -= 1  # transforma em base 0

    if np.min(cargas[:, 0]) >= 1:
        cargas = cargas.copy()
        cargas[:, 0] -= 1

    if np.min(apoios[:, 0]) >= 1:
        apoios = apoios.copy()
        apoios[:, 0] -= 1
    
    # =========================
    # ENTRADA DE DADOS
    # =========================

    def calcular_sen_cos_comp(x1, x2, y1, y2):
        ''' Calcula o seno, cosseno e comprimento dos elementos da estrutrura.
        Entradas:
            * x1, x2, y1, y2
        Saídas:
            * sen, cos, comp
        '''
        comp = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        sen = (y2 - y1)/comp
        cos = (x2 - x1)/comp
        
        return float(sen), float(cos), float(comp)
    
    coord = coordenadas

    nx = np.transpose(coord[:num_nos, :1])
    ny = np.transpose(coord[:num_nos, 1:])
    plt.scatter(nx, ny, color='red')
    for i in range(num_elem):
        x = np.array([coord[incidencia[i, 0], 0], coord[incidencia[i, 1], 0]])
        y = np.array([coord[incidencia[i, 0], 1], coord[incidencia[i, 1], 1]])
        plt.plot(x, y)
    plt.title("Treliça")

    plt.show()

    def calcular_sen_cos_comp(x1, x2, y1, y2):
        ''' Calcula o seno, cosseno e comprimento dos elementos da estrutrura.
        Entradas:
            * x1, x2, y1, y2
        Saídas:
            * sen, cos, comp
        '''
        comp = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        sen = (y2 - y1)/comp
        cos = (x2 - x1)/comp
        
        return float(sen), float(cos), float(comp)

    senos = []
    cossenos = []
    comprimentos = []

    # Loop para calcular os senos, cossenos e comprimentos dos elementos:
    for elem in range(num_elem):
        no1 = int(incidencia[elem, 0])
        no2 = int(incidencia[elem, 1])
        
        coord_x1 = float(coord[no1][0])
        coord_x2 = float(coord[no2][0])
        coord_y1 = float(coord[no1][1])
        coord_y2 = float(coord[no2][1])
        
        sen_elem, cos_elem, comp_elem = calcular_sen_cos_comp(coord_x1, coord_x2, coord_y1, coord_y2)
        
        senos.append(sen_elem)
        cossenos.append(cos_elem)
        comprimentos.append(comp_elem)

    # Matriz de Rigidez Global da Estrutura:
    '''
    Lembrando que:
        * sistema local: (r, s)
        * sistema global: (X, Y)
    '''
    k_elem_global_geral = np.zeros((2*num_nos, 2*num_nos))
    m_elem_global_geral = np.zeros((2*num_nos, 2*num_nos))

    for i in range(num_elem):
        no1 = int(incidencia[i, 0])
        no2 = int(incidencia[i, 1])
 
        A_elem = materiais[i, 0]
        E_elem = materiais[i, 1]
        rho_elem = materiais[i, 2]
        L_elem = comprimentos[i]
        
        # Matriz de Rigidez Local do Elemento:
        k_elem_local = (E_elem*A_elem/L_elem) * np.array([[1., -1.],
                                                        [-1., 1.]])
        
        # Matriz de Rigidez Global do Elemento (k_elem_global0):
        sen = senos[i]
        cos = cossenos[i]

        matriz_transp = np.array([[cos, sen,   0,   0],
                                  [  0,   0, cos, sen]])
        k_elem_global = np.dot(np.transpose(matriz_transp), k_elem_local)
        k_elem_global = np.dot(k_elem_global, matriz_transp)

    # Matriz de Rigidez Local do Elemento:
        k_elem_local = (E_elem*A_elem/L_elem) * np.array([[1.,  0., -1., 0.],
                                                          [0.,  0.,  0., 0.],
                                                          [-1., 0.,  1., 0.],
                                                          [0.,  0.,  0., 0.]])

        # Considera massa nas 2 direções (para dar o resultado que dava antes, teria que zerar a segunda e a quarta lihas).
        m_elem_local = (A_elem*rho_elem*L_elem/6.) * np.array([[2.,  0.,  1., 0.],
                                                               [0.,  2.,  0., 1.],
                                                               [1.,  0.,  2., 0.],
                                                               [0.,  1.,  0., 2.]])

        # Matriz de Rigidez Global do Elemento (k_elem_global0):
        sen = senos[i]
        cos = cossenos[i]

        T = np.array([[ cos,  sen,   0,    0],
                      [-sen,  cos,   0,    0],
                      [  0,    0,  cos,  sen],
                      [  0,    0, -sen,  cos]])

        k_elem_global = T.T @ k_elem_local @ T
        m_elem_global = T.T @ m_elem_local @ T

        # Lista de posição dos Graus de Liberdade
        posicao = [2*no1, 2*no1+1, 2*no2, 2*no2+1]

        for j in range(4): 
            for k in range(4):
                k_elem_global_geral[posicao[j], posicao[k]] = k_elem_global_geral[posicao[j], posicao[k]] + k_elem_global[j, k]
                m_elem_global_geral[posicao[j], posicao[k]] = m_elem_global_geral[posicao[j], posicao[k]] + m_elem_global[j, k]

    # Vetor de Froças Global:
    Fg = np.zeros((2*num_nos, 1))

    for i in range(cargas.shape[0]): 
        no = int(cargas[i, 0])  
        gl1 = 2*no
        gl2 = 2*no + 1

        Fg[gl1, 0] = cargas[i, 1]
        Fg[gl2, 0] = cargas[i, 2]

    # inicializa listas
    livres = []
    restritos = []
    num_cond_contorno = 0

    # percorre todos os nós
    for no in range(num_nos):
        glx = 2*no
        gly = 2*no + 1
        
        # verifica se este nó está na lista de apoios
        restricao = next((a for a in apoios if a[0] == no), None)
        
        if restricao is None:  # nó sem apoio => livres
            livres.extend([glx, gly])
        else:
            # X
            if restricao[1] == 0:
                livres.append(glx)
            else:
                restritos.append(glx)
                num_cond_contorno += 1
            # Y
            if restricao[2] == 0:
                livres.append(gly)
            else:
                restritos.append(gly)
                num_cond_contorno += 1

    # --- Cálculo das frequências naturais ---

    # Montar lista de GL restritos e livres 
    ndof = 2*num_nos
    todos_gdls = list(range(ndof))
    livres = [g for g in todos_gdls if g not in restritos]

    # Reduzir matrizes
    K_red = k_elem_global_geral[np.ix_(livres, livres)]
    M_red = m_elem_global_geral[np.ix_(livres, livres)]

    # Resolver autovalores (generalized eigenproblem: K phi = lambda M phi)
    eigvals, eigvecs = eigh(K_red, M_red)

    # proteger contra valores negativos numéricos
    eigvals_pos = np.where(eigvals > 0, eigvals, 0.0)
    omegas = np.sqrt(eigvals_pos)  # rad/s
    freqs_hz = omegas / (2*np.pi)

    # ordenar por frequência crescente
    order = np.argsort(omegas)
    omegas = omegas[order]
    freqs_hz = freqs_hz[order]

    # filtro para eliminar modos com frequência próxima de zero (rigid body)
    tol_omega = 1e-8
    modos_validos = np.where(omegas > tol_omega)[0]

    if len(modos_validos) == 0:
        # nenhum modo significativo encontrado
        frequencias = []
    else:
        # Retornar TODAS as frequências não-nulas (ou troque aqui se quiser limitar)
        frequencias = [(float(omegas[i]), float(freqs_hz[i])) for i in range(len(omegas))]

    # ---------------------------
    # CÁLCULO DO AMORTECIMENTO DE RAYLEIGH (mais robusto)
    # ---------------------------
    def rayleigh_damping(K, M, omegas, modos_escolhidos=None, zeta_vals=None):
        """
        Monta C = alpha*M + beta*K determinando alpha e beta a partir de dois modos.
        - modos_escolhidos: lista/tupla com dois índices de modos em 'omegas' (relativos a omegas)
                             se None -> usa os dois primeiros modos não-nulos
        - zeta_vals: (zeta_i, zeta_j) em razão crítica (ex.: 0.02)
        """
        # achar modos não-nulos
        tol = 1e-8
        modos_validos = [i for i, w in enumerate(omegas) if w > tol]
        if len(modos_validos) < 2:
            raise ValueError("Não há modos não-nulos suficientes para calcular amortecimento de Rayleigh.")

        if modos_escolhidos is None:
            modo_i = modos_validos[0]
            modo_j = modos_validos[1]
        else:
            modo_i, modo_j = modos_escolhidos

        if zeta_vals is None:
            zeta_i = zeta_j = 0.02
        else:
            zeta_i, zeta_j = zeta_vals

        wi = float(omegas[modo_i])
        wj = float(omegas[modo_j])

        # resolver o sistema:
        # alpha/(2 wi) + beta*(wi/2) = zeta_i
        # alpha/(2 wj) + beta*(wj/2) = zeta_j
        denom = (wi**2 - wj**2)
        if abs(denom) < 1e-12:
            raise ValueError("Modos muito próximos entre si; escolha outros modos para Rayleigh.")

        alpha = (2*wi**2*wj*zeta_j - 2*wi*wj**2*zeta_i) / (wi**2 - wj**2)
        beta  = (2*wi*zeta_i - 2*wj*zeta_j) / (wi**2 - wj**2)

        C = alpha * M + beta * K

        print('alpha')
        print(alpha)
        print(beta)
        print(beta)
        return C, alpha, beta, modo_i, modo_j

    if usar_amortecimento:
        # usa os dois primeiros modos NÃO-NULOS por padrão, e zeta = 2% em ambos
        try:
            C_red, alpha, beta, mi, mj = rayleigh_damping(K_red, M_red, omegas, modos_escolhidos=None, zeta_vals=(0.02, 0.02))
        except Exception as e:
            # se falhar, informar e não montar amortecimento
            print("Aviso: não foi possível calcular amortecimento de Rayleigh:", e)
            C_completa = None
        else:
            C_completa = np.zeros((2*num_nos, 2*num_nos))
            C_completa[np.ix_(livres, livres)] = C_red
            print(f"Rayleigh: alpha={alpha:.4e}, beta={beta:.4e}, modos usados={mi}, {mj}")
    else:
        C_completa = None

    return k_elem_global_geral, m_elem_global_geral, frequencias, C_completa