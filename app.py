import streamlit as st
import pandas as pd
from calendar_utils import conectar_google_calendar, listar_eventos, crear_evento

st.title('📆 Exportar calendario a Google')
st.write('Esta aplicación permite leer un archivo Excel y preparar la exportación de eventos a Google Calendar.')

# Subir archivo
datos = st.file_uploader("📤 Sube tu archivo Excel", type=["xlsx"])
calendars = pd.read_excel("datos/Calendarios.xlsx")

# Si se subió un archivo
if datos is not None:
    try:
        # Leer hoja específica
        df = pd.read_excel(datos, sheet_name="A101 V3")

        st.success("✅ Archivo cargado exitosamente.")
        st.write("🔍 Vista previa de los datos:")
        st.dataframe(df)

        # Formulario para agendar
        with st.form("my_form"):
            st.write("¿Deseas agendar los eventos?")
            
            # Muestra nombres pero guarda ID
            calendar_nombre = st.selectbox(
                "Selecciona el calendario:",
                options=calendars['Nombre']
            )

            # Obtener el ID real correspondiente
            calendar_id = calendars.loc[
                calendars['Nombre'] == calendar_nombre, 'Id'
            ].values[0]

            start = st.date_input(
                "Inicio de semestre",
                value="today",
                min_value=None,
                max_value=None,
                key=None
            )
            end = st.date_input(
                "Fin de semestre",
                value="today",
                min_value=None,
                max_value=None,
                key=None
            )

            submit = st.form_submit_button("📅 Agendar eventos")

            if submit:
                st.info("🔄 Aquí iría la lógica para enviar los eventos a Google Calendar.")
                # st.write(f"Calendario seleccionado: {calendar_nombre} (ID: {calendar_id})")
                
                service = conectar_google_calendar()
                crear_evento(service, calendar_id, calendar_nombre, start, end) 

    except Exception as e:
        st.error(f"❌ Error al leer la hoja 'A101 V3': {e}")
