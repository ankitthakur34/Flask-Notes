class NoteNotFoundException(Exception):
    def __init__(self, message="Note not found",status_code=404):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

