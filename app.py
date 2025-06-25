import streamlit as st
import pandas as pd
from calendar_utils import conectar_google_calendar, eliminar_eventos, crear_evento

st.title('📆 Admin Calendar')
st.write('Esta aplicación permite leer un archivo Excel y preparar la importacion de eventos a Google Calendar.')

# Subir archivo
datos = st.file_uploader("📤 Sube tu archivo Excel", type=["xlsx"])
calendars = pd.read_excel("datos/Calendarios.xlsx")

# Si se subió un archivo
if datos is not None:
    try:
        # Leer hoja específica
        events = pd.read_excel(datos) # sheet_name="A101 V3"

        st.success("✅ Archivo cargado exitosamente.")
        st.write("🔍 Vista previa de los datos:")
        st.dataframe(events)

        # Formulario para agendar
        with st.form("event_form"):
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
                st.write(f"Calendario seleccionado: {calendar_nombre}")
                service = conectar_google_calendar()
                crear_evento(service, calendar_id, events, start, end) 

    except Exception as e:
        st.error(f"❌ Error al leer la hoja 'A101 V3': {e}")

# Formulario para eliminar eventos

with st.form("delete_form"):
    st.write("¿Deseas eliminar eventos?")

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

    delete = st.form_submit_button("❌ Eliminar eventos")

    if delete:
        st.write(f"Calendario seleccionado: {calendar_nombre}")
        service = conectar_google_calendar()
        eliminar_eventos(service, calendar_id, start, end)