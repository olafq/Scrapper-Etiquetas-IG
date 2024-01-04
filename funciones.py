import pandas as pd 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import os 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def contar_archivos_txt(ruta_carpeta):
    # Obtiene la lista de archivos en la carpeta especificada
    archivos = os.listdir(ruta_carpeta)
    # Inicializa un contador para archivos .txt
    contador = 0

    # Recorre la lista de archivos y cuenta los que tienen extensión .txt
    for archivo in archivos:
        if archivo.endswith(".txt"):
            contador += 1

    return contador

def inicializarChrome():
    ruta = os.getcwd()
    driver_path = os.path.join(ruta, 'chromedriver.exe')
    service = ChromeService(executable_path=driver_path)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")  # Opcional, maximiza la ventana del navegador al iniciar
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    return driver
    
def ingresar_us_cont(driver,us,pas):
    # Espera hasta que el elemento esté presente en la página
    wait = WebDriverWait(driver, 10)
    username_input = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    # Ingresa el nombre de usuario en el campo usuario de la web
    username_input.send_keys(us)
    # Espera hasta que el elemento esté presente en la página
    wait = WebDriverWait(driver, 10)
    username_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
    # Ingresa la contraseña en el campo contraseña de la web
    username_input.send_keys(pas)

#funcion que ingresa usuario y contraseña del txt pasado para instagram
def Ingresar_a_instagram(us,pas): 
    #inicializo google 
    driver = inicializarChrome()
    #Iir a la pagina de instagram 
    driver.get('https://www.instagram.com/')
    ingresar_us_cont(driver,us,pas)
    #inicia sesion 
    esperar_elemento(driver, By.XPATH, '//button[@class=" _acan _acap _acas _aj1- _ap30" and @type="submit"]').click()
    #clickea el boton de ahora no
    esperar_elemento(driver, By.XPATH, '//div[@class="_ac8f"]').click()
    #clickea el boton de no recibir notificaciones
    esperar_elemento(driver,By.XPATH,'//button[@class="_a9-- _ap36 _a9_1"]').click()
    return driver

def Ingresar_a_buscador(driver):
    time.sleep(5)
    buscador = esperar_elementos(driver, By.XPATH,'//a[@href = "#"]')
    time.sleep(5)
    buscador[0].click()

# funcion que Cierra el navegador
def cerrrarNavegador(driver):
    driver.quit()
def buscarUsuarios(driver,usuariosABuscar):
    fechas = []
    usuarios = []
    cantidadSeguidores = []
    cantidadSeguidos = []
    cantidadPosteos = []
    # Define una variable para realizar seguimiento de la cantidad de elementos antes del scroll
    element_count = 0
    usuariosABuscar = [elemento for elemento in usuariosABuscar if elemento]
    for usuario in usuariosABuscar:
        driver.get("https://www.instagram.com/"+str(usuario)+"/")
        time.sleep(10)
        cantSeguidos, cantSeguidores, CantPosteos = obtener_cantidad_de_Etiquetas(driver)
        fechas.append(datetime.now().strftime("%Y-%m-%d"))
        usuarios.append(usuario)
        cantidadSeguidores.append(cantSeguidores)
        cantidadSeguidos.append(cantSeguidos)
        cantidadPosteos.append(CantPosteos)
        time.sleep(5)
    # Crear un DataFrame
    data = {'fecha':fechas,'Usuario':usuarios, 'cant_seguidores': cantidadSeguidores, 'cant_seguidos': cantidadSeguidos, 'cant_posteos': cantidadPosteos}
    # vamos a la ruta que queremos 
    nombre_carpeta = "warbuef001\schain-danone\\1. BI\\Analytics\\webScrapper\\WebScraperDanone\\Instagram\\EtiquetasUsuarios"
    generarDF(data,'etiquetasDeLosUsuarios.xlsx',nombre_carpeta)

def generarDF(data,nombreArchivo,nombre_carpeta):
    df = pd.DataFrame(data)
    ruta_actual = os.getcwd()
    ruta_a_crear_el_excel = os.path.join(ruta_actual, nombre_carpeta)
    with pd.ExcelWriter(ruta_a_crear_el_excel, engine='openpyxl', mode='a') as writer:
    # Si el archivo no existe, lo creamos y escribimos el DataFrame
        if not os.path.isfile(ruta_a_crear_el_excel):
            df = pd.DataFrame(data)
            df.to_excel(writer, index=False)
        else:
            # Si el archivo ya existe, simplemente escribimos el DataFrame al final
            df = pd.DataFrame(data)
            df.to_excel(writer, index=False, header=False)
#DONE
def obtener_cantidad_de_Etiquetas(driver):
    time.sleep(5)
    # toma una lista de la cantida de publicaciones, seguidres y seguidos
    info_user = esperar_elementos(driver,By.CLASS_NAME,'_ac2a')
    # se queda con la cantidad de seguidores el 2 elemento de la lista 
    seguidos = info_user[0].text 
    seguidores = info_user[1].text
    posteos = info_user[2].text

    return  seguidos, seguidores, posteos
       
    
def esperar_elemento(driver, by, selector, tiempo_espera=200):
    return WebDriverWait(driver, tiempo_espera).until(
        EC.presence_of_element_located((by, selector))
    )

def esperar_elementos(driver, by, selector, tiempo_espera=60):
    return WebDriverWait(driver, tiempo_espera).until(
        EC.presence_of_all_elements_located((by, selector))
    )