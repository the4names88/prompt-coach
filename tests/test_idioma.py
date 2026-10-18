from app.services.llm import has_foreign_script


def test_detecta_palabra_en_hindi():
    assert has_foreign_script("Recomendaciones de अभ्यास, práctica o ejercicios.")


def test_el_espanol_con_tildes_y_eñes_no_se_marca():
    assert not has_foreign_script("Diseña un plan de estudio, ¿cómo? Año 1: niños y señales.")
