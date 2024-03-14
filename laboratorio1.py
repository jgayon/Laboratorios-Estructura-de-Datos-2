#import graphviz
import os
from typing import Any, Optional, Tuple

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
        return aux

    def simple_derecha(self,nodo: NodoArbol):
        aux = nodo.left
        nodo.left = aux.right
        aux.right = nodo
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
    
    def insertar(self, tipo, numero):
        nuevo_nodo = NodoArbol(tipo, numero)
        self.root = self._insertar_recursivo(self.root, nuevo_nodo)
        print(f"se ha insertado el nodo: {nuevo_nodo.nombre_archivo}")


    def _insertar_recursivo(self, nodo_actual, nuevo_nodo):
        if nodo_actual is None:
            return nuevo_nodo

        if nuevo_nodo.nombre_archivo < nodo_actual.nombre_archivo:
            nodo_actual.left = self._insertar_recursivo(nodo_actual.left, nuevo_nodo)
        elif nuevo_nodo.nombre_archivo > nodo_actual.nombre_archivo:
            nodo_actual.right = self._insertar_recursivo(nodo_actual.right, nuevo_nodo)
        else:
            # Ignorar nodos duplicados
            return nodo_actual

        # Balancear el árbol después de la inserción
        return self.balancear(nodo_actual)


    def eliminar(self, tipo, numero):
        self.root = self._eliminar_recursivo(self.root, tipo, numero)

    def _eliminar_recursivo(self, nodo_actual, tipo, numero):
        if nodo_actual is None:
            return nodo_actual

        # Recorrer el árbol hasta encontrar el nodo a eliminar
        if numero < nodo_actual.numero:
            nodo_actual.left = self._eliminar_recursivo(nodo_actual.left, tipo, numero)
        elif numero > nodo_actual.numero:
            nodo_actual.right = self._eliminar_recursivo(nodo_actual.right, tipo, numero)
        else:
            print(f"se ha eliminado el nodo: {nodo_actual.nombre_archivo}")
            # Nodo encontrado, proceder a eliminar
            if nodo_actual.left is None:
                temp = nodo_actual.right
                nodo_actual = None
                return temp
            elif nodo_actual.right is None:
                temp = nodo_actual.left
                nodo_actual = None
                return temp

            # Nodo con dos hijos: obtener el sucesor inorden (el nodo más pequeño en el subárbol derecho)
            temp = self._min_value_node(nodo_actual.right)
            # Copiar el contenido del sucesor inorden al nodo actual
            nodo_actual.numero = temp.numero
            nodo_actual.tipo = temp.tipo
            # Eliminar el sucesor inorden
            nodo_actual.right = self._eliminar_recursivo(nodo_actual.right, temp.tipo, temp.numero)

        # Balancear el árbol después de la eliminación
        return self.balancear(nodo_actual)
    
    def _min_value_node(self, nodo):
        current = nodo
        while current.left is not None:
            current = current.left
        return current
    
    def obtener_nivel(self, nodo: NodoArbol, nivel_actual: int = 0) -> int:
        if nodo is None:
            return nivel_actual - 1  # Restamos 1 porque el nodo es nulo

        nivel_izquierdo = self.obtener_nivel(nodo.left, nivel_actual + 1)
        nivel_derecho = self.obtener_nivel(nodo.right, nivel_actual + 1)

        return max(nivel_izquierdo, nivel_derecho)

    
    def buscar_nodo(self, tipo: str, numero: int) -> None:
        nodo, padre = self.search((tipo, numero))
        if nodo is None:
            print("El nodo no fue encontrado.")
        else:
            print("El nodo fue encontrado.")
            print("Opciones:")
            print("a. Obtener el nivel del nodo.")
            print("b. Obtener el factor de balanceo (equilibrio) del nodo.")
            print("c. Encontrar el padre del nodo.")
            print("d. Encontrar el abuelo del nodo.")
            print("e. Encontrar el tío del nodo.")

            opcion = input("Seleccione una opción: ")

            if opcion == "a":
                nivel = self.obtener_altura(nodo)-1
                print(f"El nivel del nodo es: {nivel}")
            elif opcion == "b":
                balanceo = self.obtener_altura(nodo.right) - self.obtener_altura(nodo.left)
                print(f"El factor de balanceo del nodo es: {balanceo}")
            elif opcion == "c":
                if padre is None:
                    print("El nodo no tiene padre.")
                else:
                    print(f"El padre del nodo es: {padre.nombre_archivo}")
            elif opcion == "d":
                padre_aux,abuelo = self.search(padre.tipo,padre.numero)
                if abuelo is None:
                    print("El nodo no tiene abuelo.")
                else:
                    print(f"El abuelo del nodo es: {abuelo}")
            elif opcion == "e":
                padre_aux,abuelo = self.search(padre.tipo,padre.numero)
                tio = abuelo.left if not padre_aux  else abuelo.right if not padre_aux else None
                if tio is None:
                    print("El nodo no tiene tío.")
                else:
                    print(f"El tío del nodo es: {tio.self.nombre_archivo}")
            else:
                print("Opción no válida.")


    def search(self, elem: Tuple[str, int]) -> Tuple[Optional["NodoArbol"], Optional["NodoArbol"]]:
        p, pad = self.root, None
        while p is not None:
            if elem == (p.tipo, p.numero):
                return p, pad
            elif elem < (p.tipo, p.numero):
                pad = p
                p = p.left
            else:
                pad = p
                p = p.right
        return p, pad

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
                numero = input("Ingrese el número del nodo: ")
                self.insertar(tipo, numero)
             #   self.visualizar
            elif opcion == "2":
                tipo = input("Ingrese el tipo del nodo a eliminar: ")
                numero = input("Ingrese el número del nodo a eliminar: ")
                self.eliminar(tipo, numero)
              #  self.visualizar
            elif opcion == "3":
                tipo = input("Ingrese el tipo del nodo a buscar: ")
                numero = input("Ingrese el número del nodo a buscar: ")
                self.buscar_nodo(tipo, numero)
            elif opcion == "4":
                tipo = input("Ingrese el tipo para filtrar los nodos: ")
                min_size = int(input("Ingrese el tamaño mínimo del archivo: "))
                max_size = int(input("Ingrese el tamaño máximo del archivo: "))
                # Lógica para buscar nodos por criterios
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