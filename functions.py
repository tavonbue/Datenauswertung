# Funktion, um zu überprüfen, ob eine Zelle numerisch ist
def is_numeric(val):
    import pandas as pd
    try:
        pd.to_numeric(val)
        return True
    except ValueError:
        return False