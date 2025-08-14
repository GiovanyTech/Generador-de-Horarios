from BloqueHoras import BloqueHoras, DiaSemana
from Grupo import Grupo
from typing import Dict, List, Optional, Set

class Asignatura:
    """
    Representa una materia de estudio y gestiona la colección de grupos disponibles para ella.
    """
    def __init__(self, nombre: str):
        self._nombre = Asignatura._validar_nombre(nombre)
        # Usamos un diccionario para un acceso ultra-rápido a los grupos por su ID.
        self._grupos: Dict[int, Grupo] = {}

    # --- Métodos privados ---

    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre de la asignatura debe ser un texto no vacío.")
        return nombre.strip()

    # --- Propiedades Públicas de Solo Lectura ---

    @property
    def nombre(self) -> str:
        """El nombre de la asignatura (ej. "Cálculo Vectorial"). Es de solo lectura."""
        return self._nombre

    @property
    def grupos(self) -> List[Grupo]:
        """Devuelve una lista ordenada de todos los grupos disponibles."""
        # Devolvemos los valores del diccionario, convertidos a una lista.
        return sorted(self._grupos.values(), key=lambda g: g.id_grupo)

    # --- Métodos Públicos (La "API" de la clase) ---

    def agregar_grupo(self, grupo: Grupo) -> None:
        """Añade un grupo a la asignatura, verificando que no haya duplicados."""
        if not isinstance(grupo, Grupo):
            raise TypeError("Solo se pueden añadir objetos de la clase Grupo.")

        # Con un diccionario, la comprobación de duplicados es más rápida y directa.
        if grupo.id_grupo in self._grupos:
            raise ValueError(f"El grupo con ID {grupo.id_grupo} ya existe en la asignatura '{self.nombre}'.")

        self._grupos[grupo.id_grupo] = grupo

    def buscar_grupo(self, id_grupo: int) -> Optional[Grupo]:
        """Busca y devuelve un grupo por su ID. Devuelve None si no se encuentra."""
        return self._grupos.get(id_grupo) # El metodo .get() de los diccionarios es perfecto para esto.

    def eliminar_grupo(self, id_grupo: int) -> None:
        """Elimina un grupo de la asignatura por su ID."""
        if id_grupo not in self._grupos:
            raise KeyError(f"No se encontró un grupo con ID {id_grupo} en la asignatura '{self.nombre}'.")
        del self._grupos[id_grupo]

    # --- Dunder Methods ---

    def __repr__(self) -> str:
        """Representación textual del objeto, útil para debugging."""
        return f"{self.__class__.__name__}(nombre='{self.nombre}', num_grupos={len(self._grupos)})"

    def __str__(self) -> str:
        if not self._grupos:
            return f"Asignatura: {self.nombre}\n(No hay grupos disponibles)"

        grupos_str = "\n\n".join(str(g) for g in self.grupos)
        return f"--- Asignatura: {self.nombre} ---\n\n{grupos_str}"

    def __eq__(self, otro: object) -> bool:
        """Dos asignaturas son iguales si tienen el mismo nombre."""
        if not isinstance(otro, Asignatura):
            return NotImplemented
        return self.nombre.lower() == otro.nombre.lower()

    def __hash__(self) -> int:
        return hash(self.nombre.lower())


# --- Ejemplo de Uso ---
if __name__ == "__main__":
    # --- Creamos las asignaturas ---
    eym = Asignatura("Electricidad y Magnetismo")
    ed = Asignatura("Estructuras Discretas")

    calc = Asignatura("Cálculo Vectorial")
    fisica = Asignatura("Física de Ondas")

    # --- Creamos y agregamos grupos a Electricidad y Magnetismo ---
    gp_eym_8 = Grupo(8, "M.I. Germán Ramón Arconada", [
                    BloqueHoras(DiaSemana.MARTES, "17:00", "19:00"),
                    BloqueHoras(DiaSemana.JUEVES, "17:00", "19:00")
    ])

    gp_eym_17 = Grupo(17, "Ing. Santiago Gonzalez Lopez",[
                    BloqueHoras(DiaSemana.MARTES, "19:00", "21:00"),
                    BloqueHoras(DiaSemana.JUEVES, "19:00", "21:00")
    ])

    gp_eym_5 = Grupo(5, "M.I. Mayverena Jurado Pineda", [
                    BloqueHoras(DiaSemana.LUNES, "11:00", "13:00"),
                    BloqueHoras(DiaSemana.MIERCOLES, "11:00", "13:00")
    ])

    eym.agregar_grupo(gp_eym_8)
    eym.agregar_grupo(gp_eym_17)
    eym.agregar_grupo(gp_eym_5)

    # --- Creamos y agregamos grupos a Estructuras Discretas ---
    gp_ed_1 = Grupo(1, "M.I. Yi Tan Li", [
                    BloqueHoras(DiaSemana.MARTES, "17:00", "19:00"),
                    BloqueHoras(DiaSemana.JUEVES, "17:00", "19:00")
    ])

    ed.agregar_grupo(gp_ed_1)

    # --- Creamos y agregamos grupos a CÁLCULO ---
    g_calc_1 = Grupo(1, "Dr. Gauss", [
        BloqueHoras(DiaSemana.LUNES, "07:00", "09:00"),
        BloqueHoras(DiaSemana.MIERCOLES, "07:00", "09:00")  # <-- Simplemente añades el nuevo bloque aquí
    ])
    g_calc_2 = Grupo(2, "Dra. Lagrange", [BloqueHoras(DiaSemana.MARTES, "07:00", "09:00")])
    calc.agregar_grupo(g_calc_1)
    calc.agregar_grupo(g_calc_2)

    # --- Creamos y agregamos grupos a FÍSICA ---
    # ¡Aquí está la clave! Podemos tener un grupo con ID 1 porque está en OTRA asignatura.
    g_fis_1 = Grupo(1, "Dr. Einstein", [BloqueHoras(DiaSemana.VIERNES, "11:00", "13:00")])
    fisica.agregar_grupo(g_fis_1)

    print("--- Mostrando Asignatura de Cálculo ---")
    print(calc)
    print("--- Mostrando Asignatura de Física ---")
    print(fisica)
    print("--- Mostrando Asignatura de Electricidad y Magnetismo")
    print(eym)
    print("\n" + "=" * 40 + "\n")

    # --- Probando la lógica ---
    print("--- Probando la lógica de búsqueda y errores ---")

    # Buscar un grupo que existe
    grupo_encontrado = calc.buscar_grupo(2)
    print(f"Buscando grupo 2 en Cálculo... Encontrado: {grupo_encontrado.profesor}")
    print("\n" + "=" * 40 + "\n")

    # Intentar agregar un grupo duplicado (debería fallar)
    try:
        print("\nIntentando agregar de nuevo el grupo 1 a Cálculo...")
        g_calc_1_duplicado = Grupo(1, "Prof. Repetido", [])
        calc.agregar_grupo(g_calc_1_duplicado)
    except ValueError as e:
        print(f"ÉXITO: Se detectó el error correctamente.")
        print(f"  Mensaje: {e}")