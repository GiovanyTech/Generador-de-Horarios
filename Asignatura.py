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
        """El nombre de la asignatura (ej. "Cálculo Vectorial")."""
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
        """Representación legible para el usuario final."""
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
        """El hash se basa en el nombre de la asignatura, que se asume único."""
        return hash(self.nombre.lower())

# --- Ejemplo de Uso ---
if __name__ == "__main__":
    # --- Creamos las asignaturas ---
    eym = Asignatura("Electricidad y Magnetismo")
    ed = Asignatura("Ecuaciones Diferenciales")
    an = Asignatura("Análisis Numérico")
    md = Asignatura("Matemáticas Discretas")

    fisica = Asignatura("Física de Ondas")

    # --- Creamos y agregamos grupos a Electricidad y Magnetismo ---
    gp_eym_2 = Grupo(2, "Mat. James Clerk Maxwell", [
                    BloqueHoras(DiaSemana.MARTES, "11:00", "13:00"),
                    BloqueHoras(DiaSemana.JUEVES, "11:00", "13:00")
    ])

    gp_eym_4 = Grupo(4, "Fis. Gustav Robert Kirchhoff", [
                    BloqueHoras(DiaSemana.LUNES, "13:00", "15:00"),
                    BloqueHoras(DiaSemana.MIERCOLES, "13:00", "15:00")
    ])

    gp_eym_6 = Grupo(6, "Fis. Hendrik Antoon Lorentz", [
                    BloqueHoras(DiaSemana.MIERCOLES, "15:00", "17:00"),
                    BloqueHoras(DiaSemana.VIERNES, "15:00", "17:00")
    ])

    gp_eym_8 = Grupo(8, "Mtro. Michael Faraday", [
                    BloqueHoras(DiaSemana.MARTES, "17:00", "19:00"),
                    BloqueHoras(DiaSemana.JUEVES, "17:00", "19:00")
    ])

    eym.agregar_grupo(gp_eym_2)
    eym.agregar_grupo(gp_eym_4)
    eym.agregar_grupo(gp_eym_6)
    eym.agregar_grupo(gp_eym_8)

    # --- Creamos y agregamos grupos a Ecuaciones Diferenciales ---
    gp_ed_3 = Grupo(3, "Fis. Józef Maria Hoene-Wroński", [
                    BloqueHoras(DiaSemana.MARTES, "17:00", "19:00"),
                    BloqueHoras(DiaSemana.JUEVES, "17:00", "19:00")
    ])

    gp_ed_4 = Grupo(4, "Fis. Pierre-Simon Laplace", [
                BloqueHoras(DiaSemana.MIERCOLES, "15:00", "17:00"),
                BloqueHoras(DiaSemana.VIERNES, "15:00", "17:00")
    ])
    gp_ed_5 = Grupo(5, "Mat. Jean-Baptiste Joseph Fourier", [
                BloqueHoras(DiaSemana.LUNES, "11:00", "13:00"),
                BloqueHoras(DiaSemana.MIERCOLES, "11:00", "13:00")
    ])

    ed.agregar_grupo(gp_ed_3)
    ed.agregar_grupo(gp_ed_4)
    ed.agregar_grupo(gp_ed_5)

    # --- Creamos y agregamos grupos a Análisis Numérico ---
    gp_an_1 = Grupo(1, "Ing. Alekséi Nikoláyevich Krylov", [
                    BloqueHoras(DiaSemana.MARTES, "19:00", "21:00"),
                    BloqueHoras(DiaSemana.JUEVES, "19:00", "21:00")
    ])

    gp_an_2 = Grupo(2, "Mat. Brook Taylor", [
        BloqueHoras(DiaSemana.LUNES, "07:00", "09:00"),
        BloqueHoras(DiaSemana.MIERCOLES, "07:00", "09:00")
    ])

    an.agregar_grupo(gp_an_1)
    an.agregar_grupo(gp_an_2)

    # --- Creamos y agregamos grupos a Matemáticas Discretas ---
    gp_md_1 = Grupo(1, "Mat. Leonhard Paul Euler", [
                    BloqueHoras(DiaSemana.MARTES, "13:00", "15:00"),
                    BloqueHoras(DiaSemana.JUEVES, "13:00", "15:00")
    ])

    md.agregar_grupo(gp_md_1)

    print("--- Mostrando Asignatura de Electricidad y Magnetismo ---")
    print(eym)
    print("--- Mostrando Asignatura de Ecuaciones Diferenciales ---")
    print(ed)

    print("\n" + "=" * 40 + "\n")

    # --- Probando la lógica ---
    print("--- Probando la lógica de búsqueda y errores ---")

    # Buscar un grupo que existe
    grupo_encontrado = eym.buscar_grupo(2)
    print(f"Buscando grupo 2 en Electricidad y Magnetismo... Encontrado: {grupo_encontrado.profesor}")
    print("\n" + "=" * 40 + "\n")

    # Intentar agregar un grupo duplicado (debería fallar)
    try:
        print("\nIntentando agregar de nuevo el grupo 3 a Ecuaciones Dif...")
        g_ed_1_duplicado = Grupo(3, "Prof. Repetido", [])
        ed.agregar_grupo(g_ed_1_duplicado)
    except ValueError as e:
        print(f"ÉXITO: Se detectó el error correctamente.")
        print(f"  Mensaje: {e}")