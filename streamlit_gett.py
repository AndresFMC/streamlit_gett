# --------------------------------------------------

# Generador de exámenes tipo test (Gett) - Streamlit Version

#---------------------------------------
# Coste total para el ejemplo de fases-ciclo-hidrologico.pdf
# 0.005326$:
# Prompt Tokens: 1964 ()
# Completion Tokens: 2896
#cmd+k+c
#---------------------------------------
# You can set the project name for a specific tracer instance:

from langchain.callbacks.tracers import LangChainTracer
tracer = LangChainTracer(project_name="Gett de Streamlit")

import os
# LANGCHAIN_TRACING_V2 = st.secrets["tracing"]
# LANGCHAIN_ENDPOINT = st.secrets["lc_endpoint"]
# LANGCHAIN_API_KEY = st.secrets["lc_api_key"]
# OPENAI_API_KEY = st.secrets["opai_api_key"]
# LANGCHAIN_PROJECT = st.secrets["lc_project"]


# os.environ['LANGCHAIN_TRACING_V2'] = st.secrets["tracing"]
# os.environ['LANGCHAIN_ENDPOINT'] = st.secrets["lc_endpoint"]
# os.environ['LANGCHAIN_API_KEY'] = st.secrets["lc_api_key"]
# os.environ['OPENAI_API_KEY'] = st.secrets["opai_api_key"]
# os.environ['LANGCHAIN_PROJECT'] = st.secrets["lc_project"]

