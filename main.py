import streamlit as st
import streamlit_gett
import os

def iniciar_gett(url):
    # Se le pasa a Gett la ubicación del PDF

    examen = streamlit_gett.gett_action(url)

    return examen
    


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
            ett = iniciar_gett(temp_file)

            # Añadir un progreso del proceso
            

            # Mostrar el resultado por pantalla
            st.header("Examen Tipo Test:")
            st.write(ett)
            # Elimina el archivo temporal creado para cargar el PDF
            os.remove("./temp.pdf")
                

if __name__ == '__main__':
    main()