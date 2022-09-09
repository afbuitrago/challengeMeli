#Librerias que permitira conexion a pagina web y BD
from multiprocessing import connection
from urllib.request import urlopen
import mysql.connector
from mysql.connector import Error
#Librerias de manipulacion archivos json
import json

#Funcion que guarda los datos en variable
def descargar_datos(sitioUrl):
    consulta = urlopen(sitioUrl)
    return consulta

#Funcion que trata los datos como formato json y los envia uno a uno a funcion de carga a base de datos
def leer_datos(datos):
    datos_json = json.loads(datos.read())
    contador = 1
    for usuario_dic in datos_json:
        conector_mysql(usuario_dic)
        #break

#Funcion encargada de carga de datos json a base de datos
def conector_mysql(usuario_dic):
    #Archivo que contiene clave de acceso de usuario autorizado a BD (archivo protegido desde sistema base)
    fichero_1 = open('./clave_db.txt', mode="r")
    #Archivo que contiene llave de cifrado de datos sensibles (archivo protegido desde sistema base)
    fichero_2 = open('./clave_datos_sensibles.txt', mode="r")
    
    #Almacenamiento de datos de forma independiente de cada objeto para carga en la BD
    idUsuario = usuario_dic.get('id')
    nombreUsuario = usuario_dic.get('user_name')
    fechaAlta = usuario_dic.get('fec_alta')
    codigoZip = usuario_dic.get('codigo_zip')
    tarjetaCreditoNum = usuario_dic.get('credit_card_num')
    tarjetaCreditoCCV = usuario_dic.get('credit_card_ccv')
    cuentaNumero = usuario_dic.get('cuenta_numero')
    direccion = usuario_dic.get('direccion')
    geoLatitud = usuario_dic.get('geo_latitud')
    geoLongitud = usuario_dic.get('geo_longitud')
    colorFavorito = usuario_dic.get('color_favorito')
    fotoDNI = usuario_dic.get('foto_dni')
    direccionIP = usuario_dic.get('ip')
    auto = usuario_dic.get('auto')
    autoModelo = usuario_dic.get('auto_modelo')
    autoTipo = usuario_dic.get('auto_tipo')
    autoColor = usuario_dic.get('auto_color')
    cantidadComprasRealizadas = usuario_dic.get('cantidad_compras_realizadas')
    avatar = usuario_dic.get('avatar')
    fechaCumple = usuario_dic.get('fec_birthday')
    #Variables de contrasenas de cifrado y acceso a BD
    contrasena_db = fichero_1.read()
    contrasena = fichero_2.read()
    
    #Intente conexion a BD bajo losparametros enviados
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                             port=3306,
                                             database='ML_DB',
                                             user='root',
                                             password=contrasena_db,
                                             #ssl_ca="ca.pem", 
                                             #ssl_verify_cert=True
                                             )
        
        #Si realiza la conexion de forma satisfactoria 
        if connection.is_connected():
            cursor = connection.cursor()
            #Query construida para enviar datos sensibles ajo cifrado aes que sera procesado directamente en la BD
            sqlQuery = 'INSERT INTO ml_tb (id, user_name, fec_alta, codigo_zip, credit_card_num, credit_card_ccv, cuenta_numero, direccion, geo_latitud, geo_longitud, color_favorito, foto_dni, ip, auto, auto_modelo, auto_tipo, auto_color, cantidad_compras_realizadas, avatar, fec_birthday) VALUES (%s, %s, %s, %s, hex(aes_encrypt(%s,"'+contrasena+'")), hex(aes_encrypt(%s,"'+contrasena+'")), hex(aes_encrypt(%s,"'+contrasena+'")), hex(aes_encrypt(%s,"'+contrasena+'")), hex(aes_encrypt(%s,"'+contrasena+'")), hex(aes_encrypt(%s,"'+contrasena+'")), %s, hex(aes_encrypt(%s,"'+contrasena+'")), %s, %s, %s, %s, %s, %s, %s, %s)'
            #Variables enviadas que se ajustaran a cada uno de los valores %s de la query
            record = (idUsuario, nombreUsuario, fechaAlta, codigoZip, tarjetaCreditoNum, tarjetaCreditoCCV, cuentaNumero, direccion,geoLatitud, geoLongitud, colorFavorito, fotoDNI, direccionIP, auto, autoModelo, autoTipo, autoColor, cantidadComprasRealizadas, avatar, fechaCumple)
            cursor.execute(sqlQuery, record)
            connection.commit()
            print("Datos cargados de forma correcta")
            
    #Si falla conexion a BD
    except mysql.connector.Error as error:
        print("Error mientras conectaba a MySQL {}".format(error))

    #Si conecto y termino tarea finalice
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexion a MySQL fue cerrada")

#Inicio de API
if __name__ == '__main__':
#Carga de URL dispuesta por MELI con info en formato json
    sitioUrl = 'https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios'
#Envio de URL en variable para generar descarga de info
    leer_datos(descargar_datos(sitioUrl))