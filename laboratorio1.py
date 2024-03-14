#import graphviz
import os
from collections import deque
from typing import Any, List, Optional, Tuple

class NodoArbol:
    def __init__(self, tipo, numero):
        self.tipo = tipo
        self.numero = numero
        self.nombre_archivo = self.generar_nombre_archivo()
        self.size = self.obtener_tamano_archivo()
        self.left = None
        self.right = None

    def generar_nombre_archivo(self):
        if self.tipo == "bike":
            return f"bike_{self.numero.zfill(3)}.bmp"
        elif self.tipo == "cars":
            return f"carsgraz_{self.numero.zfill(3)}.bmp"
        elif self.tipo == "cats":
            return f"cat.{self.numero}.jpg"
        elif self.tipo == "dogs":
            return f"dog.{self.numero}.jpg"
        elif self.tipo == "flowers":
            return f"{self.numero.zfill(4)}.jpg"
        elif self.tipo == "horses":
            return f"horse-{self.numero}.jpg"
        elif self.tipo == "human":
            return f"rider-{self.numero}.jpg"
        else:
            return None  # Manejar casos no válidos

    def obtener_tamano_archivo(self):
        ruta_archivo = os.path.join("data", self.tipo, self.nombre_archivo)
        if os.path.exists(ruta_archivo):
            return os.path.getsize(ruta_archivo)
        else:
            return None

