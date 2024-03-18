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
import streamlit as st
from langchain.callbacks.tracers import LangChainTracer
tracer = LangChainTracer(project_name="Gett de Streamlit")

import os
LANGCHAIN_TRACING_V2 = st.secrets["tracing"]
LANGCHAIN_ENDPOINT = st.secrets["lc_endpoint"]
LANGCHAIN_API_KEY = st.secrets["lc_api_key"]
OPENAI_API_KEY = st.secrets["opai_api_key"]
LANGCHAIN_PROJECT = st.secrets["lc_project"]


os.environ['LANGCHAIN_TRACING_V2'] = st.secrets["tracing"]
os.environ['LANGCHAIN_ENDPOINT'] = st.secrets["lc_endpoint"]
os.environ['LANGCHAIN_API_KEY'] = st.secrets["lc_api_key"]
os.environ['OPENAI_API_KEY'] = st.secrets["opai_api_key"]
os.environ['LANGCHAIN_PROJECT'] = st.secrets["lc_project"]


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
    cada una con sus cuatro respuestas (precedidas de 'a)', 'b)', 'c)' y 'd)' respectivamente) y lístalas enumeradas
    de la siguiente forma':\n\n
       
        1 - 'Texto pregunta 1'\n
            a) 'Texto respuesta a)'\n
            b) 'Texto respuesta b)'\n
            c) 'Texto respuesta c)'\n
            d) 'Texto respuesta d)'\n\n
        
        2 - 'Texto pregunta 2'\n
            a) 'Texto respuesta a)'\n
            b) 'Texto respuesta b)'\n
            c) 'Texto respuesta c)'\n
            d) 'Texto respuesta d)'\n\n
        
        3 - 'Texto pregunta 3'\n
            a) 'Texto respuesta a)'\n
            b) 'Texto respuesta b)'\n
            c) 'Texto respuesta c)'\n
            d) 'Texto respuesta d)'\n\n
        ...
                                              
                                                                                             
    Paso 3 - Tras la lista anterior haz una separación, añade el título 'Soluciones' y lista las soluciones de cada
    una de las preguntas de la siguiente forma:\n\n
        
        Soluciones:\n
        
        1 - 'letra de la respuesta')\n
        2 - 'letra de la respuesta')\n
        3 - 'letra de la respuesta')\n
                                             
                                                    
                                                    
    Paso 4 - Devuelve como respuesta únicamente el resultado de el Paso 2 y el Paso 3. 
    Asegúrate de que entre pregunta y pregunta haya un doble retorno de carro para que se vea todo más organizado
    
                                                                                             
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


