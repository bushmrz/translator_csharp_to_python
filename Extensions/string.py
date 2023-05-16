class String:
    @staticmethod
    def perform_operation(operation, value1, value2):
        if isinstance(value1, str) and isinstance(value2, str):
            return operation(value1, value2)
        return None
