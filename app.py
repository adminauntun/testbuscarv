import pandas as pd
import streamlit as st
from io import BytesIO
import string

# Función para generar nombres de columnas basados en el número de columnas
def generate_column_names(n):
    alphabet = list(string.ascii_uppercase)
    column_names = []
    for first_letter in alphabet:
        column_names.append(first_letter)
        if len(column_names) == n:
            return column_names
    for first_letter in alphabet:
        for second_letter in alphabet:
            column_names.append(first_letter + second_letter)
            if len(column_names) == n:
                return column_names

# Función para convertir el dataframe a Excel para descarga
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

# Cargar el archivo
uploaded_file = st.file_uploader("Sube tu archivo aquí", type=['xlsx', 'xls', 'csv'])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1]

    # Leyendo el archivo según su extensión
    if file_extension in ['xlsx', 'xls']:
        df = pd.read_excel(uploaded_file, engine='xlrd')
    elif file_extension == 'csv':
        df = pd.read_csv(uploaded_file)

    # Inicializar barra de progreso y texto de estado en Streamlit
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Generar nombres de columnas basados en el número de columnas del DataFrame
    df.columns = generate_column_names(len(df.columns))

    progress_bar.progress(20)
    status_text.text("Preprocesando datos...")

    # Convertir las columnas relevantes a string y manejar valores NaN
    df['A'] = df['A'].astype(str).fillna('')
    df['D'] = df['D'].astype(str).fillna('')

    # Ignorar artículos que contienen la palabra 'MAIRA' en la columna 'A'
    df = df[~df['A'].str.contains('MAIRA','maira')]

    progress_bar.progress(40)
    status_text.text("Validando longitud de artículos...")

    # Filtrar artículos con longitud inválida en la columna 'A'
    valid_length = df['A'].apply(lambda x: len(x) in [5, 6])
    invalid_articles = df[~valid_length]
    df = df[valid_length]

    progress_bar.progress(60)
    status_text.text("Comparando artículos...")

    # Comparando artículos de la Columna A con la Columna D
    unmatched = df[~df['A'].isin(df['D'])][['A', 'B']]

    # Conteo de coincidencias y no coincidencias
    count_unmatched = unmatched.shape[0]
    progress_bar.progress(80)
    status_text.text(f"Proceso completado. Artículos no actualizados: {count_unmatched}")

    # Preparar el archivo Excel para la descarga
    output_file = to_excel(unmatched)
    st.download_button(label="Descargar Excel con artículos no actualizados",
                       data=output_file,
                       file_name="Items_no_encontrados.xlsx",
                       mime="application/vnd.ms-excel")

    # Opcional: Mostrar y descargar artículos con longitud inválida
    if not invalid_articles.empty:
        st.write("Artículos con longitud inválida:")
        st.dataframe(invalid_articles)
        invalid_file = to_excel(invalid_articles)
        st.download_button(label="Descargar Excel con artículos de longitud inválida",
                           data=invalid_file,
                           file_name="Articulos_longitud_invalida.xlsx",
                           mime="application/vnd.ms-excel")

    progress_bar.progress(100)
