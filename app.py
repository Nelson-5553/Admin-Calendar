import streamlit as st
import pandas as pd
from calendar_utils import conectar_google_calendar, listar_eventos

st.title('📆 Exportar calendario a Google')

st.write('Esta aplicación permite leer un archivo Excel y preparar la exportación de eventos a Google Calendar.')

# Subir archivo
datos = st.file_uploader("📤 Sube tu archivo Excel", type=["xlsx"])

# Si se subió un archivo
if datos is not None:
    try:
        # Leer hoja específica
        df = pd.read_excel(datos, sheet_name='A101 V3')

        st.success("✅ Archivo cargado exitosamente.")
        st.write("🔍 Vista previa de los datos:")
        st.dataframe(df)

        # Formulario para agendar
        with st.form("my_form"):
            st.write("¿Deseas agendar los eventos?")
            submit = st.form_submit_button("📅 Agendar eventos")

            if submit:
                st.info("🔄 Aquí iría la lógica para enviar los eventos a Google Calendar.")

                # Ejemplo (reemplazar por tu lógica real):
                calendar_id = "primary"  # Usar el calendario principal
                servicio = conectar_google_calendar()
                if servicio is None:
                    st.error("❌ No se pudo conectar a Google Calendar.")
                else:
                    listar_eventos(servicio, calendar_id)
                    # Aquí podrías llamar a una función para crear eventos
                    # Por ejemplo:
                # crear_eventos(servicio, df)
                st.success("✅ Eventos agendados (simulado)")

    except Exception as e:
        st.error(f"❌ Error al leer la hoja 'A101 V3': {e}")
