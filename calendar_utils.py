import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, time



def conectar_google_calendar(credenciales_path='credentials.json'):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    try:
        creds = service_account.Credentials.from_service_account_file(
            credenciales_path, scopes=SCOPES
        )
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



def listar_eventos(service, calendar_id, name):
    events_result = service.events().list(
        calendarId=calendar_id, maxResults=10
    ).execute()
    events = events_result.get('items', [])
    
    if not events:
        st.write("No hay eventos en este calendario.")
    else:
        st.write(f"Eventos en el calendario {name}:")
        for event in events:
            st.write(f"- {event.get('summary', 'Sin título')} ({event.get('start')})")



def crear_evento(service, calendar_id, summary, start_time, end_time):
    # Convertir date a datetime (si es necesario)
    if not isinstance(start_time, datetime):
        start_time = datetime.combine(start_time, time(8, 0))  # 08:00 AM
    if not isinstance(end_time, datetime):
        end_time = datetime.combine(end_time, time(9, 0))      # 09:00 AM

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/Bogota',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/Bogota',
        },
        'description': "Descripción del evento de prueba",
    }

    try:
        created_event = service.events().insert(
            calendarId=calendar_id, body=event
        ).execute()
        st.success(f"✅ Evento creado: {created_event.get('htmlLink')}")
    except Exception as e:
        st.error(f"❌ Error al crear el evento: {e}")
    except HttpError as e:
        st.error(f"Error al crear el evento: {e}")
    except Exception as e:
        st.error(f"Error inesperado al crear el evento: {e}")

