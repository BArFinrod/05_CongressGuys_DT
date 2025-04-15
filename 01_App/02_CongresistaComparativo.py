import streamlit as st
import pandas as pd
from openai import OpenAI
import plotly.express as px
import neo4j
import time
import json
from streamlit_plotly_events import plotly_events

# Configura tu clave de API de OpenAI
key_ = st.secrets["llm"]["key_"]

# DataFrame con los congresistas
data = {
    "congresista": [
        "ACUÑA PERALTA, MARIA GRIMANEZA",
    "ACUÑA PERALTA, SEGUNDO HECTOR",
    "AGUERO GUTIERREZ, MARIA ANTONIETA",
    "AGUINAGA RECUENCO, ALEJANDRO",
    "ALCARRAZ AGUERO, YOREL KIRA",
    "ALEGRIA GARCIA, ARTURO",
    "ALVA PRIETO, MARIA DEL CARMEN",
    "ALVA ROJAS, CARLOS ENRIQUE",
    "AMURUZ DULANTO, YESSICA ROSSELLI",
    "ANDERSON RAMIREZ, CARLOS ANTONIO",
    "ARAGON CARREÑO, LUIS ANGEL",
    "ARRIOLA TUEROS, JOSE ALBERTO",
    "AZURIN LOAYZA, ALFREDO",
    "BALCAZAR ZELADA, JOSE MARIA",
    "BARBARAN REYES, ROSANGELLA ANDREA",
    "BAZAN CALDERON, DIEGO ALONSO",
    "BAZAN NARRO, SIGRID TESORO",
    "BELLIDO UGARTE, GUIDO",
    "BERMEJO ROJAS, GUILLERMO",
    "BURGOS OLIVEROS, JUAN BARTOLOME",
    "BUSTAMANTE DONAYRE, ERNESTO",
    "CALLE LOBATON, DIGNA",
    "CAMONES SORIANO, LADY MERCEDES",
    "CASTILLO RIVAS, EDUARDO ENRIQUE",
    "CAVERO ALVA, ALEJANDRO ENRIQUE",
    "CERRON ROJAS, WALDEMAR JOSE",
    "CHACON TRUJILLO, NILZA MERLY",
    "CHIABRA LEON, ROBERTO ENRIQUE",
    "CHIRINOS VENEGAS, PATRICIA ROSA",
    "CICCIA VASQUEZ, MIGUEL ANGEL",
    "COAYLA JUAREZ, JORGE SAMUEL",
    "CORDERO JON TAY, LUIS GUSTAVO",
    "CORDOVA LOBATON, MARIA JESSICA",
    "CORTEZ AGUIRRE, ISABEL",
    "CRUZ MAMANI, FLAVIO",
    "CUETO ASERVI, JOSE ERNESTO",
    "CUTIPA CCAMA, VICTOR RAUL",
    "DAVILA ATANACIO, PASION NEOMIAS",
    "DOROTEO CARBAJO, RAUL FELIPE",
    "ECHAIZ DE NUÑEZ IZAGA, GLADYS M,",
    "ECHEVERRIA RODRIGUEZ, HAMLET",
    "ELIAS AVALOS, JOSE LUIS",
    "ESPINOZA VARGAS, JHAEC DARWIN",
    "FLORES ANCACHI, JORGE LUIS",
    "FLORES RAMIREZ, ALEX RANDU",
    "FLORES RUIZ, VICTOR SEFERINO",
    "GARCIA CORREA, IDELSO MANUEL",
    "GONZA CASTILLO, AMERICO",
    "GONZALES DELGADO, DIANA CAROLINA",
    "GUTIERREZ TICONA, PAUL SILVIO",
    "HEIDINGER BALLESTEROS, NELCY",
    "HERRERA MEDINA, NOELIA ROSSVITH",
    "HUAMAN CORONADO, RAUL",
    "INFANTES CASTAÑEDA, MERY ELIANA",
    "JAUREGUI MARTINEZ DE AGUAYO, MARIA",
    "JERI ORE, JOSE ENRIQUE",
    "JIMENEZ HEREDIA, DAVID JULIO",
    "JUAREZ CALLE, HEIDY LISBETH",
    "JUAREZ GALLEGOS, CARMEN PATRICIA",
    "JULON IRIGOIN, ELVA EDHIT",
    "KAMICHE MORANTE, LUIS ROBERTO",
    "LIMACHI QUISPE, NIEVES ESMERALDA",
    "LIZARZABURU LIZARZABURU, JUAN C,",
    "LOPEZ MORALES, JENY LUZ",
    "LOPEZ UREÑA, ILICH FREDY",
    "LUNA GALVEZ, JOSE LEON",
    "LUQUE IBARRA, RUTH",
    "MALAGA TRILLO, GEORGE EDWARD",
    "MARTICORENA MENDOZA, JORGE",
    "MARTINEZ TALAVERA, PEDRO EDWIN",
    "MEDINA HERMOSILLA, ELIZABETH SARA",
    "MEDINA MINAYA, ESDRAS RICARDO",
    "MITA ALANOCA, ISAAC",
    "MONTALVO CUBAS, SEGUNDO TORIBIO",
    "MONTEZA FACHO, SILVIA MARIA",
    "MONTOYA MANRIQUE, JORGE",
    "MORANTE FIGARI, JORGE ALBERTO",
    "MORI CELIS, JUAN CARLOS",
    "MOYANO DELGADO, MARTHA LUPE",
    "MUÑANTE BARRIOS, ALEJANDRO",
    "OBANDO MORGAN, AURISTELA ANA",
    "OLIVOS MARTINEZ, VIVIAN",
    "ORUE MEDINA, ARIANA MAYBEE",
    "PABLO MEDINA, FLOR AIDEE",
    "PADILLA ROMERO, JAVIER ROMMEL",
    "PALACIOS HUAMAN, MARGOT",
    "PAREDES CASTRO, FRANCIS JHASMINA",
    "PAREDES FONSECA, KAROL IVETT",
    "PAREDES GONZALES, ALEX ANTONIO",
    "PAREDES PIQUE, SUSEL ANA MARIA",
    "PARIONA SINCHE, ALFREDO",
    "PAZO NUNURA, JOSE BERNARDO",
    "PICON QUEDO, LUIS RAUL",
    "PORTALATINO AVALOS, KELLY ROXANA",
    "PORTERO LOPEZ, HILDA MARLENY",
    "QUIROZ BARBOZA, SEGUNDO TEODOMIRO",
    "QUISPE MAMANI, WILSON RUSBEL",
    "QUITO SARMIENTO, BERNARDO JAIME",
    "RAMIREZ GARCIA, TANIA ESTEFANY",
    "REVILLA VILLANUEVA, CESAR MANUEL",
    "REYES CAM, ABEL AUGUSTO",
    "REYMUNDO MERCADO, EDGARD CORNELIO",
    "RIVAS CHACARA, JANET MILAGROS",
    "ROBLES ARAUJO, SILVANA EMPERATRIZ",
    "ROSPIGLIOSI CAPURRO FERNANDO MIGUEL",
    "RUIZ RODRIGUEZ, MAGALY ROSMERY",
    "SAAVEDRA CASTERNOQUE, HITLER",
    "SALHUANA CAVIDES, EDUARDO",
    "SANCHEZ PALOMINO, ROBERTO HELBERT",
    "SANTISTEBAN SUCLUPE, MAGALLY",
    "SOTO PALACIOS, WILSON",
    "SOTO REYES, ALEJANDRO",
    "TACURI VALDIVIA, GERMAN ADOLFO",
    "TAIPE CORONADO, MARIA ELIZABETH",
    "TELLO MONTES, NIVARDO EDGAR",
    "TORRES SALINAS, ROSIO",
    "TRIGOZO REATEGUI, CHERYL",
    "TUDELA GUTIERREZ, ADRIANA JOSEFINA",
    "UGARTE MAMANI, JHAKELINE KATY",
    "VALER PINTO, HECTOR",
    "VARAS MELENDEZ, ELIAS MARCIAL",
    "VASQUEZ VELA, LUCINDA",
    "VENTURA ANGEL, HECTOR JOSE",
    "VERGARA MENDOZA, ELVIS HERNAN",
    "WILLIAMS ZAPATA, JOSE DANIEL",
    "WONG PUJADA, ENRIQUE",
    "YARROW LUMBRERAS, NORMA MARTINA",
    "ZEA CHOQUECHAMBI, OSCAR",
    "ZEBALLOS APONTE, JORGE",
    "ZEBALLOS MADARIAGA, CARLOS",
    "ZEGARRA SABOYA, ANA ZADITH",
    "ZETA CHUNGA, CRUZ MARIA"
    ]
}
df_congresistas = pd.DataFrame(data)
import numpy as np
import plotly.graph_objects as go
# temp_data = pd.DataFrame({
#     "congresista": np.array([0,100.]),
#     "id": np.array([1,2.])
# })

