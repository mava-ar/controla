
def es_continuar(raw_value):
    if raw_value is None or raw_value is '':
        raw_value = "y"
    return (True if (raw_value == "y" or raw_value == "Y") else False)
