# Archivo: GeneradorHorarios.py
from itertools import combinations, product
from Asignatura import Asignatura
from Grupo import Grupo
from Horario import Horario
from typing import List, Generator, Dict


def encontrar_horarios(catalogo: List[Asignatura], num_materias: int) -> Generator[Horario, None, None]:
    """
    El motor principal. Genera todas las combinaciones de horarios válidos. Utiliza un generador para producir objetos
    Horario válidos uno a la vez, lo cual es muy eficiente en memoria.

    :param catalogo: La lista completa de objetos Asignatura disponibles.
    :param num_materias: El número de materias que el usuario desea cursar.
    :yields: Un objeto Horario válido y sin conflictos.
    """

    # Fase 1: Generar cada posible subconjunto de asignaturas
    for conjunto_materias in combinations(catalogo, num_materias):

        # Creamos una lista donde cada elemento es una lista de grupos disponibles para cada asignatura
        # ej: [ [G1_Calc, G2_Calc], [G1_Fis], [G1_Prog, G2_Prog] ]
        lista_de_grupos_por_materia = [m.grupos for m in conjunto_materias]

        # Fase 2: Generar cada posible combinación de grupos (tomando un grupo por asignatura).
        # 'horario_propuesto' será una tupla de Grupos, ej: (G1_Calc, G1_Fis, G2_Prog)
        for horario_propuesto_tupla in product(*lista_de_grupos_por_materia):

            # Fase 3: Ensamblar el diccionario y VALIDAR a través del constructor de Horario.
            # zip crea los pares: (Asignatura_A, Grupo_A1) y (Asignatura_B, Grupo_B1)
            seleccion_dict: Dict[Asignatura, Grupo] = dict(zip(conjunto_materias, horario_propuesto_tupla))

            try:
                # Intentamos crear el objeto Horario.
                # El propio __init__ de Horario llamará a _validar_conflictos.
                horario_valido = Horario(seleccion_dict)

                # Si la línea anterior no lanzó un error, el horario es válido. Lo entregamos.
                yield horario_valido

            except ValueError:
                # Si Horario() lanza un ValueError, significa que hay un conflicto.
                # Simplemente lo ignoramos y continuamos con la siguiente combinación.
                continue