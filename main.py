from  funciones import *

usuariosDeInstagram = contar_archivos_txt("C:\\Users\\querolol\\Desktop\\ScrapperSeguidores\\ScrapperIG\\instagramUser" )
contadorDeExcelsIg = usuariosDeInstagram

 
# Para IG
for i in (1,usuariosDeInstagram):
    #usuarios_a_buscar
    ruta_completa = os.path.join(os.getcwd(), "C:\\Users\\querolol\\Desktop\\ScrapperSeguidores\\ScrapperIG\\UsuariosABuscar.txt")
    # Abre el archivo de texto en modo lectura
    with open(ruta_completa, "r") as archivo:
        usuariosABuscar = []
        # Itera sobre cada línea del archivo
        for linea in archivo:
            # Elimina espacios en blanco al principio y al final de la línea
            usuario = linea.strip()
            # Agrega el usuario a la lista
            usuariosABuscar.append(usuario)


    # Obtén la ruta completa al archivo de texto
    ruta_completa = os.path.join(os.getcwd(), "C:\\Users\\querolol\\Desktop\\webScrapper\\WebScraperDanone\\instagram\\instagramUser\\instagramUser"+ str(i) +".txt")
    f = open(ruta_completa, "r")
    us = f.readline().strip()
    pas = f.readline().strip()
    driver = Ingresar_a_instagram(us,pas) 

    buscarUsuarios(driver,usuariosABuscar)
    cerrrarNavegador(driver)
 