class ArbolAVL:
    def __init__(self, root: NodoArbol = None):
        self.root = root

    def obtener_altura(self, nodo: NodoArbol) -> int:
        if nodo is None:
            return 0
        altura_izquierda = self.obtener_altura(nodo.left)
        altura_derecha = self.obtener_altura(nodo.right)
        return max(altura_izquierda, altura_derecha) + 1

    def simple_izquierda(self,nodo: NodoArbol):
        
        aux = nodo.right
        nodo.right = aux.left
        aux.left = nodo
        if(nodo == self.root):
            self.root= aux
            return aux
        return aux

    def simple_derecha(self,nodo: NodoArbol):
        aux = nodo.left
        nodo.left = aux.right
        aux.right = nodo
        if(nodo == self.root):
            self.root= aux
            return aux
        return aux
    
    def balancear(self, nodo: NodoArbol) -> NodoArbol:
        bal = self.obtener_altura(nodo.right) - self.obtener_altura(nodo.left)
        if bal == 2:
            if self.obtener_altura(nodo.right.left) == -1:
                nodo.right = self.simple_derecha(nodo.right)
                return self.simple_izquierda(nodo)
            else:
                return self.simple_izquierda(nodo)

        elif bal == -2:
            if self.obtener_altura(nodo.left.right) == 1:
                nodo.left = self.simple_izquierda(nodo.left)
                return self.simple_derecha(nodo)
            else:
                return self.simple_derecha(nodo)
        return nodo
    
    def search(self, nombre_archivo: str) -> Tuple[Optional[NodoArbol], Optional[NodoArbol]]:
        p, pad = self.root, None
        while p is not None:
            if nombre_archivo == p.nombre_archivo:
                return p, pad
            elif nombre_archivo < p.nombre_archivo:
                pad = p
                p = p.left
            else:
                pad = p
                p = p.right
        return p, pad
    
    def insert(self, tipo: str, numero: int) -> bool:
        to_insert = NodoArbol(tipo, numero)
        if self.root is None:
            self.root = to_insert
            print(f"Se insertó el nodo {to_insert.nombre_archivo}.")            
            return True
        else:
            p, pad = self.search(to_insert.nombre_archivo)
            if p is None:
                if to_insert.nombre_archivo < pad.nombre_archivo:
                    pad.left = to_insert
                else:
                    pad.right = to_insert
                print(f"Se insertó el nodo {to_insert.nombre_archivo}.")
                self.balancear(self.root)  # Balancear después de la inserción
                return True
            return False

    #Delete puede tener error
    def delete(self, tipo: str, numero: int, mode: bool = True) -> bool:
        nombre_archivo = NodoArbol(tipo, numero).nombre_archivo
        p, pad = self.search(nombre_archivo)
        if p is not None:
            if p.left is None and p.right is None:
                if p == pad.left:
                    pad.left = None
                else:
                    pad.right = None
                del p
                print(f"Se eliminó el nodo {nombre_archivo}.")
            elif p.left is not None and p.right is None:
                if p == pad.left:
                    pad.left = p.left
                else:
                    pad.right = p.left
                del p
                print(f"Se eliminó el nodo {nombre_archivo}.")
            elif p.left is None and p.right is not None:
                if p == pad.left:
                    pad.left = p.right
                else:
                    pad.right = p.right
                del p
                print(f"Se eliminó el nodo {nombre_archivo}.")
            else:
                if mode:
                    pred, pad_pred = self.__pred(p)
                    p.nombre_archivo = pred.nombre_archivo
                    if pred.left is not None:
                        if pad_pred == p:
                            pad_pred.left = pred.left
                        else:
                            pad_pred.right = pred.left
                    else:
                        if pad_pred == p:
                            pad_pred.left = None
                        else:
                            pad_pred.right = None
                    del pred
                else:
                    sus, pad_sus = self.__sus(p)
                    p.nombre_archivo = sus.nombre_archivo
                    if sus.right is not None:
                        if pad_sus == p:
                            pad_sus.right = sus.right
                        else:
                            pad_sus.left = sus.right
                    else:
                        if pad_sus == p:
                            pad_sus.right = None
                        else:
                            pad_sus.left = None
                    del sus
            print(f"Se eliminó el nodo {nombre_archivo}.")    
            self.balancear(self.root)  # Balancear después de la eliminación
            return True
        print(f"No se encontró el nodo {nombre_archivo} para eliminar.")
        return False

    def __pred(self, nodoArbol: NodoArbol) -> Tuple[NodoArbol, NodoArbol]:
        p, pad = nodoArbol.left, nodoArbol
        while p.right is not None:
            p, pad = p.right, p
        return p, pad
    
    def obtener_nivel(self, nodo: NodoArbol, target: NodoArbol, nivel_actual: int = 0) -> int:
        if nodo is None:
            return -1
        
        if nodo == target:
            return nivel_actual
        
        nivel_izquierdo = self.obtener_nivel(nodo.left, target, nivel_actual + 1)
        if nivel_izquierdo != -1:
            return nivel_izquierdo
        
        nivel_derecho = self.obtener_nivel(nodo.right, target, nivel_actual + 1)
        return nivel_derecho

    def buscar_nodo(self, tipo: str, numero: int) -> None:
        nodo, padre = self.search(NodoArbol(tipo, numero).nombre_archivo)
        if nodo is None:
            print("El nodo no fue encontrado.")
        else:
            aux = nodo.nombre_archivo
            print("El nodo {aux} fue encontrado.")
            print("Opciones:")
            print("a. Obtener el nivel del nodo.")
            print("b. Obtener el factor de balanceo (equilibrio) del nodo.")
            print("c. Encontrar el padre del nodo.")
            print("d. Encontrar el abuelo del nodo.")
            print("e. Encontrar el tío del nodo.")

            opcion = input("Seleccione una opción: ")

            if opcion == "a":
                nivel = self.obtener_nivel(self.root, nodo)
                print(f"El nivel del nodo {aux} es: {nivel}")
            elif opcion == "b":
                balanceo = self.obtener_altura(nodo.right) - self.obtener_altura(nodo.left)
                print(f"El factor de balanceo del nodo {aux} es: {balanceo}")
            elif opcion == "c":
                if padre is None:
                    print("El nodo no tiene padre.")
                else:
                    print(f"El padre del nodo {aux} es: {padre.nombre_archivo}")
            elif opcion == "d":
                if padre is not None:
                    abuelo, _ = self.search(padre.nombre_archivo)
                    if abuelo is not None:
                        print(f"El abuelo del nodo {aux} es: {abuelo.nombre_archivo}")
                    else:
                        print("El nodo no tiene abuelo.")
            elif opcion == "e":
                if padre is not None:
                    _, abuelo = self.search(padre.nombre_archivo)
                    if abuelo is not None:
                        tio = abuelo.left if padre == abuelo.right else abuelo.right if padre == abuelo.left else None
                        if tio is not None:
                            print(f"El tío del nodo {aux} es: {tio.nombre_archivo}")
                        else:
                            print("El nodo no tiene tío.")
                    else:
                        print("El nodo no tiene abuelo.")
                else:
                    print("El nodo no tiene padre.")
            else:
                print("Opción no válida.")

    def buscar_nodos_por_criterios(self, tipo: str, min_size: int, max_size: int) -> List[NodoArbol]:
        resultados = []
        self.buscar_nodos_por_criterios_recursivo(self.root, tipo, min_size, max_size, resultados)
        return resultados

    def buscar_nodos_por_criterios_recursivo(self, nodo: NodoArbol, tipo: str, min_size: int, max_size: int, resultados: List[NodoArbol]) -> None:
        if nodo is None:
            return
        # Verificar si el nodo cumple con los criterios
        if nodo.tipo == tipo and min_size <= nodo.size < max_size:
            resultados.append(nodo)
        # Explorar el subárbol izquierdo si es posible
        if nodo.left is not None:
            self.buscar_nodos_por_criterios_recursivo(nodo.left, tipo, min_size, max_size, resultados)

        # Explorar el subárbol derecho si es posible
        if nodo.right is not None:
            self.buscar_nodos_por_criterios_recursivo(nodo.right, tipo, min_size, max_size, resultados)

    def recorrido_niveles(self) -> None:
        if self.root is None:
            print("El árbol está vacío.")
            return
        # Create an empty queue for level-order traversal
        queue = deque()
        # Enqueue the root node
        queue.append(self.root)

        print("Recorrido por niveles del árbol:")
        while queue:
            # Get the number of nodes at the current level
            level_size = len(queue)
            # Print nodes at the current level
            for _ in range(level_size):
                current_node = queue.popleft()
            # Print the name of the file for the current node
                print(current_node.nombre_archivo)
                # Enqueue the left child if it exists
                if current_node.left:
                    queue.append(current_node.left)
                 # Enqueue the right child if it exists
                if current_node.right:
                    queue.append(current_node.right)

        # Print a separator to indicate the end of the current level
        print("--- Fin del nivel ---")


    def menu(self):
        while True:
            print("\nMenú:")
            print("1. Insertar un nodo")
            print("2. Eliminar un nodo")
            print("3. Buscar un nodo")
            print("4. Buscar nodos por criterios")
            print("5. Mostrar recorrido por niveles del árbol")
            print("6. Visualizar árbol")
            print("7. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                tipo = input("Ingrese el tipo del nodo: ")
                while tipo not in ['bike','cars','cats','dogs','flowers','horses','human']:
                    print("Tipo no válido. Los tipos permitidos son: 'bike', 'cars', 'cats', 'dogs', 'flowers', 'horses', 'human'.")
                    tipo = input("Ingrese el tipo para filtrar los nodos: ")
                numero = input("Ingrese el número del nodo: ")
                self.insert(tipo, numero)
             #   self.visualizar
            elif opcion == "2":
                tipo = input("Ingrese el tipo del nodo a eliminar: ")
                while tipo not in ['bike','cars','cats','dogs','flowers','horses','human']:
                    print("Tipo no válido. Los tipos permitidos son: 'bike', 'cars', 'cats', 'dogs', 'flowers', 'horses', 'human'.")
                    tipo = input("Ingrese el tipo para filtrar los nodos: ")
                numero = input("Ingrese el número del nodo a eliminar: ")
                self.delete(tipo, numero)
              #  self.visualizar
            elif opcion == "3":
                tipo = input("Ingrese el tipo del nodo: ")
                while tipo not in ['bike','cars','cats','dogs','flowers','horses','human']:
                    print("Tipo no válido. Los tipos permitidos son: 'bike', 'cars', 'cats', 'dogs', 'flowers', 'horses', 'human'.")
                    tipo = input("Ingrese el tipo para filtrar los nodos: ")
                numero = input("Ingrese el número del nodo: ")
                self.buscar_nodo(tipo,numero)
            elif opcion == "4":
                tipo = input("Ingrese el tipo del nodo: ")
                while tipo not in ['bike','cars','cats','dogs','flowers','horses','human']:
                    print("Tipo no válido. Los tipos permitidos son: 'bike', 'cars', 'cats', 'dogs', 'flowers', 'horses', 'human'.")
                    tipo = input("Ingrese el tipo para filtrar los nodos: ")
                min_size = int(input("Ingrese el tamaño mínimo del archivo: "))
                max_size = int(input("Ingrese el tamaño máximo del archivo: "))
                nodos_filtrados = self.buscar_nodos_por_criterios(tipo, min_size, max_size)
                print("Nodos que cumplen con los criterios:")
                for i, nodo in enumerate(nodos_filtrados):
                    print(f"{i + 1}. {nodo.nombre_archivo}")
                    
                if nodos_filtrados:
                    opcion_filtrados = input("Seleccione un nodo para buscar más detalles (o presione Enter para omitir): ")
                    if opcion_filtrados.isdigit():
                        indice = int(opcion_filtrados) - 1
                        if 0 <= indice < len(nodos_filtrados):
                            nodo_seleccionado = nodos_filtrados[indice]
                            self.buscar_nodo(nodo_seleccionado.tipo, nodo_seleccionado.numero)
                        else:
                            print("Índice fuera de rango. No se seleccionó ningún nodo.")
                    else:
                        print("No se seleccionó ningún nodo.")
                        
            elif opcion == "5":
                self.recorrido_niveles()
            elif opcion == "6":
                self.visualizar()
            elif opcion == "7":
                print("¡Adiós!")
                break
            else:
                print("Opción no válida. Inténtelo de nuevo.")


def main():
    # Crear un árbol AVL
    arbol = ArbolAVL()

    # Abrir el menú del árbol
    arbol.menu()

# Llamada al programa principal
if __name__ == "__main__":
    main()