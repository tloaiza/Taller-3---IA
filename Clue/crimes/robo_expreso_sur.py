"""
robo_expreso_sur.py — El Robo en el Expreso del Sur

El collar de esmeraldas de la Marquesa desapareció del vagón privado del tren nocturno.
Elena fue vista en el vagón privado durante el robo; sus huellas están en el estuche de joyas.
Don Rodrigo fue grabado por la cámara de seguridad en el vagón de equipaje durante toda la noche.
El vagón de equipaje es el extremo opuesto al vagón privado; es imposible haber estado en ambos a la vez.
La Marquesa es la víctima directa del robo y presenció el incidente.
La Marquesa acusa a Elena.
Victor declara que Elena estuvo con él en el vagón comedor toda la noche.
Elena declara que Victor estuvo con ella en el vagón comedor toda la noche.

Como detective, he llegado a las siguientes conclusiones:
Quien fue grabado en cámara en un lugar alejado de la escena durante el crimen está descartado.
La víctima del crimen no tiene razón para mentir; es testigo imparcial.
La acusación de un testigo imparcial es creíble.
Quien estaba en la escena y es acusado de forma creíble es culpable.
Quien da coartada a un culpable lo está defendiendo.
Si dos personas se dan coartada mutuamente, tienen una alianza de coartadas entre sí.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    kb = KnowledgeBase()

    elena = Term("elena")
    don_rodrigo = Term("don_rodrigo")
    marquesa = Term("marquesa")

    kb.add_fact(Predicate("en_escena", (elena,)))
    kb.add_fact(Predicate("grabado_lejos_escena", (don_rodrigo, Term("vagon"))))
    kb.add_fact(Predicate("victima", (marquesa,)))
    kb.add_fact(Predicate("acusa", (marquesa, elena)))

    kb.add_rule(Rule(
        head=Predicate("descartado", (Term("$X"),)),
        body=(Predicate("grabado_lejos_escena", (Term("$X"), Term("$L"))),),
    ))

    kb.add_rule(Rule(
        head=Predicate("culpable", (Term("$X"),)),
        body=(
            Predicate("en_escena", (Term("$X"),)),
            Predicate("acusa", (Term("$A"), Term("$X"))),
        ),
    ))

    return kb


CASE = CrimeCase(
    id="robo_expreso_sur",
    title="Robo Expreso Sur",
    suspects=("elena", "don_rodrigo"),
    narrative="",
    description="Robo en tren.",
    create_kb=crear_kb,
    queries=(),
)