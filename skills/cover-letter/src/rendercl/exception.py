class RenderCLUserError(Exception):
    """An error caused by the user's input (missing file, invalid YAML), not a bug.

    Caught by `cli.error_handler.handle_user_errors` and shown as a clean
    message instead of a raw traceback, the same split rendercv makes between
    its own `RenderCVUserError` and unexpected internal errors.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
