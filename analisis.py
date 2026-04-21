def detectar_tema(pregunta):

    pregunta = pregunta.lower()

    if "clase" in pregunta or "objeto" in pregunta:
        return "POO"

    if "herencia" in pregunta:
        return "Herencia"

    if "polimorfismo" in pregunta:
        return "Polimorfismo"

    if "encapsulamiento" in pregunta:
        return "Encapsulamiento"

    return "General"