from repositorio_transacciones import RepositorioTransacciones


class PostgresRepositorio(RepositorioTransacciones):
    """R5 - Repositorio de transacciones sobre PostgreSQL.

    Implementa la misma abstracción RepositorioTransacciones que
    OracleRepositorio. La migración consiste en inyectar esta clase en
    lugar de la de Oracle desde main.py; la clase de Oracle se conserva
    intacta por si hay que devolverse durante la migración.
    """

    def guardar_transaccion(
        self,
        origen: str,
        destino: str,
        monto: float,
        comision: float
    ) -> None:
        print("[POSTGRES] Conectando a postgresql://prod-db:5432/banco...")
        print(
            f"[POSTGRES] INSERT INTO transacciones VALUES "
            f"('{origen}', '{destino}', {monto}, {comision})"
        )
