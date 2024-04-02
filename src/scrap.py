from bs4 import BeautifulSoup
import requests

# Variables globables
HEADER = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'

def getHTTPResponse(url, headers = None, responseType = 'page', verbose = False, debug = False):
    """ Obtengo la respuesta HTML de una URL.
        Le puedo pasar headers a la funcion, si no le paso ninguno
        toma algunos por defecto.
        La funcion ya pasa el resultado HTML a un objeto de Beautiful Soup.
    """

    # Definimos los headers
    if headers == None:
        headers = {
            'user-agent' : HEADER
        }

    # Realizamos una solicitud a la página web
    response = requests.get(url, headers = headers)

    # Debug
    if debug is True:
        print('HTTP response:\n',response)

    # Analizamos el contenido HTML de la página web utilizando BeautifulSoup
    page = BeautifulSoup(response.content, 'html.parser')

    # Muestro los datos en pantalla
    if verbose is True:
        print('Ejecutando la funcion getHTTPResponse() ...')
        print('\t- URL:', url)
        print('\t- OK:', response.ok)
        print('\t- Cogido recibido:', response.status_code)
        print('')

    # Validation check
    if response.ok == True:
        if responseType == 'text':
            return response.text
        else:
            return page
    else:
        print('')
        print('\tERROR! Ocurrio un error inesperado al cargar la URL seleccionada')
        print('\t- URL:', url)
        print('\t- OK:', response.ok)
        print('\t- Cogido recibido:', response.status_code)
        print('')
        return False

if __name__ == "__main__":
    
    # Obtengo el contenido HTML del clima de Google
    page = getHTTPResponse("https://www.google.com/search?q=clima", responseType='page')
    
    # Busco la temperatura
    temp = float( page.find('span', class_='wob_t q8U8x').text )
    
    # Verifico si hay lluvia
    rain_txt = page.find('img', class_='wob_tci')['src']
    rain = True if 'rain' in rain_txt else False
    
    # Muestro los datos
    print( f'Temperatura: {temp}' )
    print( f'Lluvia: {rain}' )