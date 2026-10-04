# Lab-Solid
Repositorio para el Laboratorio de SOLID de la materia Ingeniería de Software II G3 del Departamento de Ingeniería de Sistemas e Industrial - Facultad de Ingeniería de la Universidad Nacional de Colombia.

**Lenguaje elegido:** Python (traducción 1:1 del código base en Java, conservando los defectos de diseño).

## Miembros del Equipo de trabajo

* Pablo Andres Niño Barreto (pninob@unal.edu.co)
* Sergio Tovar Vasquez (setovarv@unal.edu.co)
## Commit Inicial (Bloque 0)
Se subió el bloque 0 del laboratorio, que incluye la traducción de los códigos del laboratorio, originalmente en Java y traducidos a Python. La salida del programa principal quedó congelada en `salida_original.txt` como prueba de caracterización.

---

# Bloque 1 — Diagnóstico

Objetivo: **encontrar los problemas de diseño y medir el "antes"**, sin corregir nada todavía. Todas las evidencias, salidas y métricas de esta sección se obtuvieron ejecutando el código real de este repositorio.

## 1.1 Tabla de hallazgos

Hay al menos un problema por cada letra de SOLID; algunas clases acumulan varios. La columna de **consecuencia** está escrita en términos del negocio (qué le pasa al banco o al cliente).

| Clase / método | Letra | Evidencia en el código | Consecuencia para el banco o el cliente |
|---|:---:|---|---|
| `TransaccionService.transferir` (`transaccion_service.py`, líneas 11–47) | **S** | Un mismo método valida montos, calcula la comisión, mueve el dinero, persiste en Oracle, imprime el comprobante, envía el SMS y registra la auditoría (7 bloques comentados `# 1.` a `# 7.`). | Si el área legal pide cambiar el **texto del comprobante**, hay que tocar el mismo método que **mueve el dinero**. Un error al editar el comprobante puede terminar cobrando mal una transferencia o duplicando un cargo en producción. |
| `TransaccionService.transferir` (`transaccion_service.py`, líneas 19–26) | **O** | La comisión se decide con un `if/elif/else` sobre `tipo`: `MISMO_BANCO`, `OTRO_BANCO`, `INTERNACIONAL`. | Cada vez que el negocio lanza un **tipo nuevo de transferencia** (por llave, por ejemplo) hay que **abrir y modificar la clase central** que mueve el dinero. Cada cambio arriesga romper los tipos que ya funcionaban. |
| `CDT` hereda de `Cuenta` y sobreescribe `retirar` (`cdt.py`, líneas 9–11) | **L** | `CDT` extiende `Cuenta` pero **sobreescribe `retirar()` para lanzar `RuntimeError`** si aún no ha vencido. No cumple el contrato de su clase padre. | Cualquier proceso que trate un `CDT` como una `Cuenta` y llame `retirar()` **se cae**. El cobro masivo de cuota de manejo revienta al llegar al primer CDT (ver Experimento 1, con traceback real). |
| `CobroCuotaManejo.cobrar_mensual` (`cobro_cuota_manejo.py`, líneas 7–10) | **L** | Recorre una lista de `Cuenta` y llama `retirar()` asumiendo que **todas** permiten retirar, lo cual es falso para `CDT`. | En el batch nocturno de un millón de cuentas, basta **un** CDT en la lista para detener todo el proceso a mitad de camino: unas cuentas quedan cobradas y otras no. |
| `ProductoBancario` (`producto_bancario.py`, líneas 3–21) | **I** | Interfaz "gorda" (`ABC`) con 5 métodos abstractos obligatorios: `depositar`, `retirar`, `calcular_intereses`, `pagar_cuota`, `generar_extracto`. | Los implementadores quedan obligados a definir métodos que no les sirven. Peor: un `CreditoVivienda.depositar()` **vacío** acepta la llamada y **no hace nada** — el dinero "entra" sin error y desaparece silenciosamente. |
| `TransaccionService.__init__` (`transaccion_service.py`, líneas 7–9) | **D** | Crea sus dependencias directamente: `self._repositorio = OracleRepositorio()` y `self._sms = SmsGateway()`. | Es **imposible probar** una transferencia sin conectarse a la base de producción ni enviar un SMS real al cliente (ver Experimento 2). Migrar de Oracle a otro motor obliga a editar esta clase. |

**Hallazgos adicionales (clases con evidencia de apoyo):**

