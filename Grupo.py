from BloqueHoras import BloqueHoras, DiaSemana
from typing import Optional, List, Set

class Grupo:
    """Representa un grupo específico de una asignatura, con un profesor y uno o más bloques de horario asociados."""

    def __init__(self, id_grupo: int, profesor: str, bloques_iniciales: Optional[List[BloqueHoras]] = None):
        """
        Inicializa un objeto Grupo.
        Args:
            id_grupo: El identificador numérico único del grupo (ej. 1, 2, 3...).
            profesor: El nombre del profesor que imparte la clase.
            bloques_iniciales: (Opcional) Una lista de objetos BloqueHoras para poblar el horario del grupo desde el inicio.
        Raises:
            TypeError: Si los argumentos tienen tipos incorrectos.
            ValueError: Si los argumentos tienen valores inválidos (ej. id negativo)
                        o si los bloques iniciales se solapan entre sí.
        """

        self._id_grupo = Grupo._validar_id(id_grupo)
        self._profesor = Grupo._validar_profesor(profesor)
        # Usar un 'set' es semánticamente más correcto para una colección de
        # bloques únicos. Esto previene duplicados automáticamente.
        self._bloques: Set[BloqueHoras] = set()

        if bloques_iniciales:
            # Si se proporcionan bloques, los agregamos uno por uno para asegurar la validación.
            for bloque in bloques_iniciales:
                self.agregar_bloque_horario(bloque)

    # --- Métodos Privados ---

    @staticmethod
    def _validar_id(id_grupo: int) -> int:
        if not isinstance(id_grupo, int): raise TypeError("El ID del grupo debe ser un número entero.")
        if id_grupo <= 0: raise ValueError("El ID del grupo debe ser un número positivo.")
        return id_grupo

    @staticmethod
    def _validar_profesor(profesor: str) -> str:
        if not isinstance(profesor, str) or not profesor.strip():
            raise ValueError("El nombre del profesor debe ser un string no vacío.")
        return profesor.strip()

    # --- Propiedades Públicas de Solo Lectura ---

    @property
    def id_grupo(self) -> int:
        """El identificador numérico del grupo."""
        return self._id_grupo

    @property
    def profesor(self) -> str:
        """El nombre del profesor que imparte clase en este grupo."""
        return self._profesor

    @property
    def horarios(self) -> list[BloqueHoras]:
        """Devuelve una COPIA de la lista de horarios para proteger la encapsulación."""
        return sorted(self._bloques) # Devolvemos la copia ordenada

    # --- Métodos Públicos ---

    def agregar_bloque_horario(self, nuevo_bloque: BloqueHoras) -> None:
        """
        Añade un BloqueHoras al horario del grupo, validando que no se solape con los bloques ya existentes.
        Args:
            nuevo_bloque: El objeto BloqueHoras a agregar.
        Raises:
            TypeError: Si el argumento no es un objeto BloqueHoras.
            ValueError: Si el nuevo bloque se solapa con un bloque existente en el grupo.
        """
        if not isinstance(nuevo_bloque, BloqueHoras):
            raise TypeError("Solo se pueden agregar objetos de tipo BloqueHoras.")

        # Verificamos que el nuevo bloque no choque con los existentes.
        for bloque_existente in self._bloques:
            if nuevo_bloque.se_solapa_con(bloque_existente):
                raise ValueError(f"Conflicto de horario interno en el grupo {self.id_grupo}. "
                                 f"El bloque '{nuevo_bloque}' se solapa con '{bloque_existente}'.")

        self._bloques.add(nuevo_bloque)

    def se_solapa_con(self, otro_grupo: 'Grupo') -> bool:
        """
        Verifica si este grupo tiene algún conflicto de horario con otro grupo.
        """
        # Comparamos cada uno de nuestros bloques con cada uno de los bloques del otro grupo.
        for mi_bloque in self._bloques:
            for su_bloque in otro_grupo._bloques:
                if mi_bloque.se_solapa_con(su_bloque):
                    return True  # Encontramos un conflicto, terminamos la búsqueda.
        return False  # No se encontró ningún conflicto.

        # --- Dunder Methods ---

    def __repr__(self) -> str:
        """Representación no ambigua para desarrolladores."""
        return f"{self.__class__.__name__} (id_grupo={self.id_grupo}, profesor='{self.profesor}')"

    def __str__(self) -> str:
        """Representación legible para el usuario final."""
        # Usamos un "join" para construir una lista de horarios con formato.
        horarios_str = "\n".join(f"  - {bloque}" for bloque in self.horarios)
        if not horarios_str:
            horarios_str = "  - (Sin horarios asignados)"
        return f"Grupo: {self.id_grupo}\nProfesor: {self.profesor}\nHorarios:\n{horarios_str}"

    def __eq__(self, otro: object) -> bool:
        """Dos grupos son iguales si su id_grupo es el mismo."""
        if not isinstance(otro, Grupo):
            return NotImplemented
        return self.id_grupo == otro.id_grupo

    def __hash__(self) -> int:
        """El hash se basa en el id_grupo, que se asume único."""
        return hash(self.id_grupo)


