# Programa para generar horarios de clases, el usuario ingresa las asignaturas y 
# el programa genera todas las combinaciones posibles de horarios
# cuidando que no se repitan horarios en el mismo día
import GeneradorHorarios
from Asignatura import Asignatura
from Grupo import Grupo
from BloqueHoras import DiaSemana, BloqueHoras
from typing import List, Generator, Dict

def cargar_catalogo_materias():
    # Definir las asignaturas a cursar
    eym = Asignatura("Electricidad y Magnetismo")
    lab_eym = Asignatura("Laboratorio de EyM")
    ed = Asignatura("Estructuras Discretas")
    cyc = Asignatura("Cultura y Comunicación")

    # Poblar cada asignatura con sus grupos y horarios disponibles
    eym.agregar_grupo(Grupo(8, "M.I. Germán Ramón Arconada", [
        BloqueHoras(DiaSemana.LUNES, "17:00", "19:00"),
        BloqueHoras(DiaSemana.MIERCOLES, "17:00", "19:00")]))
    eym.agregar_grupo(Grupo(17, "Ing. Santiago Gonzalez Lopez", [
        BloqueHoras(DiaSemana.MARTES, "19:00", "21:00"),
        BloqueHoras(DiaSemana.JUEVES, "19:00", "21:00")
    ]))
    eym.agregar_grupo(Grupo(5, "M.I. Mayverena Jurado Pineda", [
        BloqueHoras(DiaSemana.LUNES, "11:00", "13:00"),
        BloqueHoras(DiaSemana.MIERCOLES, "11:00", "13:00")
    ]))

    lab_eym.agregar_grupo(Grupo(12, "MI. Rafael Guillermo Suarez Najera", [
        BloqueHoras(DiaSemana.MARTES, "17:00", "19:00")
    ]))

    ed.agregar_grupo(Grupo(1, "M.I. Yi Tan Li", [
        BloqueHoras(DiaSemana.MARTES, "17:00", "19:00"),
        BloqueHoras(DiaSemana.JUEVES, "17:00", "19:00")
    ]))

    ed.agregar_grupo(Grupo(5, "Ing. Orlando Zaldivar Zamorategui", [
        BloqueHoras(DiaSemana.MARTES, "15:00", "17:00"),
        BloqueHoras(DiaSemana.JUEVES, "15:00", "17:00")
    ]))

    cyc.agregar_grupo(Grupo(27, "Ing. Jorge Velazquez", [
        BloqueHoras(DiaSemana.MIERCOLES, "19:00", "21:00"),
        BloqueHoras(DiaSemana.JUEVES, "19:00", "21:00")
    ]))

    return [eym, lab_eym, ed, cyc]

if __name__ == "__main__":
    print("Iniciando generador de horarios...")

    # 1. Cargar el catálogo de materias desde nuestra estructura de datos
    materias_disponibles = cargar_catalogo_materias()
    print(f"Catálogo cargado con {len(materias_disponibles)} materias.")

    # 2. Definir cuántas materias queremos cursar
    NUMERO_MATERIAS_A_CURSAR = 3 # Podemos cambiar este número
    print(f"Buscando combinaciones de horarios para {NUMERO_MATERIAS_A_CURSAR} materias de {len(materias_disponibles)} disponbiles")
    print("-" * 50)

    # 3. Generar y visualizar los horarios válidos
    horarios_encontrados = 0
    horarios = GeneradorHorarios.encontrar_horarios(materias_disponibles, NUMERO_MATERIAS_A_CURSAR)
    lista_horarios = list(horarios) # Convertimos el generador a una lista para poder contar los resultados

    if not lista_horarios:
        print("\nNo se encontraron combinaciones de horarios válidos.")
    else:
        print(f"\n¡Éxito! Se encontraron {len(lista_horarios)} horarios posibles:")
        for i, horario_valido in enumerate(lista_horarios):
            # Simplemente imprimimos el objeto Horario.
            # Python llamará automáticamente a su método __str__
            print(horario_valido)

''' 
    < Otra forma de mandar a imprimir los horarios: >
    horarios_encontrados = 0
    horarios = GeneradorHorarios.encontrar_horarios(materias_disponibles, NUMERO_MATERIAS_A_CURSAR)

    for h in horarios:
        horarios_encontrados += 1
        print(f"\n==================== OPCIÓN DE HORARIO #{horarios_encontrados} ====================")
        # Iteramos sobre los pares (asignatura, grupo)
        for asignatura, grupo_seleccionado in h.seleccion.items():
            print(f"  Materia: {asignatura.nombre}")
            print(f"  Grupo Seleccionado: {grupo_seleccionado.id_grupo} - {grupo_seleccionado.profesor}")
        print("=" * 60)

    if horarios_encontrados == 0:
        print("\nNo se encontraron combinaciones de horarios válidos.")
    else:
        print(f"\nSe encontraron {horarios_encontrados} combinaciones en total.")
'''