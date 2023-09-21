# Crea un generador de números pseudoaleatorios entre 0 y 100.
# - No puedes usar ninguna función "random" (o semejante) del lenguaje de programación seleccionado.

# Es más complicado de lo que parece... 

# He usado como semilla el tiempo transcurrido en segundos desde las 00.00 H del dia anterior, pero se puede mejorar
# incluyendo la fecha como numero adicional

from datetime import datetime
from typing import Generator, Tuple

def wellrng(seed: Tuple[int, ...]) -> Generator[int, None, None]:
    M1 = 3
    M2 = 24
    M3 = 10

    def mat0pos(t: int, v: int) -> int:
        return v ^ (v >> t)

    def mat0neg(t: int, v: int) -> int:
        return v ^ (v << (~t))

    def identity(v: int) -> int:
        return v

    state = list(seed)
    state += [0] * (32 - len(seed))  # Rellenar con ceros para tener una longitud de 32
    state_i = 0

    while True:
        z0 = state[(state_i + M1) & 0x001f]
        z1 = identity(state[state_i]) ^ mat0pos(8, state[(state_i + M1) & 0x001f])
        z2 = mat0neg(-19, state[(state_i + M2) & 0x001f]) ^ mat0neg(-14, state[(state_i + M3) & 0x001f])

        newV1 = z1 ^ z2
        newV0 = mat0neg(-11, z0) ^ mat0neg(-7, z1) ^ mat0neg(-13, z2)

        state[state_i] = newV1
        state_i = (state_i + 31) & 0x001f

        yield int(newV0) % 101

# Obtener la hora actual y calcular la diferencia de tiempo desde la medianoche
now = datetime.now()
time_diff = now - now.replace(hour=0, minute=0, second=0, microsecond=0)

# Usar la diferencia de tiempo como semilla
seed = (time_diff.seconds,)

generador = wellrng(seed)

# Ejemplo de uso
for _ in range(11):
    numero_pseudoaleatorio = next(generador)
    print(numero_pseudoaleatorio)
