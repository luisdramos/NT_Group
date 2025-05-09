class NaturalSet100:
    def __init__(self):
        self.full_set = set(range(1, 101))
        self.current_set = self.full_set.copy()
        self.extracted = None

    def extract(self, number: int):
        if number not in self.full_set:
            raise ValueError("El numero debe estar entre 1 y 100")
        
        if number not in self.current_set:
            raise ValueError(f"El numero {number} ya fue extraido anteriormente")
        self.current_set.remove(number)
        self.extracted = number

    def get_missing_number(self):
        if len(self.current_set) != 99:
            raise ValueError("No se ha extraído exactamente un numero.")
        return list(self.full_set - self.current_set)[0]
    
    def get_available_numbers(self):
        return sorted(self.current_set)