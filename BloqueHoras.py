from enum import Enum
from datetime import time
from functools import total_ordering

# Usar una enumeración (Enum) para los días de la semana. Ventajas:
# 1. Autocompletado en IDEs.
# 2. Evita errores por escribir mal un string (ej. "Miercoles" sin tilde).
# 3. Centraliza los valores permitidos en un solo lugar.
class DiaSemana(Enum):
    LUNES = "Lunes"
    MARTES = "Martes"
    MIERCOLES = "Miércoles"
    JUEVES = "Jueves"
    VIERNES = "Viernes"
    SABADO = "Sábado"

# El decorador @total_ordering genera automáticamente los métodos de comparación
# (__lt__, __le__, __gt__, __ge__) a partir de la definición de __eq__ y __lt__.
# Esto nos permite ordenar los bloques de horario fácilmente.
@total_ordering
class BloqueHoras:
    """
    Representa un intervalo de tiempo indivisible en un horario, definido por un día de la semana y horas de inicio y fin.
    Esta clase está diseñada para ser inmutable: una vez que se crea un BloqueHoras, sus propiedades (día, inicio, fin) no pueden cambiar.
    """
    def __init__(self, dia: DiaSemana, hora_inicio: str | time, hora_fin: str | time) -> None:

        # Hacemos el constructor más flexible: aceptamos tanto strings como objetos 'time'.
        # Si es un string, lo convertimos. Si ya es 'time', lo usamos directamente.
        # Usar objetos 'time' es mucho mejor para comparaciones que usar strings

        # 1. Validar y asignar el día
        self._dia = BloqueHoras._validar_dia(dia)

        # 2. Validar, convertir y asignar las horas usando nuestro método auxiliar.
        self._inicio = BloqueHoras._validar_y_convertir_hora(hora_inicio, "hora_inicio")
        self._fin = BloqueHoras._validar_y_convertir_hora(hora_fin, "hora_fin")

        # 3. Realizar la validación cruzada final.
        if self._inicio >= self._fin:
            raise ValueError(
                f"La hora de inicio ({self._inicio}) debe ser anterior a la hora de fin ({self._fin}).")

    # Métodos privados
    @staticmethod
    def _validar_dia(dia) -> DiaSemana:
        """Válida si un día pertenece a la Enum DíaSemana"""
        if not isinstance(dia, DiaSemana):
            raise TypeError("El día debe ser un miembro de la enumeración DiaSemana.")
        return dia

    @staticmethod
    def _validar_y_convertir_hora(valor: str | time, nombre_parametro: str) -> time:
        """
        Método auxiliar protegido que valida y convierte un input a un objeto 'time'. Es reutilizable para hora_inicio y hora_fin.

        Args:
            valor: El input a validar (puede ser str o time).
            nombre_parametro: El nombre original del parámetro para mensajes de error claros.

        Returns:
            Un objeto 'time' validado.

        Raises:
            TypeError: Si el valor no es ni 'str' ni 'time'.
            ValueError: Si el string de la hora tiene un formato incorrecto.
        """
        if isinstance(valor, time):
            return valor
        if isinstance(valor, str):
            try:
                return time.fromisoformat(valor)
            except ValueError:
                # Capturamos el error de formato para dar un mensaje más específico.
                raise ValueError(f"El string para '{nombre_parametro}' ('{valor}') no tiene un formato HH:MM válido.")

        # Si no es ni 'time' ni 'str', lanzamos un error.
        raise TypeError(f"El argumento '{nombre_parametro}' debe ser un string en formato HH:MM o un objeto time.")

    # --- Propiedades públicas de solo lectura ---
    # Exponemos los valores a través de propiedades para asegurar la inmutabilidad.

    @property
    def dia(self) -> DiaSemana:
        """El día de la semana para este bloque"""
        return self._dia

    @property
    def inicio(self) -> time:
        """La hora de inicio del bloque como un objeto time."""
        return self._inicio

    @property
    def fin(self) -> time:
        """La hora de fin del bloque como un objeto time."""
        return self._fin

    @property
    def duracion_minutos(self) -> int:
        """Calcula la duración del bloque en minutos."""
        # Se convierte a minutos para evitar problemas con la resta de objetos time.
        inicio_minutos = self.inicio.hour * 60 + self.inicio.minute
        fin_minutos = self.fin.hour * 60 + self.fin.minute
        return fin_minutos - inicio_minutos

    # --- Métodos "mágicos" (Dunder methods) ---

    def __repr__(self) -> str:
        """
        Representación textual no ambigua del objeto, ideal para desarrolladores y debugging.
        ej. BloqueHoras (DiaSemana.LUNES, '07:00', '09:00')
        """
        # self.__class__.__name__ es una forma dinámica de obtener el nombre de la clase de cualquier objeto.
        return f"{self.__class__.__name__} (DiaSemana.{self.dia.name}, '{self.inicio.strftime('%H:%M')}', '{self.fin.strftime('%H:%M')}')"

    def __str__(self) -> str:
        """
        Representación textual legible para el usuario final. Se invoca al usar print(objeto).
        ej. Lunes de 07:00 a 09:00
        """
        return f"{self.dia.value} de {self.inicio.strftime('%H:%M')} a {self.fin.strftime('%H:%M')}"

    def __eq__(self, otro: object) -> bool:
        """
        Permite la comparación de igualdad (==). Dos bloques son iguales si
        tienen el mismo día, hora de inicio y hora de fin.
        """
        if not isinstance(otro, BloqueHoras): # Nos aseguramos que compararemos dos BloqueHoras
            return NotImplemented
        return self.dia == otro.dia and self.inicio == otro.inicio and self.fin == otro.fin

    def __hash__(self) -> int:
        """
        Permite que los objetos BloqueHoras se puedan usar en colecciones
        basadas en hash, como sets o como llaves de diccionarios.
        Esencial para operaciones eficientes como eliminar duplicados.
        """
        return hash((self.dia, self.inicio, self.fin))

    def __lt__(self, otro: object) -> bool:
        """
        Define el orden natural de los bloques (menor que, <).
        Se ordena primero por día y luego por hora de inicio.
        """
        if not isinstance(otro, BloqueHoras):
            return NotImplemented
        # Mapeamos días a números para poder compararlos, la posición (el índice) de cada día representa su orden en la semana
        dias_ordenados = list(DiaSemana)
        if self.dia != otro.dia:
            return dias_ordenados.index(self.dia) < dias_ordenados.index(otro.dia)
        return self.inicio < otro.inicio

    # --- Métodos Públicos ---

    def se_solapa_con(self, otro_bloque: 'BloqueHoras') -> bool:
        """Verifica si este bloque de horario choca con otro."""
        if self.dia != otro_bloque.dia:
            return False # No pueden chocar si son en días diferentes

        # Dos bloques [A, B] y [C, D] se solapan si A < D y C < B
        return self.inicio < otro_bloque.fin and otro_bloque.inicio < self.fin


