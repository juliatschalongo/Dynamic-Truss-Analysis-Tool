import numpy as np
from scipy import linalg

def executar(K, M, C, cargas, apoios, dt, t_final, tipo_forca, params_forca):

    """
    Método das Diferenças Centrais para integração no tempo de treliças.
    """

    ndof = K.shape[0]
    todos_gdls = list(range(ndof))

    # Identificar GL restritos a partir de 'apoios'
    restritos = []
    for apoio in apoios:
        no = int(apoio[0])
        if apoio[1] == 1: restritos.append(2*no)     # restrição em X
        if apoio[2] == 1: restritos.append(2*no + 1) # restrição em Y
    livres = [g for g in todos_gdls if g not in restritos]

    # Reduzir matrizes
    Kll = K[np.ix_(livres, livres)]
    Mll = M[np.ix_(livres, livres)]
    if C is None:
        Cll = np.zeros_like(Kll)
    else:
        Cll = C[np.ix_(livres, livres)]

    # Vetor de forças global
    Fg = np.zeros(ndof)
    for c in cargas:
        no = int(c[0])
        Fx, Fy = c[1], c[2]
        Fg[2*no]   += Fx
        Fg[2*no+1] += Fy
    Fll = Fg[livres]

    u0 = np.zeros(len(livres))
    v0 = np.zeros(len(livres))

    # Avaliar força inicial coerente com o tipo de carregamento
    t0 = 0.0
    ti = params_forca.get("ti", 0.0)
    tf = params_forca.get("tf", t_final)

    if t0 < ti or t0 > tf:
        Ft0 = np.zeros_like(Fll)
    else:
        if tipo_forca == "constante":
            A = params_forca.get("amplitude", 1.0)
            Ft0 = Fll * A

        elif tipo_forca == "harmonico":
            A = params_forca.get("amplitude", 1.0)
            w = params_forca.get("omega", 1.0)
            phi = params_forca.get("phi", 0.0)
            Ft0 = Fll * (A * np.cos(phi))

        elif tipo_forca == "rampa":
            A = params_forca.get("amplitude", 1.0)
            ti = params_forca.get("ti", 0.0)
            tf = params_forca.get("tf", t_final)
            Ft0 = Fll * (A * max(0.0, min(1.0, (0.0 - ti)/(tf - ti))))

    # Calcula a aceleração inicial 
    a0 = linalg.solve(Mll, Ft0 - Kll @ u0 - Cll @ v0)

    desloc, vel, acel = [u0], [v0], [a0]

    # Aproximação para u-1
    u_menos1 = u0 - dt*v0 + 0.5*(dt**2)*a0

    # Matrizes auxiliares
    K_eff = (Mll/(dt**2)) + (Cll/(dt*2))
    Amat = (Mll/(dt**2)) - (Cll/(dt*2))
    B = Kll - (2*Mll/(dt**2))

    Ft0 = Ft0 if 'Ft0' in locals() else np.zeros_like(Fll)

    # Matrizes auxiliares
    K_eff = (Mll/(dt**2)) + (Cll/(2*dt))
    Amat = (Mll/(dt**2)) - (Cll/(2*dt))
    B = Kll - (2*Mll/(dt**2))

    # Uusar Ft0 (força em t=0) para obter u1
    P0 = Ft0 - Amat @ u_menos1 - B @ u0    
    u1 = linalg.solve(K_eff, P0)

    desloc = [u0, u1]

    # v0, a0 já conhecidos 
    # calcular v1 e a1 usando aproximações coerentes
    v1 = (u1 - u_menos1) / (2.0 * dt)        
    a1 = (u1 - 2.0*u0 + u_menos1) / (dt**2)    

    vel = [v0, v1]
    acel = [a0, a1]

    # Preparar iteração
    u_prev = u0     # u_{n-1}
    u_curr = u1     # u_{n}
    tempo = np.arange(0.0, t_final + 1e-12, dt) 

    ti = params_forca.get("ti", 0.0)
    tf = params_forca.get("tf", t_final)

    # Loop: gerar u_{n+1} e armazenar valores alinhados (cada append corresponde a t_{n+1})
    for i, t in enumerate(tempo[1:], start=1):
        # Ft corresponde à força no tempo t (para montar P para obter u_next)
        if t < ti or t > tf:
            Ft = np.zeros_like(Fll)
        else:
            if tipo_forca == "constante":
                A = params_forca.get("amplitude", 1.0)
                Ft = Fll * A
            elif tipo_forca == "harmonico":
                A = params_forca.get("amplitude", 1.0)
                w = params_forca.get("omega", 1.0)
                phi = params_forca.get("phi", 0.0)
                Ft = Fll * (A * np.cos(w*t + phi))
            elif tipo_forca == "rampa":
                A = params_forca.get("amplitude", 1.0)
                Ft = Fll * (A * (t - ti) / (tf - ti))

        # resolver para u_next (u_{n+1})
        P = Ft - Amat @ u_prev - B @ u_curr
        u_next = linalg.solve(K_eff, P)

        # calcular velocidade e aceleração correspondentes a u_next (tempo t_{n+1})
        # uso backward differences para alinhar v_next com u_next:
        v_next = (u_next - u_curr) / dt
        a_next = (u_next - 2.0*u_curr + u_prev) / (dt**2)

        # armazenar (t_{n+1} corresponde ao índice i)
        desloc.append(u_next)
        vel.append(v_next)
        acel.append(a_next)

        # avançar indices
        u_prev, u_curr = u_curr, u_next

    # converter para arrays e reconstruir espaço completo como antes
    desloc = np.array(desloc)
    vel = np.array(vel)
    acel = np.array(acel)

    # garantir que o tamanho corresponde ao vetor tempo
    n_passos = len(tempo)
    if desloc.shape[0] > n_passos:
        desloc = desloc[:n_passos, :]
        vel = vel[:n_passos, :]
        acel = acel[:n_passos, :]
    elif desloc.shape[0] < n_passos:
        # se estiver faltando um passo, rechear com zeros (ou repetir o último) 
        falta = n_passos - desloc.shape[0]
        desloc = np.vstack([desloc, np.tile(desloc[-1], (falta, 1))])
        vel = np.vstack([vel, np.tile(vel[-1], (falta, 1))])
        acel = np.vstack([acel, np.tile(acel[-1], (falta, 1))])

    # Guardar cópia reduzida antes de expandir para todos os GLs
    desloc_reduzido = desloc.copy()
    vel_reduzido = vel.copy()
    acel_reduzido = acel.copy()

    # Reconstruir resultados no espaço completo 
    n_passos = desloc_reduzido.shape[0]
    desloc_full = np.zeros((n_passos, ndof))
    vel_full    = np.zeros((n_passos, ndof))
    acel_full   = np.zeros((n_passos, ndof))

    livres_arr = np.array(livres, dtype=int)

    desloc_full[:, livres_arr] = desloc_reduzido
    vel_full[:,    livres_arr] = vel_reduzido
    acel_full[:,   livres_arr] = acel_reduzido

    # Agora substituir os arrays pelos completos
    desloc = desloc_full
    vel    = vel_full
    acel   = acel_full

    if len(desloc) > len(tempo):
        desloc = desloc[:len(tempo), :]
        vel = vel[:len(tempo), :]
        acel = acel[:len(tempo), :]

    return desloc, vel, acel