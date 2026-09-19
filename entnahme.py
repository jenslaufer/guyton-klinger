"""Die Leitplanken-Entscheidung — ohne Streamlit, damit sie prüfbar ist."""


def naechste_entnahme(
    vorjahres_entnahme,
    depotwert,
    inflation,
    obere_schwelle,
    untere_schwelle,
    schritt,
):
    """Entnahme für das Folgejahr nach der Leitplanken-Regel.

    Erst Inflationsanpassung, dann die daraus folgende Entnahmerate gegen die
    beiden Schwellen halten. Gibt die neue Entnahme und die gegriffene Regel
    zurück ("oben", "unten" oder "standard").

    Die Schwellen sind absolute Raten, keine Abweichungen — sie werden einmal
    aus der Startrate gerechnet und bleiben über alle Jahre stehen.
    """
    entnahme = vorjahres_entnahme * (1 + inflation)
    rate = entnahme / depotwert

    if rate > obere_schwelle:
        return entnahme * (1 - schritt), "oben"
    if rate < untere_schwelle:
        return entnahme * (1 + schritt), "unten"
    return entnahme, "standard"
