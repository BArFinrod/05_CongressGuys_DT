import streamlit as st
import pandas as pd
from openai import OpenAI
import json
import neo4j
import time

# Configura tu clave de API de OpenAI (asegúrate de definirla en st.secrets o reemplazarla directamente)
key_ = st.secrets["llm"]["key_"]

# DataFrame de ejemplo con los contextos
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
df_contextos = pd.DataFrame(data)


######### DB
uri = st.secrets['database']['uri']
auth =  (st.secrets['database']['auth1'], st.secrets['database']['auth2'])
# driverDB = neo4j.GraphDatabase.driver(uri, auth=auth)
#####
@st.cache_resource
def get_neo4j_driver(uri=uri, auth=auth):
    # Crea una conexión al driver de Neo4j
    return neo4j.GraphDatabase.driver(uri, auth=auth)

driverDB = get_neo4j_driver()

@st.cache_data
def consulta_neo4j(selected_congresista):
    # Define la consulta Cypher para obtener el perfil del congresista seleccionado
    query_str = f"MATCH (c:Congresista) WHERE c.Nombre = '{selected_congresista}' RETURN c.Perfil AS perfil"
    # Ejecuta la consulta y transforma el resultado a un DataFrame de pandas
    perfil_eager = driverDB.execute_query(query_str) #, result_transformer_=neo4j.Result.to_df)
    print(perfil_eager)
    perfil = perfil_eager.records[0].get("perfil") # Cambia el nombre de la columna a 'perfil'
    return perfil

# Desplegable en la barra lateral para seleccionar el contexto
with st.sidebar:
    st.header("Congresistas")
    selected_congresista = st.selectbox("Selecciona un congresista", df_contextos["congresista"].tolist())
    st.info("Selecciona un congresista para ver su perfil y chatear.")
    st.markdown("---")
    potencia = st.toggle("Análisis más potente", key="potente", value=False)
# Extrae el perfil correspondiente al contexto seleccionado
##### Consulta a Neo4j para obtener el perfil del congresista seleccionado
selected_perfil = consulta_neo4j(selected_congresista)

client = OpenAI(api_key = key_)
################
def _ask_chatgpt(messages, model="gpt-4o-mini"):
    if model == "o3-mini":
        response = client.chat.completions.create(
            model=model,
            # model="gpt-4o",
            # model="o1-preview",
            messages=messages,
            seed=12345,
            # max_tokens=100
        )
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            seed=12345,
            temperature=0,
        )
    response_txt = response.dict()['choices'][0]['message']['content']
    print(response_txt)
    return response_txt
##############
# Verifica si se ha cambiado de contexto y, en ese caso, reinicia el historial del chat
if "current_context" not in st.session_state or st.session_state.current_context != selected_congresista:
    st.session_state.current_context = selected_congresista
    # Se inicia el historial del chat con el mensaje de sistema que contiene el perfil del contexto
    # "Contesta como si tu fueras el congresista, infiere un estilo en base a su perfil"
    st.session_state.chat_history = [{"role": "system", "content": "Contesta las preguntas del usuario en base al siguiente perfil de congresista: \n ..." + selected_perfil}]

st.title("Chat con AI")


# Entrada de texto para el mensaje del usuario
user_input = st.chat_input("Escribe tu mensaje:", key="user_input")
if st.session_state["user_input"]:
    # Añade el mensaje del usuario al historial
    st.session_state.chat_history.append({"role": "user", "content": user_input})

# @st.cache_data
def stream_data(_LOREM_IPSUM):
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)

# Muestra el historial del chat
# Find the index of the last assistant message (if any)
last_assistant_idx = -1
for i, message in enumerate(st.session_state.chat_history):
    if message["role"] == "assistant":
        last_assistant_idx = i



# Botón para enviar el mensaje
if st.session_state["user_input"]:
    # Añade el mensaje del usuario al historial
    # st.session_state.chat_history.append({"role": "user", "content": user_input})
    # Llamada a la API de ChatGPT usando el historial completo de mensajes
    if potencia:
        response = _ask_chatgpt(
            model="o3-2025-04-16",
            messages=st.session_state.chat_history
        )
    else:
        response = _ask_chatgpt(
            model="gpt-4o-mini",
            messages=st.session_state.chat_history
        )
    
    # Extrae la respuesta del asistente y la añade al historial
    # assistant_response = response["choices"][0]["message"]["content"]
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Recarga la aplicación para actualizar el chat
    st.rerun()

# Display all messages
for i, message in enumerate(st.session_state.chat_history):
    if message["role"] == "user":
        with st.chat_message("Usuario"):
            st.write(f"{message['content']}")
    elif message["role"] == "assistant":
        with st.chat_message("AI"):
            # Only use streaming for the latest assistant message
            if i == last_assistant_idx:
                st.write_stream(stream_data(f"{message['content']}"))
            else:
                st.write(f"{message['content']}")
    # System messages are not displayed
