#Libreria para generación de hash
import hashlib
#Libreria para manipulación de archivos formato json
import json
#Libreria para solicitud segura de pass
from getpass import getpass
#Libreria que permitira conexion a BD
import mysql.connector
from mysql.connector import Error

#funcion de requerimientos de usuario y contrasena
def solicitarCredenciales():
    nombreUsuario = input("Ingresa tu usuario: ")
    passUsuario = getpass("Ingresa tu contrasena: ")
    #Paso de parametros a validar
    lectorGruposUsuarios(nombreUsuario, passUsuario)

#Funcion que validara valores ingresados
def lectorGruposUsuarios(nombreUsuario, passUsuario):
    #Abrir diccionario de usuarios
    with open("grupos_usuarios.json") as fichero_1:
    #fichero_1 = open('./grupos_usuarios.json')
        usuarios_dic = json.load(fichero_1)
        for usuario_dic in usuarios_dic:
            #Guardar todos los valores del usuario consultado en variables  
            salt = usuario_dic.get('salt')
            grupof = usuario_dic.get('grupo')
            usuariof = usuario_dic.get('usuario')
            passwdf = usuario_dic.get('pass')
            
            #Validar existencia de usuario
            if(nombreUsuario == usuariof):
                #Calcular valores de salt mas password 
                saltPass = salt+passUsuario+salt
                #Uso de hash 256
                hashSha2 = hashlib.sha256()
                #Generar hash de saltPass calculado
                hashSha2.update(saltPass.encode())
                #Validar si has de saltPass coincide con datos del usuario en diccionario
                if(hashSha2.hexdigest() == passwdf):
                    print("Acceso correcto")
                    #Identificacin del grupo al que pertenece el usuario para lectura de la BD y envio a funcion de consulta
                    envioQuery(grupof)
                #Si pass no coincide termine    
                if(hashSha2 != passwdf):
                    print("Por favor validar credenciales de acceso")
                    break

#Funcion de consulta segun grupo
def envioQuery(grupof):
    #Archivo que contiene clave de acceso de usuario autorizado a BD (archivo protegido desde sistema base)
    fichero_1 = open('./clave_db.txt', mode="r")
    contrasena_db = fichero_1.read()
    
    #Intente coneccion a BD con los parametros definidos
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                             port=3306,
                                             database='ML_DB',
                                             user='root',
                                             password=contrasena_db,
                                             #ssl_ca="ca.pem", 
                                             #ssl_verify_cert=True
                                             )
        #Si el grupo es administradores, realice query con contraseña cargada desde archivo protegido para descifrado de todos los datos
        if(grupof=="Administradores"):
            #Archivo que contiene llave de cifrado de datos sensibles (archivo protegido desde sistema base)
            fichero_2 = open('./clave_datos_sensibles.txt', mode="r")
            contrasena = (fichero_2.read()).strip()
            sql_select_Query = 'SELECT id, user_name, fec_alta, codigo_zip, aes_decrypt(unhex(credit_card_num),"'+contrasena+'"), aes_decrypt(unhex(credit_card_ccv),"'+contrasena+'"), aes_decrypt(unhex(cuenta_numero),"'+contrasena+'"), aes_decrypt(unhex(direccion),"'+contrasena+'"), aes_decrypt(unhex(geo_latitud),"'+contrasena+'"), aes_decrypt(unhex(geo_longitud),"'+contrasena+'"), color_favorito, aes_decrypt(unhex(foto_dni),"'+contrasena+'"), aes_decrypt(unhex(ip),"'+contrasena+'"), auto, auto_modelo, auto_tipo, auto_color, cantidad_compras_realizadas, avatar, fec_birthday FROM ml_tb'
        #Si el grupo es cartera, realice query con contraseña cargada desde archivo protegido para descifrado de algunos datos
        if(grupof=="Cartera"):
            #Archivo que contiene llave de cifrado de datos sensibles (archivo protegido desde sistema base)
            fichero_2 = open('./clave_datos_sensibles.txt', mode="r")
            contrasena = (fichero_2.read()).strip()
            sql_select_Query = 'SELECT id, user_name, fec_alta, codigo_zip, credit_card_num, credit_card_ccv, cuenta_numero, aes_decrypt(unhex(direccion),"'+contrasena+'"), aes_decrypt(unhex(geo_latitud),"'+contrasena+'"), aes_decrypt(unhex(geo_longitud),"'+contrasena+'"), color_favorito, aes_decrypt(unhex(foto_dni),"'+contrasena+'"), aes_decrypt(unhex(ip),"'+contrasena+'"), auto, auto_modelo, auto_tipo, auto_color, cantidad_compras_realizadas, avatar, fec_birthday FROM ml_tb'
        #Si el grupo es reportes, realice query sin contraseña, todos los datos los devolvera cifrados
        if(grupof=="Reportes"):
            sql_select_Query = 'SELECT id, user_name, fec_alta, codigo_zip, credit_card_num, credit_card_ccv, cuenta_numero, direccion, geo_latitud, geo_longitud, color_favorito, foto_dni, ip, auto, auto_modelo, auto_tipo, auto_color, cantidad_compras_realizadas, avatar, fec_birthday FROM ml_tb'
        

        cursor = connection.cursor()
        #Envie la variable de la query cargada segun grupo
        cursor.execute(sql_select_Query)
        #Envie la consulta a todos los registros de la BD
        records = cursor.fetchall()
    
        print("Numero total de registros en la tabla: ", cursor.rowcount)

        #Retorne la consulta de cada regitro con su respectiva informacion
        print("\nPrinting each row")
        for row in records:
            print("Id = ", row[0], )
            print("User name = ", row[1])
            print("Fecha alta  = ", row[2])
            print("Codigo Zip = ", row[3], )
            print("Numero TC = ", row[4])
            print("CVV TC  = ", row[5])
            print("Numero Cuenta = ", row[6], )
            print("Direccion = ", row[7])
            print("Latitud  = ", row[8])
            print("Longitud = ", row[9], )
            print("Color Favorito = ", row[10])
            print("Foto DNI  = ", row[11])
            print("IP = ", row[12], )
            print("Auto = ", row[13])
            print("Modelo Auto  = ", row[14])
            print("Tipo Auto = ", row[15], )
            print("Color Auto = ", row[16])
            print("Cantidad compras realizadas  = ", row[17])
            print("Avatar = ", row[18], )
            print("Fecha cumpleanos  = ", row[19], "\n")
            #break

    #En caso de que no conecte
    except mysql.connector.Error as error:
        print("Error mientras conectaba a MySQL {}".format(error))
    #Finalmente cierre conexion
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("Conexion a MySQL fue cerrada")

#Inicio de API
if __name__ == '__main__':
    #Funcion de autenticacion
    solicitarCredenciales()