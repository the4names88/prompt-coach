from app.services.analysis import validate_prompt


def test_prompt_con_dame_y_tabla_saca_puntaje_completo():
    r = validate_prompt(
        "Eres un tutor de Python. Dame un plan de estudio de 4 semanas "
        "para un principiante. Responde en una tabla."
    )
    assert r["score"] == 100
    assert r["is_valid"] is True