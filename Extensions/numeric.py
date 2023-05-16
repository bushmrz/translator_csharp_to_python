class Numeric:
    @staticmethod
    def perform_operation(operation, value1, value2):
        if isinstance(value1, int) and isinstance(value2, int) or (isinstance(value1, float) and isinstance(value2, float)):
            return operation(value1, value2)
        return None

    @staticmethod
    def perform_comparison(operation, value1, value2):
        if isinstance(value1, int) and isinstance(value2, int) or (isinstance(value1, float) and isinstance(value2, float)):
            return operation(value1, value2)
        return None
