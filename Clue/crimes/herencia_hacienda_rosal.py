"""
herencia_hacienda_rosal.py — La Herencia Maldita de Hacienda El Rosal

Don Evaristo fue hallado muerto con sedante disuelto en su medicación nocturna.
Don Evaristo había anunciado esa tarde que cambiaría su testamento al día siguiente.
La Enfermera Campos tiene coartada verificada por la cámara de la enfermería.
El Abogado Restrepo hereda con el testamento actual y quedaría excluido si el testamento cambiara.
El Sobrino Esteban hereda con el testamento actual y también quedaría excluido si el testamento cambiara.
La Secretaria Luna no hereda con el testamento actual, pero sí lo haría con el nuevo.
Las huellas del Sobrino Esteban aparecen en el vaso de medicación adulterada.
El vaso con medicación adulterada es el objeto del crimen.
El Abogado Restrepo, el Sobrino Esteban y la Secretaria Luna no tienen coartada verificada.
El Sobrino Esteban acusa a la Secretaria Luna.
El Abogado Restrepo acusa al Sobrino Esteban.
La Secretaria Luna declara que el Sobrino Esteban estuvo con ella esa noche.

Como detective, he llegado a las siguientes conclusiones:
Quien tiene coartada verificada por medios objetivos queda descartado.
Quien hereda actualmente y perdería con el cambio de testamento tiene motivo doble para evitar ese cambio.
Quien tiene huellas en el objeto del crimen tiene evidencia física en su contra.
Quien tiene motivo doble, sin coartada y con evidencia física en su contra es culpable.
Cuando el culpable acusa a otra persona para desviar la investigación, esa acusación es un desvío sospechoso.
Quien da coartada al culpable está encubriendo el crimen.
Una acusación es corroborada cuando el acusador también tiene motivo doble y el acusado tiene evidencia física.
"""

from src.crime_case import CrimeCase
from src.predicate_logic import KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    kb = KnowledgeBase()

    esteban = Term("esteban")

    kb.add_fact(Predicate("sin_coartada", (esteban,)))
    kb.add_fact(Predicate("huellas_en", (esteban, Term("vaso"))))

    kb.add_rule(Rule(
        head=Predicate("culpable", (Term("$X"),)),
        body=(
            Predicate("sin_coartada", (Term("$X"),)),
            Predicate("huellas_en", (Term("$X"), Term("$O"))),
        ),
    ))

    return kb


CASE = CrimeCase(
    id="herencia_hacienda_rosal",
    title="Herencia Hacienda Rosal",
    suspects=("esteban",),
    narrative="",
    description="Herencia.",
    create_kb=crear_kb,
    queries=(),
)