| Clase / método | Letra | Evidencia en el código | Consecuencia para el banco o el cliente |
|---|:---:|---|---|
| `Cuenta.retirar` (`cuenta.py`, líneas 21–24) | **L** | La clase base promete `retirar()` incondicional para **toda** cuenta; de ahí nace la violación del CDT. | El contrato mal diseñado en la raíz es lo que permite que un subtipo (CDT) no pueda cumplirlo. |
| `TarjetaCredito.depositar` (`tarjeta_credito.py`, línea 9) | **I** | Método vacío: `pass  # No aplica`. | Una tarjeta de crédito "acepta" un depósito que no hace nada: comportamiento engañoso para quien consume la interfaz. |
| `CreditoVivienda.depositar` y `CreditoVivienda.retirar` (`credito_vivienda.py`, líneas 7–11) | **I** | Dos métodos vacíos: `pass  # No aplica`. | Mismo riesgo de operación silenciosa que no falla pero tampoco ejecuta nada. |

## 1.2 Dos experimentos

### Experimento 1 — El CDT

**Qué hicimos:** agregamos el CDT de Ana a la lista de `CobroCuotaManejo.cobrar_mensual`. El script está en `experimentos/experimento1_cdt.py`.

> ⚠️ **Nota de fidelidad:** en `main.py` el CDT se crea con `vencimiento=date(2026, 9, 30)`, una fecha **ya vencida** hoy; eso haría que el CDT se comporte como "ya liberado" y el experimento **no** fallaría. El Java original usa `LocalDate.now().plusMonths(6)` (siempre a futuro). Para que el experimento sea fiel al enunciado, el script usa un CDT **no vencido** (`date.today() + 180 días`). *Recomendación:* corregir esa fecha en `main.py` para que la traducción sea fiel (ver nota al final).

**Qué pasa (traceback real):**

```
>>> Lista a cobrar: [ana, cdt_ana, luis]
Cuota de manejo cobrada a 001-1
Traceback (most recent call last):
  File "experimentos/experimento1_cdt.py", line 12, in <module>
    CobroCuotaManejo().cobrar_mensual([ana, cdt_ana, luis])
  File "cobro_cuota_manejo.py", line 9, in cobrar_mensual
    cuenta.retirar(self.CUOTA)
  File "cdt.py", line 11, in retirar
    raise RuntimeError("Un CDT no permite retiros antes del vencimiento")
RuntimeError: Un CDT no permite retiros antes del vencimiento
```

Se cobra la cuota a `001-1` (Ana), el proceso llega al CDT, invoca `retirar()`, el CDT lanza `RuntimeError` y el programa **se detiene**: **`001-2` (Luis) nunca recibe el cobro**. El recorrido muere en el elemento problemático y no continúa.

**Qué pasaría en producción:** si el batch corre de noche sobre **un millón de cuentas** y la cuenta número **500 000 es un CDT**, el proceso cobra correctamente las primeras 499 999, explota en la 500 000 y **deja sin cobrar las 500 000 restantes**. Resultado: cierre contable inconsistente (medio banco cobrado, medio no) y una falla que probablemente nadie note hasta la conciliación. Un único dato "raro" tumba todo el proceso.

### Experimento 2 — La prueba imposible

**Qué intentamos:** escribir una prueba que verifique que una transferencia a otro banco cobra $7 500 de comisión, **sin conectarse a Oracle ni enviar SMS**. El script está en `experimentos/test_prueba_imposible.py`.

**Qué pasó al ejecutarla (salida real de `pytest -s`):**

```
[ORACLE] Conectando a jdbc:oracle:thin:@prod-db:1521/BANCO...
[ORACLE] INSERT INTO transacciones VALUES ('001-1', '001-2', 100000, 7500.0)
===== BANCO ANDINO - COMPROBANTE =====
Origen: 001-1
Destino: 001-2
Monto: $100000
Comisión: $7500.0
=====================================
[SMS] Conectando al proveedor de mensajeria...
[SMS] Para Ana: Transferiste $100000 a la cuenta 001-2
[AUDITORIA] 2026-10-01 ... OTRO_BANCO 001-1->001-2 $100000
.
1 passed in 0.01s
```

**¿Lo logramos?** **No.** El `assert` sobre la comisión sí pasa, pero la prueba **no pudo evitar** que se ejecutaran el repositorio y el SMS: en la salida aparecen `[ORACLE] Conectando a ... prod-db ...` y `[SMS] Conectando al proveedor ...`.