# print(temp_data)
# fig = go.Figure(data=go.Scatter(
#     x=temp_data["congresista"].to_list(),
#     y=temp_data["id"].to_list(),
#     mode='markers',
#     marker=dict(size=10),
#     text=temp_data["congresista"],
#     hoverinfo='text'
#     ))
# fig.update_layout(
#     title="Haz clic en un punto para ver la respuesta del congresista",
#     xaxis_title="Congresista",
#     yaxis_title="ID"
# )
#     # fig.update_traces(marker=dict(size=12), textposition="top center", textfont_size=10)
# # fig.update_layout(yaxis=dict(visible=True, range=[0, 2]))
    
#     # Mostrar gráfico interactivo y capturar eventos de clic
# selected_points = plotly_events(fig, click_event=True)
# Configuración Neo4j
uri = st.secrets['database']['uri']
auth = (st.secrets['database']['auth1'], st.secrets['database']['auth2'])

@st.cache_resource
def get_neo4j_driver(uri=uri, auth=auth):
    return neo4j.GraphDatabase.driver(uri, auth=auth)

driverDB = get_neo4j_driver()

@st.cache_data
def consulta_neo4j(selected_congresista):
    query_str = f"MATCH (c:Congresista) WHERE c.Nombre = '{selected_congresista}' RETURN c.Perfil AS perfil"
    perfil_eager = driverDB.execute_query(query_str)
    perfil = perfil_eager.records[0].get("perfil")
    return perfil

