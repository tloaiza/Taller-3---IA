"""
cnf_transform.py — Transformaciones a Forma Normal Conjuntiva (CNF).
El pipeline completo to_cnf() llama a todas las transformaciones en orden.
"""

from __future__ import annotations

from src.logic_core import And, Atom, Formula, Not, Or, Implies, Iff


# --- FUNCION GUÍA SUMINISTRADA COMPLETA ---


def eliminate_double_negation(formula: Formula) -> Formula:
    """
    Elimina dobles negaciones recursivamente.

    Transformacion:
        Not(Not(a)) -> a

    Se aplica recursivamente hasta que no queden dobles negaciones.

    Ejemplo:
        >>> eliminate_double_negation(Not(Not(Atom('p'))))
        Atom('p')
        >>> eliminate_double_negation(Not(Not(Not(Atom('p')))))
        Not(Atom('p'))
    """
    if isinstance(formula, Atom):
        return formula
    if isinstance(formula, Not):
        if isinstance(formula.operand, Not):
            return eliminate_double_negation(formula.operand.operand)
        return Not(eliminate_double_negation(formula.operand))
    if isinstance(formula, And):
        return And(*(eliminate_double_negation(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        return Or(*(eliminate_double_negation(d) for d in formula.disjuncts))
    return formula


# --- FUNCIONES QUE DEBEN IMPLEMENTAR ---


def eliminate_iff(formula: Formula) -> Formula:
    """
    Elimina bicondicionales recursivamente.

    Transformacion:
        Iff(a, b) -> And(Implies(a, b), Implies(b, a))

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> eliminate_iff(Iff(Atom('p'), Atom('q')))
        And(Implies(Atom('p'), Atom('q')), Implies(Atom('q'), Atom('p')))

    Hint: Usa pattern matching sobre el tipo de la formula.
          Para cada tipo, aplica eliminate_iff recursivamente a los operandos,
          y solo transforma cuando encuentras un Iff.
    """

    # === YOUR CODE HERE ===
    """
------------------------------Mi version de la funcion-------------------------------
    if isinstance(formula, Atom):
        return formula
    if isinstance(formula, Not):
        return Not(eliminate_iff(formula.operand))
    if isinstance(formula, Iff):
        A = eliminate_iff(formula.left)
        B = eliminate_iff(formula.right)
        return And(Implies(A, B), Implies(B, A))
    if isinstance(formula, Implies):
        return Implies(eliminate_iff(formula.antecedent), eliminate_iff(formula.consequent))
    if isinstance(formula, And):
        return And(*(eliminate_iff(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        return Or(*(eliminate_iff(d) for d in formula.disjuncts))
    return formula
    
    Prompt que use para la IA
Podrias hacer esta funcion mas optima, corta y que funcion bien para los test en los que falla
------------------------------------------------------------------------------------------------
    """
    match formula:
        case Atom():
            return formula
        case Not(operand=operand):
            return Not(eliminate_iff(operand))
        case Iff(left=left, right=right):
            A, B = eliminate_iff(left), eliminate_iff(right)
            return And(Implies(A, B), Implies(B, A))
        case Implies(antecedent=antecedent, consequent=consequent):
            return Implies(eliminate_iff(antecedent), eliminate_iff(consequent))
        case And(conjuncts=conjuncts):
            return And(*(eliminate_iff(c) for c in conjuncts))
        case Or(disjuncts=disjuncts):
            return Or(*(eliminate_iff(d) for d in disjuncts))
        case _:
            return formula
    # === END YOUR CODE ===


def eliminate_implication(formula: Formula) -> Formula:
    """
    Elimina implicaciones recursivamente.

    Transformacion:
        Implies(a, b) -> Or(Not(a), b)

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> eliminate_implication(Implies(Atom('p'), Atom('q')))
        Or(Not(Atom('p')), Atom('q'))

    Hint: Similar a eliminate_iff. Recorre recursivamente y transforma
          solo los nodos Implies.
    """
    # === YOUR CODE HERE ===+
    
    """
    ---------------------------------Mi version del codigo----------------------------------------
    if isinstance(formula, Atom):
        return formula
    if isinstance(formula, Not):
        return Not(eliminate_implication(formula.operand))
    if isinstance(formula, Implies):
        # Implies usa antecedent y consequent -> ~A | B
        A = eliminate_implication(formula.antecedent)
        B = eliminate_implication(formula.consequent)
        return Or(Not(A), B)
    if isinstance(formula, And):
        return And(*(eliminate_implication(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        return Or(*(eliminate_implication(d) for d in formula.disjuncts))
    if isinstance(formula, Iff):
        return Iff(eliminate_implication(formula.left), eliminate_implication(formula.right))
    return formula
    
    Prompt que use para la IA
    Podrias hacer este codigo mas optimo y que se arreglen algunos errores que tiene con los test
    ------------------------------------------------------------------------------------------------
    """
    match formula:
        case Atom():
            return formula
        case Not(operand=operand):
            return Not(eliminate_implication(operand))
        case Implies(antecedent=antecedent, consequent=consequent):
            A = eliminate_implication(antecedent)
            B = eliminate_implication(consequent)
            return Or(Not(A), B)
        case And(conjuncts=conjuncts):
            return And(*(eliminate_implication(c) for c in conjuncts))
        case Or(disjuncts=disjuncts):
            return Or(*(eliminate_implication(d) for d in disjuncts))
        case Iff(left=left, right=right):
            return Iff(eliminate_implication(left), eliminate_implication(right))
        case _:
            return formula
    # === END YOUR CODE ===


def push_negation_inward(formula: Formula) -> Formula:
    """
    Aplica las leyes de De Morgan y mueve negaciones hacia los atomos.

    Transformaciones:
        Not(And(a, b, ...)) -> Or(Not(a), Not(b), ...)   (De Morgan)
        Not(Or(a, b, ...))  -> And(Not(a), Not(b), ...)   (De Morgan)

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> push_negation_inward(Not(And(Atom('p'), Atom('q'))))
        Or(Not(Atom('p')), Not(Atom('q')))
        >>> push_negation_inward(Not(Or(Atom('p'), Atom('q'))))
        And(Not(Atom('p')), Not(Atom('q')))

    Hint: Cuando encuentres un Not, revisa que hay adentro:
          - Si es Not(And(...)): aplica De Morgan para convertir en Or de negaciones.
          - Si es Not(Or(...)): aplica De Morgan para convertir en And de negaciones.
          - Si es Not(Atom): dejar como esta.
          Para And y Or sin negacion encima, simplemente recursa sobre los hijos.

    Nota: Esta funcion se llama DESPUES de eliminar Iff e Implies,
          asi que no necesitas manejar esos tipos.
    """
    # === YOUR CODE HERE ===
    """
   -----------------------------------------------------------------Mi version del codigo------------------------------------- 
    if isinstance(formula, Atom):
        return formula
    
    if isinstance(formula, Not):
        child = formula.operand
        if isinstance(child, Not):
            return push_negation_inward(child.operand)
        
        if isinstance(child, And):
            return Or(*(push_negation_inward(Not(c)) for c in child.conjuncts))

        if isinstance(child, Or):
            return And(*(push_negation_inward(Not(d)) for d in child.disjuncts))

        if isinstance(child, Atom):
            return formula
        
    if isinstance(formula, And):
        return And(*(push_negation_inward(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        return Or(*(push_negation_inward(d) for d in formula.disjuncts))
    if isinstance(formula, Implies):
        return Implies(push_negation_inward(formula.antecedent), push_negation_inward(formula.consequent))
    if isinstance(formula, Iff):
        return Iff(push_negation_inward(formula.left), push_negation_inward(formula.right))
    
    return formula
    prompt para la IA
    Podrias ayudarme a optimisar este codigo, que sea mas corto y que solucione algunos problemas que tiene con algunos tests.
    """
    match formula:
        case Atom():
            return formula
        case Not(operand=child):
            match child:
                case Not(operand=inner):
                    # ~~A -> A
                    return push_negation_inward(inner)
                case And(conjuncts=conjuncts):
                    # ¬(A ∧ B) -> ¬A ∨ ¬B
                    return Or(*(push_negation_inward(Not(c)) for c in conjuncts))
                case Or(disjuncts=disjuncts):
                    # ¬(A ∨ B) -> ¬A ∧ ¬B
                    return And(*(push_negation_inward(Not(d)) for d in disjuncts))
                case Atom():
                    return formula
                case _:
                    return Not(push_negation_inward(child))
        case And(conjuncts=conjuncts):
            return And(*(push_negation_inward(c) for c in conjuncts))
        case Or(disjuncts=disjuncts):
            return Or(*(push_negation_inward(d) for d in disjuncts))
        case Implies(antecedent=antecedent, consequent=consequent):
            return Implies(push_negation_inward(antecedent), push_negation_inward(consequent))
        case Iff(left=left, right=right):
            return Iff(push_negation_inward(left), push_negation_inward(right))
        case _:
            return formula
    # === END YOUR CODE ===


def distribute_or_over_and(formula: Formula) -> Formula:
    """
    Distribuye Or sobre And para obtener CNF.

    Transformacion:
        Or(A, And(B, C)) -> And(Or(A, B), Or(A, C))

    Debe aplicarse recursivamente hasta que no queden Or que contengan And.

    Ejemplo:
        >>> distribute_or_over_and(Or(Atom('p'), And(Atom('q'), Atom('r'))))
        And(Or(Atom('p'), Atom('q')), Or(Atom('p'), Atom('r')))

    Hint: Para un nodo Or, primero distribuye recursivamente en los hijos.
          Luego busca si algun hijo es un And. Si lo encuentras, aplica la
          distribucion y recursa sobre el resultado (podria haber mas).
          Para And, simplemente recursa sobre cada conjuncion.
          Atomos y Not se retornan sin cambio.

    Nota: Esta funcion se llama DESPUES de mover negaciones hacia adentro,
          asi que solo veras Atom, Not(Atom), And y Or.
    """
    # === YOUR CODE HERE ===
    raise NotImplementedError("Implementa distribute_or_over_and()")
    # === END YOUR CODE ===


def flatten(formula: Formula) -> Formula:
    """
    Aplana conjunciones y disyunciones anidadas.

    Transformaciones:
        And(And(a, b), c) -> And(a, b, c)
        Or(Or(a, b), c)   -> Or(a, b, c)

    Debe aplicarse recursivamente.

    Ejemplo:
        >>> flatten(And(And(Atom('a'), Atom('b')), Atom('c')))
        And(Atom('a'), Atom('b'), Atom('c'))
        >>> flatten(Or(Or(Atom('a'), Atom('b')), Atom('c')))
        Or(Atom('a'), Atom('b'), Atom('c'))

    Hint: Para un And, recorre cada hijo. Si un hijo tambien es And,
          agrega sus conjuncts directamente en vez de agregar el And.
          Igual para Or con sus disjuncts.
          Si al final solo queda 1 elemento, retornalo directamente.
    """
    # === YOUR CODE HERE ===
    raise NotImplementedError("Implementa flatten()")
    # === END YOUR CODE ===


# --- PIPELINE COMPLETO ---


def to_cnf(formula: Formula) -> Formula:
    """
    [DADO] Pipeline completo de conversion a CNF.

    Aplica todas las transformaciones en el orden correcto:
    1. Eliminar bicondicionales (Iff)
    2. Eliminar implicaciones (Implies)
    3. Mover negaciones hacia adentro (Not)
    4. Eliminar dobles negaciones (Not Not)
    5. Distribuir Or sobre And
    6. Aplanar conjunciones/disyunciones

    Ejemplo:
        >>> to_cnf(Implies(Atom('p'), And(Atom('q'), Atom('r'))))
        And(Or(Not(Atom('p')), Atom('q')), Or(Not(Atom('p')), Atom('r')))
    """
    formula = eliminate_iff(formula)
    formula = eliminate_implication(formula)
    formula = push_negation_inward(formula)
    formula = eliminate_double_negation(formula)
    formula = distribute_or_over_and(formula)
    formula = flatten(formula)
    return formula