**¿Qué lo impide?** `TransaccionService.__init__` **crea sus dependencias adentro** (`OracleRepositorio()` y `SmsGateway()`). No hay ningún punto (parámetro ni setter) por donde inyectar una versión falsa. Por eso, cada corrida de la prueba:

- Golpea la "base de producción" (`[ORACLE] Conectando a jdbc:oracle:thin:@prod-db...`).
- Envía un "SMS real" al cliente (`[SMS] Para Ana...`).

Capturar la consola no desacopla nada: seguimos conectando a Oracle y mandando SMS en cada corrida. Este es el síntoma exacto del problema **D (DIP)**, que se resuelve en el Punto de control D del Bloque 2.

## 1.3 Medición "antes"

| Métrica | Antes |
|---|:---:|
| Líneas del método `transferir` | **23 líneas de código** (cuerpo de 36 líneas: 23 de código + 7 comentarios + 6 en blanco) |
| Número de razones distintas por las que `TransaccionService` podría cambiar | **7** (validación · comisión · movimiento de dinero · persistencia · comprobante · notificación · auditoría) |
| Clases concretas que `TransaccionService` instancia directamente (`new`) | **2** (`OracleRepositorio`, `SmsGateway` — líneas 8–9) |
| Métodos vacíos o que lanzan excepción por "no aplica" | **3 vacíos** (`TarjetaCredito.depositar`, `CreditoVivienda.depositar`, `CreditoVivienda.retirar`) **+ 1 que lanza excepción** (`CDT.retirar`) |
| ¿Se puede probar `transferir` sin Oracle ni SMS? | **No** (demostrado en el Experimento 2) |

## 1.4 Diagrama de clases del código original

Diagrama UML del código base. En **rojo** se marcan las herencias y dependencias problemáticas (las que causan las violaciones SOLID). Este bloque Mermaid se renderiza automáticamente en GitHub.

```mermaid
classDiagram
    direction TB

    class Cuenta {
        #numero
        #titular
        #saldo
        +depositar(monto)
        +retirar(monto)
    }
    class CuentaAhorros
    class CDT {
        -vencimiento
        +retirar(monto)
    }
    class TransaccionService {
        -repositorio
        -sms
        +transferir(origen, destino, monto, tipo)
    }
    class OracleRepositorio {
        +guardar_transaccion(origen, destino, monto, comision)
    }
    class SmsGateway {
        +enviar(destinatario, mensaje)
    }
    class CobroCuotaManejo {
        +cobrar_mensual(cuentas)
    }
    class ProductoBancario {
        <<abstract>>
        +depositar(monto)
        +retirar(monto)
        +calcular_intereses()
        +pagar_cuota(monto)
        +generar_extracto()
    }
    class TarjetaCredito {
        -deuda
        -cupo
        +depositar(monto)
        +retirar(monto)
        +calcular_intereses()
        +pagar_cuota(monto)
        +generar_extracto()
    }
    class CreditoVivienda {
        -saldo_pendiente
        +depositar(monto)
        +retirar(monto)
        +calcular_intereses()
        +pagar_cuota(monto)
        +generar_extracto()
    }
    class Main {
        +main()
    }

    Cuenta <|-- CuentaAhorros
    Cuenta <|-- CDT
    ProductoBancario <|-- TarjetaCredito
    ProductoBancario <|-- CreditoVivienda
    TransaccionService ..> OracleRepositorio : new
    TransaccionService ..> SmsGateway : new
    TransaccionService ..> Cuenta : usa
    CobroCuotaManejo ..> Cuenta : retirar()
    Main ..> TransaccionService : new
    Main ..> CobroCuotaManejo : new
    Main ..> CuentaAhorros : new
    Main ..> CDT : new
    Main ..> TarjetaCredito : new
    Main ..> CreditoVivienda : new

    classDef problema fill:#ffe3e3,stroke:#d00000,stroke-width:2px,color:#660000;
    class CDT problema
    class TransaccionService problema
    class ProductoBancario problema

    linkStyle 1 stroke:#d00000,stroke-width:2px
    linkStyle 2 stroke:#d00000,stroke-width:2px
    linkStyle 3 stroke:#d00000,stroke-width:2px
    linkStyle 4 stroke:#d00000,stroke-width:2px
    linkStyle 5 stroke:#d00000,stroke-width:2px
    linkStyle 7 stroke:#d00000,stroke-width:2px
```

