import graphviz
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

    @classmethod
    def obtener_altura(cls, nodo: NodoArbol) -> int:
        if nodo is None:
            return 0
        altura_izquierda = cls.obtener_altura(nodo.left)
        altura_derecha = cls.obtener_altura(nodo.right)
        return max(altura_izquierda, altura_derecha) + 1

    @classmethod
    def simple_izquierda(cls, nodo: NodoArbol):
        aux = nodo.right
        nodo.right = aux.left
        aux.left = nodo
        return aux

    @classmethod
    def simple_derecha(cls, nodo: NodoArbol):
        aux = nodo.left
        nodo.left = aux.right
        aux.right = nodo
        return aux

    @classmethod
    def balancear(cls, nodo: NodoArbol) -> NodoArbol:
        bal = cls.obtener_altura(nodo.right) - cls.obtener_altura(nodo.left)
        if bal == 2:
            if cls.obtener_altura(nodo.right.left) == -1:
                nodo.right = cls.simple_derecha(nodo.right)
                return cls.simple_izquierda(nodo)
            else:
                return cls.simple_izquierda(nodo)

        elif bal == -2:
            if cls.obtener_altura(nodo.left.right) == 1:
                nodo.left = cls.simple_izquierda(nodo.left)
                return cls.simple_derecha(nodo)
            else:
                return cls.simple_derecha(nodo)

        return nodo

    def insertar(self, tipo, numero):
        nuevo_nodo = NodoArbol(tipo, numero)
        self.root = self._insertar_recursivo(self.root, nuevo_nodo)

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


    def _eliminar_recursivo(self, nodo_actual, tipo, numero):
        if nodo_actual is None:
            return nodo_actual

        # Recorrer el árbol hasta encontrar el nodo a eliminar
        if numero < nodo_actual.numero:
            nodo_actual.left = self._eliminar_recursivo(nodo_actual.left, tipo, numero)
        elif numero > nodo_actual.numero:
            nodo_actual.right = self._eliminar_recursivo(nodo_actual.right, tipo, numero)
        else:
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

  ##  def visualizar_con_acciones(self):
        dot = graphviz.Digraph()

        self._construir_grafo_con_acciones(dot, self.root)

        dot.render('arbol_avl', format='png', cleanup=True)
        dot.view()

  ##  def _construir_grafo_con_acciones(self, dot, nodo):
        if nodo is not None:
            ruta_imagen = os.path.join("data", nodo.tipo, nodo.nombre_archivo)
            dot.node(str(nodo.nombre_archivo), label=str(nodo.nombre_archivo), URL=ruta_imagen)
            if nodo.left is not None:
                dot.edge(str(nodo.nombre_archivo), str(nodo.left.nombre_archivo))
                self._construir_grafo_con_acciones(dot, nodo.left)
            if nodo.right is not None:
                dot.edge(str(nodo.nombre_archivo), str(nodo.right.nombre_archivo))
                self._construir_grafo_con_acciones(dot, nodo.right)

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
                nivel = self.obtener_nivel(nodo)
                print(f"El nivel del nodo es: {nivel}")
            elif opcion == "b":
                balanceo = self.obtener_altura(nodo.right)-self.obtener_altura(nodo.left)
                print(f"El factor de balanceo del nodo es: {balanceo}")
            elif opcion == "c":
                if padre is None:
                    print("El nodo no tiene padre.")
                else:
                    print(f"El padre del nodo es: {padre.data}")
            elif opcion == "d":
                abuelo = self.obtener_abuelo(nodo)
                if abuelo is None:
                    print("El nodo no tiene abuelo.")
                else:
                    print(f"El abuelo del nodo es: {abuelo.data}")
            elif opcion == "e":
                tio = self.obtener_tio(nodo)
                if tio is None:
                    print("El nodo no tiene tío.")
                else:
                    print(f"El tío del nodo es: {tio.data}")
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
             #   self.visualizar_con_acciones()
            elif opcion == "2":
                tipo = input("Ingrese el tipo del nodo a eliminar: ")
                numero = input("Ingrese el número del nodo a eliminar: ")
                self.eliminar(tipo, numero)
              #  self.visualizar_con_acciones()
            elif opcion == "3":
                tipo = input("Ingrese el tipo del nodo a buscar: ")
                numero = input("Ingrese el número del nodo a buscar: ")
                # Lógica para buscar el nodo
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


    def submenu_buscar_nodo(self, nodo_encontrado):
        while True:
            print("\nSubmenú del nodo encontrado:")
            print("a. Obtener nivel del nodo")
            print("b. Obtener factor de balanceo del nodo")
            print("c. Encontrar el padre del nodo")
            print("d. Encontrar el abuelo del nodo")
            print("e. Encontrar el tío del nodo")
            print("f. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "a":
                nivel = self.obtener_nivel(self.root, nodo_encontrado, 1)
                print(f"Nivel del nodo: {nivel}")
            elif opcion == "b":
                factor_balanceo = self.obtener_factor_balanceo(nodo_encontrado)
                print(f"Factor de balanceo del nodo: {factor_balanceo}")
            elif opcion == "c":
                padre = self.encontrar_padre(self.root, nodo_encontrado)
                print(f"Padre del nodo: {padre.nombre_archivo if padre else 'No tiene padre'}")
            elif opcion == "d":
                abuelo = self.encontrar_abuelo(self.root, nodo_encontrado)
                print(f"Abuelo del nodo: {abuelo.nombre_archivo if abuelo else 'No tiene abuelo'}")
            elif opcion == "e":
                tio = self.encontrar_tio(self.root, nodo_encontrado)
                print(f"Tío del nodo: {tio.nombre_archivo if tio else 'No tiene tío'}")
            elif opcion == "f":
                print("Volviendo al menú principal...")
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