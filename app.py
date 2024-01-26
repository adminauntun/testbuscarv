import pandas as pd
import streamlit as st

def file_opener(uploaded_file):
    try:
        # Especifica dtype=str para asegurar que todos los datos se lean como texto
        df = pd.read_excel(uploaded_file, header=0, dtype=str)
        return df
    except:
        st.error("Error al cargar el archivo.")

def create_lista(df, columna):
    return df[columna].tolist()

valores_no_utiles = ["Código", "MAIRA SRL", "MAIRA", "nan"]

def depuracion(lista):
    return [i for i in lista if i not in valores_no_utiles and not pd.isna(i)]

def buscador_coincidencias_y_columna_adjacente(df, productos_a_actualizar_depurado, productos_actualizados_depurado):
    sin_actualizar_con_adjacente = []
    for producto in productos_a_actualizar_depurado:
        if producto not in productos_actualizados_depurado:
            index = df[df['a actualizar'] == producto].index[0]
            valor_adjacente = df.iloc[index, df.columns.get_loc('a actualizar') + 1]
            # Asegurarse de que los datos estén como texto
            producto = str(producto)
            valor_adjacente = str(valor_adjacente)
            sin_actualizar_con_adjacente.append([producto, valor_adjacente])
    return sin_actualizar_con_adjacente

st.title("Cargador de Archivos de Productos")
st.write("Colocar ´a actualizar´ como titulo a la columna de codigos a modificar")
st.write("Colocar ´actualizados´ como titulo a la columna de codigos modificados del reporte de flexxus")
uploaded_file = st.file_uploader("Cargue aquí su archivo Excel", type=['xlsx'])

if uploaded_file is not None:
    file_handler = file_opener(uploaded_file)

    productos_a_actualizar = create_lista(file_handler, "a actualizar")
    productos_actualizados = create_lista(file_handler, "actualizados")

    productos_a_actualizar_depurado = depuracion(productos_a_actualizar)
    productos_actualizados_depurado = depuracion(productos_actualizados)

    productos_sin_actualizar_con_adjacente = buscador_coincidencias_y_columna_adjacente(file_handler, productos_a_actualizar_depurado, productos_actualizados_depurado)

    df_resultado = pd.DataFrame(productos_sin_actualizar_con_adjacente, columns=["Productos sin actualizar", "Descripcion del producto"])
    
    # Mostrar la tabla en Streamlit
    cantidad_no_actualizados = len(df_resultado)
    cantidad_actualizados = len(productos_a_actualizar_depurado) - cantidad_no_actualizados
    st.write("Haz actualizado: ",cantidad_actualizados, " de ", len(productos_a_actualizar_depurado))
    st.write("La cantidad de productos sin actualizar es: ", cantidad_no_actualizados)
    st.write("Vista previa de la tabla a descargar:")
    st.dataframe(df_resultado)  # Puedes usar st.table(df_resultado) si prefieres
    
    # Convertir DataFrame a CSV para la descarga
    csv_data = df_resultado.to_csv(index=False, sep=';', quotechar='"', encoding='utf-8')
    
    archivo_salida = "productos_sin_actualizar.csv"
    
    st.download_button(label="Descargar Datos", data=csv_data, file_name=archivo_salida, mime='text/csv')
    

else:
    st.write("Por favor, cargue un archivo para continuar.")
