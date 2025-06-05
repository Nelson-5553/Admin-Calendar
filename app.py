import streamlit as st
import pandas as pd
from calendar_utils import conectar_google_calendar, listar_eventos

st.title('📆 Exportar calendario a Google')

st.write('Esta aplicación permite leer un archivo Excel y preparar la exportación de eventos a Google Calendar.')

# Subir archivo
datos = st.file_uploader("📤 Sube tu archivo Excel", type=["xlsx"])
calendar_id = pd.read_excel("datos/Calendarios.xlsx")

# Si se subió un archivo
if datos is not None:
    try:
        # Leer hoja específica
        df = pd.read_excel(datos)

        st.success("✅ Archivo cargado exitosamente.")
        st.write("🔍 Vista previa de los datos:")
        st.dataframe(df)

        # Formulario para agendar
        with st.form("my_form"):
            st.write("¿Deseas agendar los eventos?")
             # Muestra nombres pero guarda ID
            calendar_nombre = st.selectbox(
                "Selecciona el calendario:",
                options=calendar_id['Nombre']
            )

            # Obtener el ID real correspondiente
            calendar_id = calendar_id.loc[
                calendar_id['Nombre'] == calendar_nombre, 'Id'
            ].values[0]

            submit = st.form_submit_button("📅 Agendar eventos")

            if submit:
                st.info("🔄 Aquí iría la lógica para enviar los eventos a Google Calendar.")
                # st.write(f"Calendario seleccionado: {calendar_nombre} (ID: {calendar_id})")
                
                service = conectar_google_calendar()

                listar_eventos(service, calendar_id)

            
              
                st.success("✅ Eventos agendados (simulado)")

    except Exception as e:
        st.error(f"❌ Error al leer la hoja 'A101 V3': {e}")