# --- Ejemplo de Uso ---
if __name__ == "__main__":
    # --- Bloques de ejemplo ---
    bloque_fis_1 = BloqueHoras(DiaSemana.MARTES, "11:00", "13:00")
    bloque_fis_2 = BloqueHoras(DiaSemana.JUEVES, "11:00", "13:00")
    bloque_fis_3 = BloqueHoras(DiaSemana.LUNES, "13:00", "15:00")
    bloque_fis_4 = BloqueHoras(DiaSemana.MIERCOLES, "13:00", "15:00")
    bloque_fis_5 = BloqueHoras(DiaSemana.MIERCOLES, "15:00", "17:00")
    bloque_fis_6 = BloqueHoras(DiaSemana.VIERNES, "15:00", "17:00")

    bloque_ed_1 = BloqueHoras(DiaSemana.MARTES, "17:00", "19:00")
    bloque_ed_2 = BloqueHoras(DiaSemana.JUEVES, "17:00", "19:00")
    bloque_ed_3 = BloqueHoras(DiaSemana.MIERCOLES, "15:00", "17:00")
    bloque_ed_4 = BloqueHoras(DiaSemana.VIERNES, "15:00", "17:00")
    bloque_ed_5 = BloqueHoras(DiaSemana.LUNES, "11:00", "13:00")
    bloque_ed_6 = BloqueHoras(DiaSemana.MIERCOLES, "11:00", "13:00")

    bloque_an_1 = BloqueHoras(DiaSemana.MARTES, "19:00", "21:00")
    bloque_an_2 = BloqueHoras(DiaSemana.JUEVES, "19:00", "21:00")


    # --- Creación de Grupos ---
    print("--- Creando Grupos ---")
    gp_fis_2 = Grupo(2, "Mat. James Clerk Maxwell", [bloque_fis_1, bloque_fis_2])
    gp_fis_4 = Grupo(4, "Fis. Gustav Robert Kirchhoff", [bloque_fis_3, bloque_fis_4])
    gp_fis_6 = Grupo(6, "Fis. Hendrik Antoon Lorentz", [bloque_fis_5, bloque_fis_6])

    gp_ed_3 = Grupo(3,"Fis. Józef Maria Hoene-Wroński", [bloque_ed_1, bloque_ed_2])
    gp_ed_4 = Grupo(4, "Fis. Pierre-Simon Laplace", [bloque_ed_3, bloque_ed_4])
    gp_ed_5 = Grupo(5, "Mat. Jean-Baptiste Joseph Fourier", [bloque_ed_5, bloque_ed_6])

    gp_an_1 = Grupo(1, "Ing. Alekséi Nikoláyevich Krylov", [bloque_an_1, bloque_an_2])

    gp_fis_8 = Grupo(id_grupo=8, profesor="Dra. Newton")  # No tiene BloqueHoras a propósito

    print(gp_fis_2)
    print(gp_fis_4)
    print(gp_fis_6)
    print(gp_fis_8)
    print(gp_ed_3)
    print(gp_ed_4)
    print(gp_ed_5)
    print(gp_an_1)
    print("-" * 30)

    # --- Probando la lógica de solapamiento ---
    print("\n--- Probando Lógica de Solapamiento ---")
    print(f"¿Grupo de Física 8 se solapa con Grupo de Física 2? {gp_fis_8.se_solapa_con(gp_fis_2)}")
    print(f"¿Grupo de Ecuaciones Dif. 4 se solapa con Grupo de Física 6? {gp_ed_4.se_solapa_con(gp_fis_6)}")
    print("-" * 30)

    print("\n--- Probando Validación Interna ---")
    try:
        print("Intentando agregar un bloque conflictivo al Grupo de Física 2...")
        # Esto debería fallar, porque 10-12 del jueves ya existe
        bloque_interno_conflictivo = BloqueHoras(DiaSemana.JUEVES, "11:00", "13:00")
        gp_fis_2.agregar_bloque_horario(bloque_interno_conflictivo)
    except ValueError as e:
        print(f"ÉXITO: Se detectó el error correctamente.")
        print(f"  Mensaje: {e}")
    print("-" * 30)

    # --- Probando __eq__ y __hash__ ---
    print("\n--- Probando Igualdad y Sets ---")
    print(f"¿Grupo ED 4 == Grupo Física 4? {gp_ed_4 == gp_fis_4} (Mismo ID)")
    print(f"¿Grupo ED 5 == Grupo Física 2? {gp_ed_5 == gp_fis_2} (Diferente ID)")
    conjunto_grupos = {gp_ed_4, gp_fis_4, gp_an_1, gp_fis_6}
    print(f"\nAñadimos 4 grupos a un set, pero como dos tienen el mismo ID, el tamaño es {len(conjunto_grupos)}")
    print("Contenido del set (basado en repr):")
    for g in conjunto_grupos:
        print(f" - {repr(g)}")