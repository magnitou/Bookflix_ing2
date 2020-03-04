import requests
import json

api_reference = 'https://api-referencias.proyecto2019.linti.unlp.edu.ar'
api_google = 'https://www.googleapis.com/calendar/v3/calendars/es.ar%23holiday@group.v.calendar.google.com/events?key=AIzaSyCUVxxp1vm9vAmxLTjK61HSP78IYcnERAY'

def get_tipo_documentos():
    return requests.get(api_reference + '/tipo-documento').json()
    
def get_localidad():
    return requests.get(api_reference + '/localidad').json()
    
def get_feriados():
    crudes = requests.get(api_google).json()['items']
    feriados = []
    for i in range(len(crudes)):
        feriados.append({})
        feriados[i]['nombre'] = crudes[i]['summary']
        feriados[i]['inicio'] = crudes[i]['start']['date']
        feriados[i]['fin'] = crudes[i]['end']['date']
    return feriados


