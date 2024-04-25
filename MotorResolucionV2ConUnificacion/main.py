import re
#Cosas para leer la informacion de los archivos
#Leer lineas del archivo
def leer_archivo():
    with open("MarcoCesar/Logico.txt", "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        archivo.close()
    return lineas
#Clasificación de la información del archivo inicial
def analizar_informacion(lineas):
    Constantes = []
    Predicados = []
    BaseCon = []
    Pregunta = ""
    Negacion = ""

    for linea in lineas:
        
        linea = linea.strip()
        if(linea.startswith("#")):
            partes = linea.split("#")
            categoria = partes[1]
        else:
            if (categoria == "Constantes"):
                Constantes.append(linea)
            elif (categoria == "Predicados"):
                Predicados.append(linea)
            elif (categoria == "Base de conocimiento"):
                BaseCon.append(linea)
            elif (categoria == "Pregunta"):
                Pregunta = linea
            elif (categoria == "Negación"):
                Negacion = linea

    return Constantes, Predicados, BaseCon, Pregunta, Negacion
#Lectura del archivo de reglas
def reglas_simp():
        diccionario = {}
        contador = 0

        with open("LogPrimOrden.txt", "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                linea = linea.strip()
                if(linea.startswith("#")):
                    nombre = ""
                    reglas = []
                    resultados = []
                    partes = linea.split("#")
                    nombre = partes[1]
                    contador = 1
                    continue
                elif(contador == 1):
                    reglas.append(linea)
                    contador = 2
                    continue
                elif(contador == 2):
                    resultados.append(linea)
                    contador = 1
                diccionario[nombre] = [reglas, resultados]
        archivo.close()
        return diccionario

#Cosas meramente del proyecto 'V'-Proceso de unificación de variables
def unificacion(base):
    #primero encuento a aquellos que ya sean constantes en la base
    constantes = []
    #Para eso, obtengo los valores que esten dentro de () y si unicamente contienen constantes, los añado
    for linea in base:
        if not re.search(r'\b[x|y]\d+\b', linea):
            constantes.append(linea)

    nuevas_lineas_base = []

    for constante in constantes:
        cte = re.search(r'(.+?)(?=\()', constante).group(1)
        pattern_single = rf'{cte}\((.*?)\)'  # Regex para un valor dentro de los paréntesis
        pattern_double = rf'{cte}\((.*?),(.*?)\)'  # Regex para dos valores dentro de los paréntesis
        
        for linea in base:
            if constante != linea:
                match_single = re.search(pattern_single, linea)
                match_double = re.search(pattern_double, linea)
                

                linea_modificada = linea

                if match_double:
                    valor_x = match_double.group(1)
                    valor_y = match_double.group(2)

                    linea_modificada = linea.replace(f"{cte}({valor_x},{valor_y})", constante)

                    linea_modificada = linea_modificada.replace(valor_x, "Marco").replace(valor_y, "Cesar")
                    #nuevas_lineas_base.append(linea_modificada)
                elif match_single:
                    valor_x = match_single.group(1)

                    linea_modificada = linea.replace(f"{cte}({valor_x})", constante)

                    linea_modificada = linea_modificada.replace(valor_x, "Marco")
                    #nuevas_lineas_base.append(linea_modificada)

                if not re.search(r'\(.*[xy].*\)', linea_modificada):  # Verifica si no hay 'x' o 'y' entre paréntesis
                    if linea_modificada not in nuevas_lineas_base:
                        nuevas_lineas_base.append(linea_modificada)  # Si no se encuentra todavia en la nueva base para no tener duplicados


    # Actualizar la base de conocimiento con las nuevas líneas modificadas
    lineas_base = nuevas_lineas_base
    lineas_base.append('¬Romano(Marco)∨Leal(Marco,Cesar)∨Odia(Marco,Cesar)')

    return lineas_base

#Simplificar información de la base de conocimiento eliminando para todo y para alguno
def quitarAyE(base):
    limpio = []
    for i in range(0,len(base)):
        if "∀" in base[i] or "∃" in base[i] :
            nuevoi=base[i][2:]
            if "∀" in nuevoi or "∃" in nuevoi :
                nuevoi=nuevoi[2:]
                base[i]=nuevoi
            else:
                base[i]=nuevoi
    return base    

#Eliminacion de parentesis cuando tienen antes una negación y cuando no
def quitarParentesis(base):

    for i in range(0,len(base)):
 
        if "[" in base[i]:
            if "¬[" in base[i]:
                base[i]=base[i].replace('¬[','¬')
                base[i]=base[i].replace('∧','∨¬')
            else:
                base[i]=base[i].replace('[','')
            
            base[i]=base[i].replace(']','')
    
    return base

#Eliminación por implicación--------------------------------
def conv_FNC(base,reglas):
    for i in range(0,len(base)):
        if "⇒" in base[i]:
            antecedente, consecuente = base[i].split("⇒")
            antecedente = antecedente.strip()
            consecuente = consecuente.strip()
            base[i]=f"¬{antecedente}∨{consecuente}"
    return base



#Proceso de comprobación por refutación-----------------
def actualizar(elem,base,lista):
    print(f"Elem: {elem}")
    if elem.startswith("¬"):
        for i in base:
            if elem[1:] in i:
                print(f"\x1b[1;33mEncontro {elem} en {i} \x1b[0;37m \n")
                nuevaInfo=i.replace(elem[1:],'')
                nuevaInfo = re.split(r'∧|∨', nuevaInfo)
                nuevaInfo = list(filter(bool, nuevaInfo))
                if len(lista)>0:
                    lista.remove(elem)                
                for item in reversed(nuevaInfo):
                    lista.insert(0, item)
                base.remove(i)
                break

    else:
        for i in base:
            if "¬"+elem in i:
                print(f"\x1b[1;33mEncontro {elem} en {i} \x1b[0;37m \n")
                nuevaInfo=i.replace("¬"+elem,'')
                nuevaInfo = re.split(r'∧|∨', nuevaInfo)
                nuevaInfo = list(filter(bool, nuevaInfo))
                if len(lista)>0:
                    lista.remove(elem)
                for item in reversed(nuevaInfo):
                    lista.insert(0, item)
                base.remove(i)                
                break

    return lista,base

def operar(base,negacion,Pregunta):

    print(f"Elemento: {negacion}")


    lista = []
    lista,base=actualizar(negacion,base,lista)

    while True:
        print(f"Nuevos elementos de la lista: {lista}")
        if len(lista) == 0:
            print(f"Se ha realizado la comprobación por refutación")
            print(f"Por lo tanto: {Pregunta} es VERDADERA")
            break
        if len(lista) != 0 and len(base) ==0:
            print("No se ha logrado realizar la comprobación y ya no hay mas informacion en la base de conocimiento")
            print(f"Por lo tanto: {Pregunta} es FALSA")
            break
        else:
            lista,base=actualizar(lista[0],base,lista)
#Main-------------------------
if __name__ == '__main__':
    lineas = leer_archivo()
    Constantes, Predicados, BaseCon, Pregunta, Negacion = analizar_informacion(lineas)
    reglas = reglas_simp()
    nuevaBase = quitarAyE(BaseCon)
    nuevaBase = conv_FNC(nuevaBase,reglas)
    baseFinal=quitarParentesis(nuevaBase)
    base = unificacion(baseFinal)
    
    print("BASE DE CONOCIMIENTOS INICIAL: ")
    for i in BaseCon:
        print(i)
    print("------------------------------------------------")
    print("BASE DE CONOCIMIENTOS DESPUÉS DE PROCESO DE UNIFICACIÓN: ")
    for i in base:
        print(i)
    print("------------------------------------------------")
    operar(base,Negacion,Pregunta)