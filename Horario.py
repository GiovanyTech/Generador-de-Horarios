# Archivo: Horario.py
from BloqueHoras import DiaSemana, BloqueHoras
from Asignatura import Asignatura
from Grupo import Grupo
from typing import List, Dict, Tuple, Iterable

class Horario:
    """
    Representa una única combinación validada de asignaturas y grupos que no
    presentan conflictos de horario entre sí.
    """

    def __init__(self, seleccion: Dict[Asignatura, Grupo]):
        """
        Inicializa y VALIDA un horario.

        Args:
            seleccion: Un diccionario que mapea un objeto Asignatura a un
                       objeto Grupo seleccionado para esa asignatura.

        Raises:
            ValueError: Si se detecta un conflicto de horario entre los
                        grupos seleccionados.
        """
        if not isinstance(seleccion, dict):
            raise TypeError("La selección debe ser un diccionario de {Asignatura: Grupo}.")

        self._seleccion = seleccion
        self._validar_conflictos() # Método privado
        self._bloques_organizados = self._organizar_para_vista() # Método privado

    def _validar_conflictos(self):
        """Método interno para asegurar que no hay solapamientos. Si hay
            solapamientos, regresamos ValueError, de lo contrario seguimos normal"""
        grupos_a_validar = list(self._seleccion.values()) # Lista de values=Grupos
        for i in range(len(grupos_a_validar)): # Recorremos cada Grupo
            for j in range(i + 1, len(grupos_a_validar)):
                grupo1 = grupos_a_validar[i]
                grupo2 = grupos_a_validar[j]
                if grupo1.se_solapa_con(grupo2):
                    raise ValueError(f"Conflicto de horario detectado entre:\n"
                                     f" - {grupo1.id_grupo} ({list(self._seleccion.keys())[i].nombre})\n"
                                     f" - {grupo2.id_grupo} ({list(self._seleccion.keys())[j].nombre})")

    def _organizar_para_vista(self) -> Dict[DiaSemana, List[Tuple[BloqueHoras, str]]]:
        """Pre-procesa los bloques para una visualización eficiente."""

        # Creamos una lista vacía para cada día de la semana
        bloques_por_dia = {dia: [] for dia in DiaSemana}

        # Recorremos la <asignatura, grupo> del horario
        for asignatura, grupo in self._seleccion.items():
            # Recorremos los bloques de horas de cada grupo
            for bloque in grupo.horarios:
                info_str = f"{asignatura.nombre} (Gpo {grupo.id_grupo}) - {grupo.profesor}"
                bloques_por_dia[bloque.dia].append((bloque, info_str))

        # Ordenar los bloques dentro de cada día por hora de inicio
        for dia in bloques_por_dia:
            bloques_por_dia[dia].sort(key=lambda item: item[0].inicio)

        return bloques_por_dia

    # --- Propiedades Públicas de Solo Lectura ---

    @property
    def seleccion(self):
        return self._seleccion

    # Magic Methods

    def __str__(self) -> str:
        """Genera una representación de tabla del horario."""
        output = ["========================================", "          HORARIO PROPUESTO           ",
                  "========================================"]

        for dia in DiaSemana:
            bloques_info = self._bloques_organizados[dia]
            if not bloques_info:
                continue  # No imprimir días sin clases

            output.append(f"\n--- {str(dia).upper()} ---")
            for bloque, info_str in bloques_info:
                output.append(f"  {bloque.inicio:%H:%M} - {bloque.fin:%H:%M} | {info_str}")

        return "\n".join(output)

    def __len__(self) -> int:
        """Devuelve el número de asignaturas en el horario."""
        return len(self._seleccion)

    def __iter__(self) -> Iterable[Tuple[Asignatura, Grupo]]:
        """Permite iterar sobre los pares (asignatura, grupo) del horario."""
        return iter(self._seleccion.items())


# ==============================================================================
# --- Ejemplo de Uso del Sistema Completo ---
# ==============================================================================
if __name__ == "__main__":
    # 1. Definir las asignaturas que quieres cursar
    calc = Asignatura("Cálculo Vectorial")
    fisica = Asignatura("Física de Ondas")
    prog = Asignatura("Estructuras de Datos")

    # 2. Poblar cada asignatura con sus grupos y horarios disponibles
    calc.agregar_grupo(Grupo(1, "Dr. Gauss", [BloqueHoras(DiaSemana.LUNES, "07:00", "09:00"),
                                              BloqueHoras(DiaSemana.MIERCOLES, "07:00", "09:00")]))
    calc.agregar_grupo(Grupo(2, "Dra. Lagrange", [BloqueHoras(DiaSemana.MARTES, "07:00", "09:00"),
                                                  BloqueHoras(DiaSemana.JUEVES, "07:00", "09:00")]))

    fisica.agregar_grupo(Grupo(1, "Dr. Einstein", [BloqueHoras(DiaSemana.LUNES, "09:00", "11:00"),
                                                   BloqueHoras(DiaSemana.MIERCOLES, "09:00", "11:00")]))
    fisica.agregar_grupo(
        Grupo(2, "Dra. Curie", [BloqueHoras(DiaSemana.LUNES, "08:00", "10:00")]))  # <-- Grupo conflictivo

    prog.agregar_grupo(Grupo(5, "Prof. Turing", [BloqueHoras(DiaSemana.VIERNES, "10:00", "13:00")]))

    # 3. Probar una combinación VÁLIDA
    print("--- Probando una combinación VÁLIDA ---")
    try:
        seleccion_valida = {
            calc: calc.buscar_grupo(1),  # Cálculo Grupo 1 (L y M 7-9)
            fisica: fisica.buscar_grupo(1),  # Física Grupo 1 (L y M 9-11)
            prog: prog.buscar_grupo(5)  # Prog Grupo 5 (V 10-13)
        }
        horario_1 = Horario(seleccion_valida)
        print(horario_1)
    except (ValueError, TypeError) as e:
        print(f"ERROR INESPERADO: {e}")

    # 4. Probar una combinación INVÁLIDA (con conflicto)
    print("\n\n--- Probando una combinación INVÁLIDA ---")
    try:
        seleccion_invalida = {
            calc: calc.buscar_grupo(1),  # Cálculo Grupo 1 (L y M 7-9)
            fisica: fisica.buscar_grupo(2),  # Física Grupo 2 (L 8-10) <-- ¡CONFLICTO!
            prog: prog.buscar_grupo(5)
        }
        horario_2 = Horario(seleccion_invalida)
        print(horario_2)
    except ValueError as e:
        print(f"ÉXITO: El conflicto fue detectado correctamente.")
        print(f"Detalle del error:\n{e}")
