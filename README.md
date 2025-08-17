# **Generador de Horarios Universitarios (By: GiovanyTech)**

Un script de Python que genera todas las combinaciones de horarios de clases posibles y sin conflictos a partir de un catálogo de asignaturas y grupos ingresadas por el usuario. Este proyecto está construido con un fuerte enfoque en los principios de Diseño Orientado a Objetos (OOP) para garantizar un código robusto, legible y sostenible a cambios futuros.

## Características Clave

*   **Arquitectura Orientada a Objetos:** El sistema está modelado en capas de abstracción (`BloqueHoras`, `Grupo`, `Asignatura`, `Horario`), cada una con una única responsabilidad.
*   **Validación y Robustez:** Las clases se auto-validan en su creación (principio "Fail-Fast"), asegurando que no puedan existir objetos en estados inválidos (ej. un horario con conflictos).
*   **Eficiencia:** Utiliza estructuras de datos eficientes (`dict`, `set`) para búsquedas rápidas y un generador (`yield`) para producir horarios sin consumir grandes cantidades de memoria.
*   **Código Limpio y "Pythónico":** Emplea características idiomáticas de Python como decoradores (`@property`, `@staticmethod`, @total_ordering), "dunder methods" para mostrar información de los objetos (`__str__`, `__repr__`) y Type Hinting para una máxima claridad.

## ¿Cómo Ejecutarlo?

1.  Asegúrate de tener Python 3.9 o superior instalado.
2.  Clona este repositorio.
3.  Navega a la carpeta del proyecto: `cd TU_REPOSITORIO`
4.  Ejecuta el programa principal: `python main.py`
5.  Puedes modificar los datos de las materias en la función `cargar_catalogo_materias()` dentro de `main.py` para experimentar.

## Estructura del Proyecto

El proyecto está organizado en una arquitectura de capas, donde cada clase tiene una responsabilidad única. Las clases de nivel inferior (`BloqueHoras`) son utilizadas por las de nivel superior (`Grupo`, `Asignatura`) para construir el *modelo de datos* completo.

| Archivo | Descripción |
| --- | --- |
| `BloqueHoras.py` | La clase base. Representa un único bloque de tiempo indivisible. |
| `Grupo.py` | Modela un grupo específico de una asignatura (profesor y horarios). |
| `Asignatura.py` | Modela una asignatura y gestiona su colección de grupos. |
| `Horario.py` | Representa un único horario válido y validado. Responsable de la presentación final. |
| `GeneradorHorarios.py` | Contiene el motor lógico que combina y filtra los horarios, no es una clase como tal. |
| `main.py` | El punto de entrada de la aplicación. Carga los datos y orquesta la generación y visualización de horarios. |

## Conceptos de Diseño Demostrados

Este proyecto es una demostración práctica de los siguientes conceptos de ingeniería de software:

*   **Encapsulación:** Los datos internos de cada objeto están protegidos y solo se exponen a través de una API pública y segura.
*   **Inmutabilidad:** La clase `BloqueHoras` es inmutable para garantizar la integridad de los datos.
*   **Principio de Responsabilidad Única (SRP):** Cada clase tiene un propósito claro y definido, así como sus funciones (es decir, las funciones no realizan múltiples tareas, deben realizar una pero bien hecha).
*   **Programación Defensiva:** El código anticipa y maneja errores de forma elegante (`try-except`, validación de entradas).
*   **Uso de Generadores para la Eficiencia de Memoria.**
