import re

def leer_archivo():
    with open("MarcoCesar/Logico.txt", "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        archivo.close()
    return lineas

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



#-------------------------------
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

def operar(Constantes,base,negacion,pregunta):

    print(f"Elemento: {negacion}")


    lista = []
    lista,base=actualizar(negacion,base,lista)

    while True:
        print(f"Nuevos elementos de la lista: {lista}")
        if len(lista) == 0:
            print(f"Se ha realizado la comprobación por refutación")
            break
        if len(lista) != 0 and len(base) ==0:
            print("No se ha logrado realizar la comprobación y ya no hay mas informacion en la base de conocimiento")
            break
        else:
            lista,base=actualizar(lista[0],base,lista)

if __name__ == '__main__':
    lineas = leer_archivo()
    Constantes, Predicados, BaseCon, Pregunta, Negacion = analizar_informacion(lineas)
    reglas = reglas_simp()
    nuevaBase = quitarAyE(BaseCon)
    nuevaBase = conv_FNC(nuevaBase,reglas)
    baseFinal=quitarParentesis(nuevaBase)
    operar(Constantes,baseFinal,Negacion,Pregunta)