# Configuración de OpenAI
client = OpenAI(api_key=key_)

def _ask_chatgpt(messages, model="gpt-4o-mini"):
    if model == "o3-mini":
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            seed=12345,
            response_format = {"type": 'json_object',},
        )
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            seed=12345,
            temperature=0,
            response_format = {"type": 'json_object',}
        )
    return json.loads(response.dict()['choices'][0]['message']['content'])

# App principal
st.title("Análisis Comparativo de Congresistas")

# Sidebar para opciones
with st.sidebar:
    st.header("Opciones")
    num_congresistas = st.slider("Número de congresistas a analizar", 
                                min_value=2, max_value=len(df_congresistas), value=2)
    potencia = st.toggle("Análisis más potente", key="potente", value=False)
    st.markdown("---")
    st.info("Esta app permite hacer la misma pregunta a múltiples congresistas y comparar sus respuestas.")

# Seleccionar congresistas aleatoriamente o permitir selección manual
congresistas_seleccionados = df_congresistas.sample(n=num_congresistas)["congresista"].tolist()

# Entrada para la pregunta principal
query_input = st.text_input("¿Qué pregunta quieres hacer a todos los congresistas?", 
                           key="main_query")

# Botón para iniciar el análisis
if st.button("Analizar Respuestas", key="analisis_btn"):
    if not query_input:
        st.warning("Por favor, ingresa una pregunta para realizar el análisis.")
    else:
        # Inicializa un diccionario para almacenar las respuestas
        if "respuestas" not in st.session_state:
            st.session_state.respuestas = {}
            
        # Mostrar una barra de progreso
        progress_bar = st.progress(0)
        status_text = st.empty()
            
        # Ciclo para consultar a cada congresista
        for i, congresista in enumerate(congresistas_seleccionados):
            status_text.text(f"Procesando a {congresista}...")
            
            # Obtener el perfil del congresista
            perfil = consulta_neo4j(congresista)
            
            # Consulta al modelo de lenguaje con este perfil específico
            messages = [
                {"role": "system", "content": f"Contesta las preguntas del usuario en base al siguiente perfil de congresista: \n ... {perfil}. Responde en el siguiente formato json: \n {{\"respuesta\": \"...\", \"sentimiento\": \"...\"}} \n donde sentimiento puede se positivo, negativo o neutro."},
                {"role": "user", "content": query_input}
            ]
            
            model = "o3-mini" if potencia else "gpt-4o-mini"
            response = _ask_chatgpt(messages=messages, model=model)
            print(response)
            # Guardar la respuesta
            st.session_state.respuestas[congresista] = {
                "perfil": perfil,
                "respuesta": response['respuesta'],
                "sentimiento": response['sentimiento']
            }
            
            # Actualizar progreso
            progress_bar.progress((i + 1) / len(congresistas_seleccionados))
        
        status_text.text("¡Análisis completado!")
        st.session_state.analisis_completo = True

