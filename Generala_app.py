{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
\
st.set_page_config(page_title="Generala Pro", layout="centered")\
\
def main():\
    st.title("\uc0\u55356 \u57266  Anotador de Generala")\
\
    # Estructura de juego\
    categorias = \{\
        "1": 5, "2": 10, "3": 15, "4": 20, "5": 25, "6": 30,\
        "Escalera": (20, 25), "Full": (30, 35), "P\'f3ker": (40, 45), \
        "Generala": (50, 50), "Generala Doble": (100, 100)\
    \}\
    \
    jugadores = [f"Jugador \{i\}" for i in range(1, 6)]\
\
    # FIX: Inicializaci\'f3n robusta del estado\
    if 'puntajes' not in st.session_state:\
        st.session_state.puntajes = \{j: \{cat: 0 for cat in categorias\} for j in jugadores\}\
    else:\
        # Si el estado existe pero faltan jugadores (por cambio de c\'f3digo), los agregamos\
        for j in jugadores:\
            if j not in st.session_state.puntajes:\
                st.session_state.puntajes[j] = \{cat: 0 for cat in categorias\}\
\
    # --- VISTA DE RESUMEN ---\
    st.subheader("Estado de la Partida")\
    # Calculamos totales din\'e1micamente\
    totales = \{j: sum(st.session_state.puntajes[j].values()) for j in jugadores\}\
    df_totales = pd.DataFrame(totales, index=["Puntos totales"])\
    st.table(df_totales)\
\
    st.divider()\
\
    # --- INGRESO DE DATOS ---\
    st.subheader("Cargar Puntos")\
    tabs = st.tabs(jugadores)\
\
    for i, jugador in enumerate(jugadores):\
        with tabs[i]:\
            for cat, val in categorias.items():\
                key = f"\{jugador\}_\{cat\}"\
                \
                if isinstance(val, tuple):\
                    col1, col2 = st.columns([2, 1])\
                    with col1:\
                        # Recuperamos el valor previo para que no se borre al cambiar de pesta\'f1a\
                        valor_actual = st.session_state.puntajes[jugador][cat]\
                        logrado = st.checkbox(cat, key=f"log_\{key\}", value=(valor_actual > 0))\
                    with col2:\
                        servido = st.checkbox("S", key=f"chk_\{key\}", help="Servido")\
                    \
                    puntos = (val[1] if servido else val[0]) if logrado else 0\
                    st.session_state.puntajes[jugador][cat] = puntos\
                else:\
                    max_puntos = int(cat) * 5\
                    st.session_state.puntajes[jugador][cat] = st.number_input(\
                        f"Puntos en \{cat\}", min_value=0, max_value=max_puntos, \
                        step=int(cat), key=f"num_\{key\}",\
                        value=st.session_state.puntajes[jugador][cat]\
                    )\
\
    if st.button("Limpiar Tablero", use_container_width=True):\
        st.session_state.puntajes = \{j: \{cat: 0 for cat in categorias\} for j in jugadores\}\
        st.rerun()\
\
if __name__ == "__main__":\
    main()}