**Lectura del diagrama (qué está en rojo y por qué):**

- `CDT ──▷ Cuenta` (herencia) → **LSP**: el subtipo no cumple el contrato de `retirar()`.
- `CobroCuotaManejo ┄> Cuenta` (`retirar()`) → punto donde la violación LSP **explota** en ejecución.
- `TarjetaCredito ┄▷ ProductoBancario` y `CreditoVivienda ┄▷ ProductoBancario` → **ISP**: obligan a implementar métodos vacíos.
- `TransaccionService ┄> OracleRepositorio` y `┄> SmsGateway` (ambas con `new`) → **DIP**: dependen de clases concretas creadas adentro.
- `TransaccionService` (nodo rojo) → **SRP + OCP**: concentra 7 responsabilidades y el `if/elif` por tipo.
- `ProductoBancario` (nodo rojo) → **ISP**: interfaz gorda.

Las dependencias de `Main` hacia las clases concretas quedan en negro: `Main` es el punto de armado del sistema, y ahí sí es legítimo instanciar (eso se refuerza en el Punto de control D).

---

### Nota pendiente para corregir en Bloque 0 (fidelidad de la traducción)

En `main.py`, el CDT se crea con `date(2026, 9, 30)` (fecha fija ya vencida). El Java original usa `LocalDate.now().plusMonths(6)`. Para ser fiel al código base conviene cambiarlo por una fecha futura relativa, por ejemplo `date.today() + timedelta(days=180)`. No afecta a `salida_original.txt` (en `main.py` el CDT solo se construye, nunca se retira), pero sí importa para la coherencia del dominio y para los bloques siguientes.

**Commit del bloque:** `bloque-1-diagnostico`


## Bloque 2 — Refactorización

En este bloque se refactoriza el sistema aplicando los principios SOLID de forma progresiva, manteniendo el comportamiento original del programa.

Después de cada punto de control se compara la salida del programa con `salida_original.txt` para verificar que la refactorización no haya alterado su comportamiento.

### Punto de Control S — Single Responsibility Principle

En el código original, el método `transferir()` de `TransaccionService` concentraba diferentes responsabilidades dentro de una misma clase:

1. Validación del monto.
2. Cálculo de la comisión.
3. Movimiento del dinero entre las cuentas.
4. Persistencia de la transacción.
5. Generación del comprobante.
6. Notificación mediante SMS.
7. Registro de auditoría.

Esta concentración hacía que `TransaccionService` tuviera múltiples razones para cambiar. Por ejemplo, un cambio en el formato del comprobante o en la forma de realizar la auditoría obligaría a modificar la misma clase encargada de coordinar la transferencia.

Para aplicar el principio de Responsabilidad Única (SRP), se separaron varias de estas responsabilidades en clases independientes:

- `ValidadorTransferencia`: se encarga de validar el monto de la transferencia.
- `CalculadorComision`: se encarga de calcular la comisión según el tipo de transferencia.
- `GeneradorComprobante`: se encarga de generar e imprimir el comprobante.
- `AuditorTransferencia`: se encarga de registrar la auditoría de la operación.

De esta forma, `TransaccionService` pasó a encargarse principalmente de coordinar el flujo de una transferencia utilizando los componentes especializados.

#### Estructura después de aplicar SRP

```text
TransaccionService
├── ValidadorTransferencia
├── CalculadorComision
├── GeneradorComprobante
├── AuditorTransferencia
├── OracleRepositorio
└── SmsGateway


### Punto de Control O — Open/Closed Principle

En el código original, el cálculo de la comisión dependía de una
estructura condicional que verificaba el tipo de transferencia.
Para agregar un nuevo tipo era necesario modificar el código
existente de `CalculadorComision`.

Para aplicar el principio Abierto/Cerrado (OCP), se creó la
abstracción `TipoTransferencia`, que define el comportamiento que
debe tener cada tipo de transferencia.

Se implementaron las siguientes clases:

- `TransferenciaMismoBanco`
- `TransferenciaOtroBanco`
- `TransferenciaInternacional`

Cada una implementa su propia forma de calcular la comisión.

`CalculadorComision` ahora depende de la abstracción
`TipoTransferencia` y simplemente delega en ella el cálculo:

```python
def calcular(self, monto: float, tipo: TipoTransferencia) -> float:
    return tipo.calcular_comision(monto)