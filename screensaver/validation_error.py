
# TODO: BADSMELL: This seems and exception message but do not includes context.
# TODO: The name should be in relation of root of error (Position invalid)
class ValidationError:
    def __init__(self, message):
        self.message = message
