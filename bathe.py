import numpy as np
from scipy import linalg

def executar(K, M, C, cargas, apoios, dt, t_final, tipo_forca, params_forca,
            B1=0.57, B2=0.07*0.57, gamma=0.5):
    
    """
    Método Explícito de Bathe para integração no tempo de treliças.
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
            Ft0 = Fll * (A * np.cos(w*t0 + phi))

        elif tipo_forca == "rampa":
            A = params_forca.get("amplitude", 1.0)
            Ft0 = Fll * (A * (t0 - ti) / (tf - ti))

    # Agora calcula a aceleração inicial com a força inicial correta
    a0 = linalg.solve(Mll, Ft0 - Kll @ u0 - Cll @ v0)

    desloc, vel, acel = [u0], [v0], [a0]

    # --- Loop no tempo
    tempo = np.arange(0, t_final+dt, dt)
    u, v, a = u0, v0, a0

    ti = params_forca.get("ti", 0.0)
    tf = params_forca.get("tf", t_final)

    for i, t in enumerate(tempo[1:], start=1):
        if t < ti or t > tf:
            Ft = np.zeros_like(Fll)
        else:
            if tipo_forca == "constante":
                A = params_forca.get("amplitude", 1.0)
                Ft = Fll * A

            elif tipo_forca == "harmonico":
                A = params_forca.get("amplitude", 1.0)
                w = params_forca.get("omega", 1.0)   # rad/s
                phi = params_forca.get("phi", 0.0)   # rad
                Ft = Fll * (A * np.cos(w*t + phi))

            elif tipo_forca == "rampa":
                A = params_forca.get("amplitude", 1.0)
                Ft = Fll * (A * (t-ti) / (tf-ti))  # normaliza no intervalo

        # --- Substep 1 ---
        u1 = u + gamma*dt*v + 0.5*((gamma*dt)**2)*a
        v1 = v + gamma*dt*a
        R_hat = Ft - (Cll @ v1) - (Kll @ u1)
        a1 = linalg.solve(Mll, R_hat)

        v1 = v + gamma*dt*a + B1*gamma*dt*(a1-a)
        u1 = u + gamma*dt*v + 0.5*((gamma*dt)**2)*a + B2*((gamma*dt)**2)*(a1-a)

        # --- Substep 2 ---
        u2 = u1 + (1-gamma)*dt*v1 + 0.5*((1-gamma)*dt)**2 * a1
        v2 = v1 + (1-gamma)*dt*a1
        R2_hat = Ft - (Cll @ v2) - (Kll @ u2)
        a2 = linalg.solve(Mll, R2_hat)

        v2 = v1 + (1-gamma)*dt*a1 + B1*(1-gamma)*dt*(a2-a1)
        u2 = u1 + (1-gamma)*dt*v1 + 0.5*((1-gamma)*dt)**2*a1 + B2*((1-gamma)*dt)**2*(a2-a1)

        u, v, a = u2, v2, a2

        desloc.append(u); vel.append(v); acel.append(a)

    # --- transforma listas em arrays (resultados no espaço reduzido) ---
    desloc = np.array(desloc)   # shape = (n_passos, n_gl_livres)
    vel    = np.array(vel)
    acel   = np.array(acel)

    # Guarda cópia reduzida para compatibilidade
    desloc_reduzido = desloc.copy()
    vel_reduzido = vel.copy()
    acel_reduzido = acel.copy()

    # --- Reconstruir resultados no espaço completo ---
    n_passos = desloc_reduzido.shape[0]
    desloc_full = np.zeros((n_passos, ndof))
    vel_full    = np.zeros((n_passos, ndof))
    acel_full   = np.zeros((n_passos, ndof))

    livres_arr = np.array(livres, dtype=int)

    desloc_full[:, livres_arr] = desloc_reduzido
    vel_full[:,    livres_arr] = vel_reduzido
    acel_full[:,   livres_arr] = acel_reduzido

    # Agora substituímos os arrays pelos completos
    desloc = desloc_full
    vel    = vel_full
    acel   = acel_full

    return desloc, vel, acel