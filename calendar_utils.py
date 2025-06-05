import streamlit as st
from google.oauth2 import service_account
import asyncio
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, time, timedelta



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


def crear_evento(service, calendar_id, events, fecha_inicio, fecha_fin):
    dias_semana_map = {
        "LUNES": 0,
        "MARTES": 1,
        "MIERCOLES": 2,
        "JUEVES": 3,
        "VIERNES": 4,
        "SABADO": 5,
        "DOMINGO": 6
    }

    mensaje_estado = st.empty()
    mensaje_estado.info("⏳ Procesando datos...")

    eventos_creados = 0

    for idx, row in events.iterrows():
        try:
            start_time = datetime.strptime(str(row['Start Time']), "%H:%M").time()
            end_time = datetime.strptime(str(row['End Time']), "%H:%M").time()

            dias_evento = [dias_semana_map[d.strip()] for d in row["Days"].split(",")]

            current_date = fecha_inicio
            while current_date <= fecha_fin:
                if current_date.weekday() in dias_evento:
                    start_datetime = datetime.combine(current_date, start_time).isoformat()
                    end_datetime = datetime.combine(current_date, end_time).isoformat()

                    event = {
                        'summary': row["SUBJECT"],
                        'start': {
                            'dateTime': start_datetime,
                            'timeZone': 'America/Bogota',
                        },
                        'end': {
                            'dateTime': end_datetime,
                            'timeZone': 'America/Bogota',
                        },
                        'description': row["Location"]
                    }

                    service.events().insert(
                        calendarId=calendar_id, body=event
                    ).execute()

                    eventos_creados += 1
                    mensaje_estado.info(f"⏳ Procesando datos... ({eventos_creados} eventos creados)")

                current_date += timedelta(days=1)

        except ValueError as ve:
            st.error(f"❌ Error de formato: {ve}")
        except Exception as e:
            st.error(f"❌ Error al crear el evento: {e}")

    mensaje_estado.success(f"✅ Eventos creados exitosamente. Total: {eventos_creados}")

    
def listar_horas(events):
    st.info("Horas iniciales:")
    for hora in events['Start Time']:
        st.write(f"- {hora}")
                
    st.info("Horas finales:")
    for hora in events['End Time']:
        st.write(f"- {hora}")


