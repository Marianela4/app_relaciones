import random
import streamlit as st
import pandas as pd

st.set_page_config(page_title="APP de relaciones", page_icon="🔗", layout="centered")
st.markdown("""
<style>
    button[kind="primary"] {
        background-color: #2E8B57;
        border-color: #2E8B57;
        color: white;
    }
    button[kind="primary"]:hover {
        background-color: #246B45;
        border-color: #246B45;
        color: white;
    }
</style>
""", unsafe_allow_html=True)
st.title("App de relaciones")
st.write("Generá una relación aleatoria y comprobá si es reflexiva y simétrica.")

entrada = st.text_input("Escribi los elementos del conjunto A (separados por comas)", value="4, 5, 7")
elementos = [e.strip() for e in entrada.split(",") if e.strip()]

if not elementos:
    st.warning("Ingresá al menos un elemento.")
    st.stop()
if len(elementos) != len(set(elementos)):
    st.error("No repitas elementos: en un conjunto cada elemento aparece una sola vez.")
    st.stop()
if len(elementos) > 6:
    st.warning("Por claridad visual, usá hasta 6 elementos.")
    st.stop()

A = elementos
pares_posibles = [(a, b) for a in A for b in A]
st.write("**Conjunto A:**", "{" + ", ".join(A) + "}")
st.write(f"**Producto cartesiano:** {len(pares_posibles)} pares posibles")
st.write(f"**Cantidad de relaciones posibles:** 2^{len(pares_posibles)} = {2 ** len(pares_posibles)}")

if st.button("🎲 Generar relación aleatoria", type="primary"):
    st.session_state.relacion = [par for par in pares_posibles if random.choice([True, False])]
    st.session_state.conjunto_de_relacion = tuple(A)

if st.session_state.get("conjunto_de_relacion") != tuple(A):
    st.info("Presioná el botón para generar una relación con este conjunto.")
    st.stop()

R = st.session_state.relacion
R_set = set(R)
texto_relacion = "{" + ", ".join(f"({a}, {b})" for a, b in R) + "}" if R else "∅"
st.subheader("Relación generada")
st.code("R = " + texto_relacion, language=None)

faltan_reflexiva = [(a, a) for a in A if (a, a) not in R_set]
faltan_inversos = [(b, a) for a, b in R if (b, a) not in R_set]
reflexiva = len(faltan_reflexiva) == 0
simetrica = len(faltan_inversos) == 0

izquierda, derecha = st.columns(2)
with izquierda:
    st.metric("Reflexiva", "Sí ✅" if reflexiva else "No ❌")
with derecha:
    st.metric("Simétrica", "Sí ✅" if simetrica else "No ❌")

if reflexiva:
    st.success("Es reflexiva: todos los pares (a, a) pertenecen a R.")
else:
    st.warning("No es reflexiva. Faltan: " + ", ".join(str(p) for p in faltan_reflexiva))

if simetrica:
    st.success("Es simétrica: para cada (a, b) de R también está (b, a).")
else:
    st.warning("No es simétrica. Faltan los inversos: " + ", ".join(str(p) for p in sorted(set(faltan_inversos))))

st.subheader("Matriz de la relación")
st.write("✅ significa que el par pertenece a R; · significa que no pertenece.")
matriz = pd.DataFrame(
    [["✅" if (a, b) in R_set else "·" for b in A] for a in A],
    index=A,
    columns=A,
)
matriz.index.name = "a ↓ / b →"
st.table(matriz)

with st.expander("¿Cómo se genera y se comprueba la relación?"):
    st.write("Para cada par de A × A, el programa decide aleatoriamente incluirlo o no. "
             "Una relación es reflexiva si contiene todos los pares (a, a). "
             "Es simétrica si, por cada par (a, b) incluido, también incluye (b, a).")
