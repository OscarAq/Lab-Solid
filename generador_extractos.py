from producto_bancario import ProductoBancario


class GeneradorExtractos:
    def generar(self, producto: ProductoBancario) -> str:
        return producto.generar_extracto()