import os
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY = os.environ.get('LANGCHAIN_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
LANGCHAIN_PROJECT="Gett de Streamlit"


# Librerías para la extracción del texto del PDF
from langchain.prompts import PromptTemplate

from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain

from langchain_community.document_loaders import PyMuPDFLoader
from langchain.chains.combine_documents.stuff import StuffDocumentsChain


def gett_action(url_pdf):

    # 1 - Prompt para la extracción de los conceptos clave
    first_prompt_template = """
    Analiza el siguiente texto y extrae los conceptos más importantes. 
    Resume estos conceptos en una lista enumerada, asegurándote de incluir solamente 
    aquellos elementos que sean fundamentales para entender la 
    temática central del texto. Evita detalles secundarios y céntrate en 
    las ideas principales.

    Texto:
    {Texto}
    """
    first_prompt = PromptTemplate.from_template(first_prompt_template)


    #2 - Cadena que realiza la consulta con el primer Prompt
    llm = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(llm=llm, prompt=first_prompt)


    # 3 - Obtención de los conceptos clave con la cadena Stuff
    # Recuerda que la document_variable_name debe ser la palabra clave del prompt
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="Texto")

    loader = PyMuPDFLoader(url_pdf)
    docs = loader.load()
    print("\n\nPDF cargado y listo para comenzar con Gett\n\n")

    #print(stuff_chain.invoke(docs))
    resultado = stuff_chain.invoke(docs)
    conceptos = resultado["output_text"]

    print("\n\nConceptos clave extraídos:\n\n")
    print(conceptos, "\n\n")
    

    from langchain.prompts import ChatPromptTemplate
    from langchain.chains import SequentialChain

    # 4 - Creación de las preguntas a partir de los conceptos clave
    # prompt template 2 - Conceptos -> Preguntas
    second_prompt = ChatPromptTemplate.from_template("""
    Basado en los conceptos clave extraídos previamente del texto, 
    crea una pregunta para cada concepto de manera que la respuesta 
    directa a cada pregunta sea el concepto clave correspondiente. 
    Asegúrate de que las preguntas estén formuladas de manera clara y 
    comprensible, y que inviten a respuestas que sean específicamente 
    esos conceptos.

    Conceptos:
    {Conceptos}

    """
    )

    # chain 2: input= Conceptos and output= Preguntas
    chain_two = LLMChain(llm=llm, prompt=second_prompt, 
                        output_key="Preguntas"
                        )

    # prompt template 3 - Preguntas -> JSON
    third_prompt = ChatPromptTemplate.from_template("""
    {Preguntas}

    Sigue las siguientes instrucciones paso a paso utilizando las preguntas mostradas previamente.
                                                    
    Paso 1 - Para cada una de las preguntas generadas previamente, 
    basadas en los conceptos clave extraídos del texto, 
    desarrolla tres respuestas alternativas erróneas. 
    Estas respuestas deben ser plausibles y no evidentes como incorrectas a primera vista. 
    Deben requerir una comprensión clara del concepto clave para identificar por qué son incorrectas. 
    Considera tanto la respuesta correcta como el contenido del texto original para asegurar que cada 
    respuesta incorrecta sea convincente y relevantemente errónea. 
    Formúlalas de tal manera que estimulen el pensamiento crítico y la comprensión profunda del tema.

    Paso 2 - Organiza el conjunto de preguntas proporcionadas, 
    cada una con sus cuatro respuestas, en un formato JSON estructurado. 
    Para cada pregunta, incluye un identificador único, 
    la pregunta, las respuestas y, para cada respuesta, 
    un booleano que indique si es correcta o incorrecta. 
    Asegúrate de que el formato JSON sea válido y 
    fácilmente interpretable por un humano o una máquina.
                                                    
    Finalmente, devuelve únicamente el resultado del paso 2 completo
                                                    
    Paso 2 - Organiza el conjunto de preguntas proporcionadas, 
    cada una con sus cuatro respuestas, en un formato JSON estructurado de la siguiente manera:                                              
    
    ```json
        {{
        "preguntas": [
            {{
            "id": 1,
            "texto": "Aquí va la pregunta",
            "respuestas": [
                {{"respuesta a": "Aquí va el texto de la respuesta a", "correcta": false}},
                {{"respuesta b": "Aquí va el texto de la respuesta b", "correcta": false}},
                {{"respuesta c": "Aquí va el texto de la respuesta c", "correcta": true}},
                {{"respuesta d": "Aquí va el texto de la respuesta d", "correcta": false}}
            ],
            "solucion": "respuesta c"
                                                    
            }},
            {{
            "id": 2,
            "texto": "Aquí va la siguiente pregunta",
            "respuestas": [
                {{"respuesta a": "Aquí va el texto de la respuesta a", "correcta": false}},
                {{"respuesta b": "Aquí va el texto de la respuesta b", "correcta": true}},
                {{"respuesta c": "Aquí va el texto de la respuesta c", "correcta": false}},
                {{"respuesta d": "Aquí va el texto de la respuesta d", "correcta": false}}
            ]
            "solucion": "respuesta b"                                       
            }}
            // Añade más preguntas siguiendo el mismo patrón
        ]
        }}
    
    ```
    Es importante que en las claves de las respuestas se distinga entre A, B, C o D para poder
    manejar las respuestas independientemente.
                                                    
    Finalmente, devuelve únicamente el resultado del paso 2 completo    
                                                                                             
    """
    )

    # chain 3: input= Preguntas and output= ett
    chain_three = LLMChain(llm=llm, prompt=third_prompt,
                        output_key="json_ett"
                        )


    # overall_chain: input= Texto 
    # and output= Conceptos, Preguntas, json_ett
    overall_chain = SequentialChain(
        chains=[chain_two, chain_three,],
        input_variables=["Conceptos"],
        output_variables=[ "Preguntas", "json_ett"],
        verbose=True
    )

    respuesta = overall_chain.invoke(conceptos)
    json = respuesta["json_ett"]
    print("\n\nGett completado con éxito\n\n")
    return json



# print("\n\nTipo de la respuesta: ", type(respuesta), "\n\n")
# print("Respuesta: \n\n", respuesta, "\n\n")

# print("\n\nTipo del json: ", type(json), "\n\n")
# print("json: \n\n", json, "\n\n")