# --- Ejemplo de uso ---
if __name__ == "__main__":
    try:
        # Crear bloques usando la enumeración y strings para las horas
        bloque_electromagnetismo_L = BloqueHoras(DiaSemana.LUNES, "13:00","15:00")
        bloque_electromagnetismo_M = BloqueHoras(DiaSemana.MIERCOLES, "13:00", "15:00")

        bloque_estructuras_L = BloqueHoras(DiaSemana.MARTES, "05:00", "07:00")
        bloque_calculo_L = BloqueHoras(DiaSemana.LUNES, "07:00", "09:00")
        bloque_fisica_L = BloqueHoras(DiaSemana.LUNES, "08:30", "10:00")
        bloque_programacion_L = BloqueHoras(DiaSemana.LUNES, "09:00", "11:00")
        bloque_etica_M = BloqueHoras(DiaSemana.MARTES, "12:00", "14:00")

        # También se pueden crear usando objetos 'time'
        bloque_calculo_L_duplicado = BloqueHoras(DiaSemana.LUNES, time(7, 0), time(9, 0))

        print("--- Representaciones de Objetos ---")
        print(f"str (amigable): {str(bloque_calculo_L)}")
        print(f"repr (debug):   {repr(bloque_calculo_L)}")
        print("-" * 20)

        print("\n--- Comparaciones (==) ---")
        print(f"¿Cálculo y Física son iguales? {bloque_calculo_L == bloque_fisica_L}")
        print(f"¿Cálculo y su duplicado son iguales? {bloque_calculo_L == bloque_calculo_L_duplicado}")
        print("-" * 20)

        print("\n--- Detección de Solapamiento ---")
        print(
            f"¿Cálculo ({bloque_calculo_L.inicio.strftime('%H:%M')}-{bloque_calculo_L.fin.strftime('%H:%M')}) se solapa con Física ({bloque_fisica_L.inicio.strftime('%H:%M')}-{bloque_fisica_L.fin.strftime('%H:%M')})? "
            f"{bloque_calculo_L.se_solapa_con(bloque_fisica_L)}")

        print(
            f"¿Cálculo ({bloque_calculo_L.inicio.strftime('%H:%M')}-{bloque_calculo_L.fin.strftime('%H:%M')}) se solapa con Programación ({bloque_programacion_L.inicio.strftime('%H:%M')}-{bloque_programacion_L.fin.strftime('%H:%M')})? "
            f"{bloque_calculo_L.se_solapa_con(bloque_programacion_L)}")  # No se solapan, uno termina justo cuando el otro empieza

        print(f"¿Cálculo ({bloque_calculo_L.dia.value}) se solapa con Ética ({bloque_etica_M.dia.value})? "
              f"{bloque_calculo_L.se_solapa_con(bloque_etica_M)}")
        print("-" * 20)

        print("\n--- Uso en Sets (gracias a __hash__ y __eq__) ---")
        horarios_unicos = {bloque_calculo_L, bloque_fisica_L, bloque_calculo_L_duplicado, bloque_electromagnetismo_L}
        print(f"Bloques iniciales: 3, Bloques únicos en el set: {len(horarios_unicos)}")
        print("Contenido del set:")
        for b in horarios_unicos:
            print(f"  - {b}")
        print("-" * 20)

        print("\n--- Ordenamiento (gracias a @total_ordering) ---")
        lista_desordenada = [bloque_programacion_L, bloque_etica_M, bloque_calculo_L, bloque_electromagnetismo_L]
        print("Lista original:", [str(b) for b in lista_desordenada])
        lista_desordenada.sort()
        print("Lista ordenada:", [str(b) for b in lista_desordenada])
        print("-" * 20)

        print(f"\nDuración de la clase de Ética: {bloque_etica_M.duracion_minutos} minutos.")

    except (ValueError, TypeError) as e:
        print(f"\nERROR: Ha ocurrido un problema al crear un bloque de horario.")
        print(f"Detalle: {e}")