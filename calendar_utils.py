import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def conectar_google_calendar(credenciales_path='credentials.json'):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    try:
        creds = service_account.Credentials.from_service_account_file(credenciales_path, scopes=SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        # Verificar conexión
        st.success("Conexión exitosa a Google Calendar.")

        return service
    except FileNotFoundError:
        st.error("Archivo de credenciales no encontrado.")
    except HttpError as e:
        st.error(f"Error en la conexión con Google Calendar: {e}")
    except Exception as e:
        st.error(f"Error inesperado: {e}")
    return None

def listar_eventos(service, calendar_id):
    events_result = service.events().list(calendarId=calendar_id, maxResults=10).execute()
    events = events_result.get('items', [])
    
    if not events:
        st.write("No hay eventos en este calendario.")
    else:
        st.write(f"Eventos en el calendario {calendar_id}:")
        for event in events:
            st.write(f"- {event.get('summary', 'Sin título')} ({event.get('start')})")

