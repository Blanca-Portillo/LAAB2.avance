class MetaAhorro:
    def __init__(self, nombre, objetivo_monto, fecha_objetivo):
        self.nombre = nombre
        self.objetivo_monto = objetivo_monto
        self.fecha_objetivo = fecha_objetivo
        self.monto_ahorrado = 0

    def agregar_ahorro(self, monto):
        self.monto_ahorrado += monto
        if self.monto_ahorrado > self.objetivo_monto:
            self.monto_ahorrado = self.objetivo_monto  # No permitir que se ahorre más que el objetivo

    def mostrar_progreso(self):
        progreso = (self.monto_ahorrado / self.objetivo_monto) * 100
        return f"Progreso hacia '{self.nombre}': {progreso}% (Monto ahorrado: ${self.monto_ahorrado}, Objetivo: ${self.objetivo_monto})"

# Ejemplo de uso
meta = MetaAhorro("Vacaciones", 1500, "2025-06-01")
meta.agregar_ahorro(300)
print(meta.mostrar_progreso())
