import streamlit as st
import streamlit_gett
import os
import json
import time

def iniciar_gett(url):
    # Se le pasa a Gett la ubicación del PDF

    examen = streamlit_gett.gett_action(url)

    return examen

# Función para mostrar las preguntas y respuestas
def mostrar_preguntas(data):
    for pregunta in data['preguntas']:

        # 1 - ¿Texto de pregunta?
        st.write(f"{pregunta['id']} - {pregunta['texto']}")

        for respuesta in pregunta['respuestas']:

            # Recorrer cada respuesta para extraer su contenido y si es correcta
            for clave, texto in respuesta.items():
                


                if clave != 'correcta':  # Ignorar la clave 'correcta' para este paso

                    letra_respuesta = clave.split()[-1] 
                    texto_respuesta = f"\t{letra_respuesta}) {texto}"
                    
                    # Añadir '(Correcta)' si esta respuesta es la correcta
                    #if respuesta['correcta']:
                    #    texto_respuesta += " (Correcta)"

                    #st.write(texto_respuesta)
                    # Se utiliza markdown para enriquecer la respuesta
                    st.markdown(f"<pre>\t{texto_respuesta}</pre>", unsafe_allow_html=True)


        st.write(f"Solución: {pregunta['solucion']}")
        st.write("---")  # Añadir una línea divisoria


def boton_generar():
    st.session_state.generando = True


def generar_examen(pdf):
    

    my_bar = st.progress(0)
    my_bar.progress(5)
    time.sleep(2)

   
    my_bar.progress(15)
    time.sleep(1)

    my_bar.progress(25)
    # Generación del examen
    son_ett = iniciar_gett(pdf)



    my_bar.progress(60)
    time.sleep(2)
    
    # Paso de json a diccionario
    data = json.loads(json_ett)

    my_bar.progress(80)
    time.sleep(2)
    
    time.sleep(2)
    my_bar.progress(100)


    st.write("Proceso finalizado. Para generar un nuevo examen suba de nuevo un PDF")  # Añadir una línea divisoria



    # Mostrar el resultado por pantalla
    st.header("Examen Tipo Test:")
    mostrar_preguntas(data)

    st.session_state.generando = False

    my_bar.empty()



def main():
    # Configuración del título en la pestaña del navegador y en la página
    st.set_page_config(layout="wide", page_title="Gett App")
    st.title("Generador de exámenes tipo test")
    #st.header("(Texto de Header)")
    #st.markdown('## Texto con Markdown')
    #st.write("(Texto de Write)")
    #texto_input = st.text_input("**Texto de Input**")

    if 'generando' not in st.session_state:
        st.session_state.generando = False


    pdf_file = st.file_uploader('Elige tu documento PDF para generar el examen', type="pdf")

    # Sólo si el PDF se ha subido
    if pdf_file is not None:
        # Crea un archivo temporal para extraerlo con PyMuPDFLoader desde su ubicación
        temp_file = "./temp.pdf"
        with open(temp_file, "wb") as file:
            file.write(pdf_file.getvalue())
            file_name = pdf_file.name


        # Se muestra el botón si aún no se ha empezado a generar
        if not st.session_state.generando:
            st.button('Generar', on_click=boton_generar)
            st.write("Nota: Dependiendo del tamaño del PDF, el proceso puede tardar uno o varios minutos")
        
    if st.session_state.generando:
        generar_examen(temp_file)

                

if __name__ == '__main__':
    main()