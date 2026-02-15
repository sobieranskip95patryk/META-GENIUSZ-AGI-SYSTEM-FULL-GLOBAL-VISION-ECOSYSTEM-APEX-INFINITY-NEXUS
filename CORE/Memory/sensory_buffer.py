"""
Pamięć krótkotrwała (Sensory Buffer).
Przechowuje surowe dane z bieżącego cyklu przetwarzania.
"""

class SensoryBuffer:
    def __init__(self):
        self.buffer = []

    def add_input(self, data):
        self.buffer.append(data)
