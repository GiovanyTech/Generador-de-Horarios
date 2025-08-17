# Programa para generar horarios de clases, el usuario ingresa las asignaturas y 
# el programa genera todas las combinaciones posibles de horarios
# cuidando que no se repitan horarios en el mismo día
import GeneradorHorarios
from Asignatura import Asignatura
from Grupo import Grupo
from BloqueHoras import DiaSemana, BloqueHoras
# from typing import List, Generator, Dict

def cargar_catalogo_materias():
    # --- Creamos las asignaturas ---
    eym = Asignatura("Electricidad y Magnetismo")
    ed = Asignatura("Ecuaciones Diferenciales")
    an = Asignatura("Análisis Numérico")
    md = Asignatura("Matemáticas Discretas")

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

    return [eym, ed, an, md]

if __name__ == "__main__":
    print("Iniciando generador de horarios...")

    # 1. Cargar el catálogo de materias desde nuestra estructura de datos
    materias_disponibles = cargar_catalogo_materias()
    print(f"Catálogo cargado con {len(materias_disponibles)} materias.")

    # 2. Definir cuántas materias queremos cursar
    NUMERO_MATERIAS_A_CURSAR = 4 # Podemos cambiar este número
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