# Visualización de resultados (solo si hay análisis completado)
if "analisis_completo" in st.session_state and st.session_state.analisis_completo:
    st.header("Visualización de Resultados")
    
    # Crear un DataFrame para la visualización
    viz_data = pd.DataFrame({
        "congresista": list(st.session_state.respuestas.keys()),
        "id": range(len(st.session_state.respuestas)),
        "sentimiento": [st.session_state.respuestas[c]["sentimiento"] for c in st.session_state.respuestas],
    })
    
    # Asignar colores según el sentimiento
    color_map = {"positivo": "red", "neutro": "gray", "negativo": "blue"}
    viz_data["color"] = viz_data["sentimiento"].map(color_map)
    
    # Crear gráfico interactivo
    fig = go.Figure(data=go.Scatter(
        x=viz_data["congresista"].to_list(), 
        y=viz_data.shape[0]*[1],  # Mantener y constante para visualización
        mode='markers+text',
        # text=viz_data["congresista"],
        hoverinfo='text',
        marker=dict(size=10, color=viz_data["color"].to_list())
    ))
    fig.update_layout(
        title="Haz clic en un punto para ver la respuesta del congresista",
        xaxis_title="X",
        yaxis_title="Y"
    )
    fig.update_layout(yaxis=dict(visible=True, range=[0, 2]))
    
    # Mostrar gráfico interactivo y capturar eventos de clic
    selected_points = plotly_events(fig, click_event=True)
    
    # Diseño de dos columnas para mostrar respuesta seleccionada
    col1, col2 = st.columns([1, 2])
    
    # Mostrar la respuesta del congresista seleccionado
    if selected_points:
        idx = selected_points[0]["pointIndex"]
        congresista_seleccionado = viz_data.iloc[idx]["congresista"]
        
        with col1:
            st.subheader("Congresista")
            st.write(congresista_seleccionado)
            
        with col2:
            st.subheader("Respuesta")
            st.write(st.session_state.respuestas[congresista_seleccionado]["respuesta"])
    
    # Sección para preguntas sobre todas las respuestas
    st.header("Análisis de Respuestas")
    meta_query = st.chat_input("Pregunta sobre las respuestas de los congresistas:", key="meta_query")
    
    if meta_query:
        # Preparar el contexto con todas las respuestas
        context = "Respuestas de los congresistas a la pregunta: " + query_input + "\n\n"
        for congresista, data in st.session_state.respuestas.items():
            context += f"--- {congresista} ---\n{data['respuesta']}\n\n"
        
        # Consulta al modelo
        messages = [
            {"role": "system", "content": "Analiza las siguientes respuestas de congresistas peruanos y responde la pregunta del usuario sobre ellas."},
            {"role": "user", "content": context + "\n\nPregunta: " + meta_query}
        ]
        
        with st.spinner("Analizando respuestas..."):
            model = "o3-mini" if potencia else "gpt-4o-mini"
            meta_response = _ask_chatgpt(messages=messages, model=model)
        
        st.subheader("Análisis")
        st.write(meta_response)