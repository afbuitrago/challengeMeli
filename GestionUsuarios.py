#Libreria para solicitud segura de pass
from getpass import getpass
#Libreria para expresiones regulares
import re
#Libreria para generación de hash
import hashlib
#Libreria para generar valores random
import random
#Libreria para manipulación de archivos formato json
import json

#Funcion de creacion de usuarios
def crearUsuario():
    #Solicitar usuario
    nombreUsuario = input("Ingresa el nombre del usuario: ")
    print("Tener en cuenta que debera ingresar una contrasena de minimo 12 caracteres que tenga mayusculas, minusculas, digitos y por lo menos uno de los siguientes caracteres: /*-+!#$&=?¡_.,;@")
    print("Ingresa la contrasena para ",nombreUsuario)
    #Solicitar pass de forma segura
    passUsuario = getpass()
    #Validara si el pass cumple con los paramtros minimos de seguridad requeridos
    if(validarCompPass(passUsuario)==True): 
        #Validara si el usuario no existe y permite crearlo   
        if(lectorUsuarios(nombreUsuario) == 1):
            #Genera un salt de seguridad para el pass
            saltPass = generarSalt()
            #Unifica password del usuario y salt y posterior genera el hash en sha256
            hashPassSalt = saltPass+passUsuario+saltPass
            hash = generarHash(hashPassSalt)
            print("Ingresa el valor numerico del rol del usuario: \n","1. Administradores \n","2. Cartera \n","3. Reportes \n")
            #Solicita el grupo al que correspondera el usuario
            numeroGrupo = input()
            if (numeroGrupo == "1"):
                grupoUsuario = "Administradores"
            elif (numeroGrupo == "2"):
                grupoUsuario = "Cartera"
            elif (numeroGrupo == "3"):
                grupoUsuario = "Reportes"
            else: print("Ingreso un valor invalido")     

            print("Se creara el usuario ",nombreUsuario," en el grupo ",grupoUsuario)    
            #Variable que se agregara al diccionario en formato json con los datos del nuevo usuario
            datos = {"usuario":nombreUsuario,"salt":saltPass,"pass":hash,"grupo":grupoUsuario}

            #Lectura del diccionario y adicion de nuevo usuario al diccionario    
            with open("grupos_usuarios.json",'r') as fichero_1:
                usuarios_dic = json.load(fichero_1)
                usuarios_dic.append(datos)
            
            #Escritura del diccionario con el nuevo usuario
            with open("grupos_usuarios.json",'w') as fichero_1:
                json.dump(usuarios_dic, fichero_1, indent=4, sort_keys=True)
        else: print("El usuario ya existe")
    else:print("La contrasena no cumple con los parametros de seguridad")

#Funcion de validación de parametros minimos de seguridad
def validarCompPass(passUsuario):
    #Validar longitud minima requerida
    if len(passUsuario) >= 12:
        #Validar uso de mayusculas y minusculas
        if re.search('[a-z]',passUsuario) and re.search('[A-Z]',passUsuario):
            #Validar uso de digitos
            if re.search('[0-9]',passUsuario):
                #Validar uso de caracteres especiales
                if re.search('[/*-+!#$&=?¡_.,;@]',passUsuario):
                    return True
    return False

#Funcion de busqueda de usuarios existentes
def lectorUsuarios(nombreUsuario):
    #Apertura de diccionario con usuarios
    fichero_1 = open('grupos_usuarios.json')
    usuarios_dic = json.load(fichero_1)
    permitido = 0
    #Busqueda de usuario
    for usuario_dic in usuarios_dic:
        usuariof = usuario_dic.get('usuario')
        if(nombreUsuario == usuariof):
            permitido = 0
            break
        else: permitido = 1
    return permitido

#Funcion de generación de salt aleatorio
def generarSalt():
    #Lista de caracteres para generar salt
    CARACTERES = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/*-+!#$&=?¡_.,;@"
    lista=[]
    for i in range(16):
        lista.append(random.choice(CARACTERES))
    return(''.join(lista))

#Funcion de generacion de hash
def generarHash(hashPassSalt):
    #Definicion de hash a utilizar
    hashSha2 = hashlib.sha256()
    #Generación de hash del valor hashPassSalt
    hashSha2.update(hashPassSalt.encode())
    return hashSha2.hexdigest()


#Funcion eliminación de usuarios
def eliminarUsuario():
    fichero_1 = open('grupos_usuarios.json')
    usuarios_dic = json.load(fichero_1)
    conta = 0
    #Asignación de id para poder identificar usuario en diccionario
    for usuario_dic in usuarios_dic:
        usuariof = usuario_dic.get('usuario')
        print('id:',conta,'_______usuario:',usuariof)
        conta+=1
    #Solicitud de id del usuario a eliminar    
    idUsuario = input("Ingresa el id del usuario a eliminar: ")
    #Lee archivo y se guarda valor id de usuario a eliminar en variable idUsuario
    with open("grupos_usuarios.json",'r') as fichero_1:
            usuarios_dic = json.load(fichero_1)
            usuarios_dic.pop(int(idUsuario))
    #Escribe el archivo con la actualización del usuario eliminado    
    with open("grupos_usuarios.json",'w') as fichero_1:
            json.dump(usuarios_dic, fichero_1, indent=4, sort_keys=True)
            print("Usuario Eliminado")
    
#Inicio de API
if __name__ == '__main__':
#Solicitar acciones a realizar con usuarios
    entrada = input("Ingrese 1 para crear usuario, 2 para eliminar usuario: ")
    if(entrada == "1"):
        crearUsuario()
    if(entrada == "2"):
        eliminarUsuario()
    else: 
        print("Salido")
