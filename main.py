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
    


def main():
    # Configuración del título en la pestaña del navegador y en la página
    st.set_page_config(layout="wide", page_title="Gett App")
    st.title("Generador de exámenes tipo test")
    #st.header("(Texto de Header)")
    #st.markdown('## Texto con Markdown')
    #st.write("(Texto de Write)")
    #texto_input = st.text_input("**Texto de Input**")


    pdf_file = st.file_uploader('Elige tu documento PDF para generar el examen', type="pdf")
    # Sólo si el PDF se ha subido
    if pdf_file is not None:
        # Crea un archivo temporal para extraerlo con PyMuPDFLoader desde su ubicación
        temp_file = "./temp.pdf"
        with open(temp_file, "wb") as file:
            file.write(pdf_file.getvalue())
            file_name = pdf_file.name



        # Aparece el botón para generar el examen
        # El botón está asociado a la función que lanza al gett
        generar = st.button("Generar")
        if generar:
            
            # Creación de barra de progreso
            progress_text = "Examen generándose, por favor espere unos instantes"
            st.text(progress_text)
            my_bar = st.progress(0)
            my_bar.progress(5)
            time.sleep(2)

            my_bar.progress(15)
            time.sleep(1)
            my_bar.progress(25)

            # Generación del examen
            json_ett = iniciar_gett(temp_file)


            my_bar.progress(60)
            time.sleep(2)
            
            # Paso de json a diccionario
            data = json.loads(json_ett)

            my_bar.progress(80)
            time.sleep(2)
            
            time.sleep(2)
            my_bar.progress(100)

            # Mostrar el resultado por pantalla
            st.header("Examen Tipo Test:")
            
            mostrar_preguntas(data)
            progress_text.empty()
            my_bar.empty()

            os.remove("./temp.pdf")

                

if __name__ == '__main__':
    main()