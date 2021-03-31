import os

def init():
    print ('***Administrar archivos y carpetas***')
    opcion = raw_input('Seleccione una opcion, a=crear y e=eliminar:')
    if (opcion == "a"):
        ruta=raw_input('Indique la ruta, si no la indica sera la actual:')
        if(ruta == ""): ruta = os.getcwd()
        #comprobar si la ruta existe
        if(os.path.isdir(ruta)):
            tipo=raw_input("Indique el tipo: a=archivo y c=carpeta ")
            if (tipo=="a"):
                archivo=raw_input("Indique el nombre del archivo: ")
                #crear archvo en la ruta indicada
                manejador=open(ruta+archivo, "w")
                manejador.close()
                print "Archivo ",archivo," craedo con exito"
            elif(tipo=="c"):
                carpeta=raw_input("Indique el nombre de la carpeta: ")
                #crear carpeta
                os.mkdir(ruta+carpeta)
                print "Carpeta ",carpeta," creada con exito."
            else: init()
            
    elif (opcion== "e"):
        ruta=raw_input("Indique la ruta, si no la indica sera la actual")
        if (ruta==''):ruta=os.getcwd()
        eliminar=raw_input("Indique el nombre de la carpeta o archivo a eliminar")
        #si es un archivo
        if (os.path.isfile(ruta+eliminar)):
            os.remove(ruta+eliminar)
            print "Archivo ",eliminar," eliminado con exito."
        #si es una carpeta
        elif (os.path.isdir(ruta+eliminar)):
            os.rmdir(ruta+eliminar)
            print "Carpeta ",eliminar," con exito."
        else: init ()#Reiniciar el programa
    
    else: init()#reiniciar el programa nuevamenta
    
#llamar a la funcion