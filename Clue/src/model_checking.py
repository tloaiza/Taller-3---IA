"""
model_checking.py

Este modulo contiene las funciones de model checking proposicional.

Hint: Usa las funciones get_atoms() y evaluate() de logic_core.py.
"""

from __future__ import annotations

from src.logic_core import Formula
from src.logic_core import get_atoms, evaluate




"""
    GET_ALL_MODELS_INSTRUCTIONS

    Genera todos los modelos posibles (asignaciones de verdad).
    Para n atomos, genera 2^n modelos.

    Args:
        atoms: Conjunto de nombres de atomos proposicionales.

    Returns:
        Lista de diccionarios, cada uno mapeando atomos a valores booleanos.

    Ejemplo:
        >>> get_all_models({'p', 'q'})
        [{'p': True, 'q': True}, {'p': True, 'q': False},
         {'p': False, 'q': True}, {'p': False, 'q': False}]

    Hint: Piensa en como representar los numeros del 0 al 2^n - 1 en binario.
          Cada bit corresponde al valor de verdad de un atomo.
    """

#--------------------------- mi versión del código get_all_models-------------------------------
# def get_all_models(atoms: set[str]) -> list[dict[str, bool]]:
#     atoms_list = list(atoms)
#     n = len(atoms_list)
#
#     model = []
#
#     for i in range(n):
#         for j in range(2 ** n):
#              value = (i >> j) & 1  
#              model[atoms_list[j]] = bool(value)
#
#     return model
#-----------------------------------------------------------------------------------------------
   

"""
Prompt Utilizado con Chat GPT:
Porfavor colabórame a corregir el siguiente codigo mostrándome los errores que puede haber
y además me indicas cual es la correción que realizaste en forma de comentarios. También 
porfavor optimizala en dado caso que se pueda. 
"""

#---------------------------VERSION OPTIMIZADA Y MEJORADA POR CHAT GPT-------------------------------
def get_all_models(atoms: set[str]) -> list[dict[str, bool]]:
    atoms_list = list(atoms)
    n = len(atoms_list)

    models = []  
    # Corrección: antes era "model = []"
    # Se usaba una sola lista llamada model y además se trataba luego como diccionario
    # Esto provocaba error de tipo porque una lista no se puede indexar con strings

    for i in range(2 ** n):  
        # Corrección: antes era range(n)
        # Eso solo generaba n iteraciones
        # Pero se necesitan 2^n combinaciones posibles de valores de verdad

        model = {}  
        # Corrección: antes no se creaba un diccionario por cada modelo
        # Entonces no existía estructura donde mapear átomo → valor
        # Además se intentaba escribir sobre una lista usando claves string

        for j in range(n):  
            # Corrección: antes era range(2 ** n)
            # Eso hacía que j excediera la cantidad de átomos
            # Provocando IndexError en atoms_list[j]

            value = (i >> j) & 1  
            # Corrección: antes los índices estaban invertidos (i y j mal usados)
            # Se terminaban generando valores incorrectos para cada átomo
            # Ahora cada bit de i representa un átomo distinto

            model[atoms_list[j]] = bool(value)

        models.append(model)  
        # Corrección: antes nunca se agregaba cada modelo a la lista
        # Como resultado solo se construía uno o ninguno

    return models  
    # Corrección: antes retornaba "model"
    # Eso devolvía una estructura incorrecta y no todos los modelos
#-----------------------------------------------------------------------------------------------



"""
    CHECK_SATISFIABLE INSTRUCTIONS

    Determina si una formula es satisfacible.

    Args:
        formula: Formula logica a verificar.

    Returns:
        (True, modelo) si encuentra un modelo que la satisface.
        (False, None) si es insatisfacible.

    Ejemplo:
        >>> check_satisfiable(And(Atom('p'), Not(Atom('p'))))
        (False, None)

    Hint: Genera todos los modelos con get_all_models(), luego evalua
          la formula en cada uno usando evaluate().
    """
    
#--------------------------- mi versión del código check_satisfiable-------------------------------
def check_satisfiable(formula: Formula) -> tuple[bool, dict[str, bool] | None]:
    
    atoms = get_atoms(formula)  
    models = get_all_models(atoms)  
    
    for model in models:
        if evaluate(formula, model):  
            return True, model

    return False, None  

# NOTA: para este bloque de código, no se utilizó ninguna IA para correcciones ni mejoras
#-----------------------------------------------------------------------------------------------  




"""
    CHECK_VALID INSTRUCTIONS
    Determina si una formula es una tautologia (valida en todo modelo).

    Args:
        formula: Formula logica a verificar.

    Returns:
        True si la formula es verdadera en todos los modelos posibles.

    Ejemplo:
        >>> check_valid(Or(Atom('p'), Not(Atom('p'))))
        True

    Hint: Una formula es valida si y solo si su negacion es insatisfacible.
          Alternativamente, verifica que sea verdadera en TODOS los modelos.
    """

#---------------------------mi versión del código check_valid-------------------------------
def check_valid(formula: Formula) -> bool:
    
    atoms = get_atoms(formula)
    models = get_all_models(atoms)
    

    for model in models:
        if not evaluate(formula, model):
            return False

    return True

# NOTA: para este bloque de código, no se utilizó ninguna IA para correcciones ni mejoras
#-----------------------------------------------------------------------------------------------  





"""
    CHECK_ENTAILMENT INSTRUCTIONS
    Determina si KB |= query (la base de conocimiento implica la consulta).

    Args:
        kb: Lista de formulas que forman la base de conocimiento.
        query: Formula que queremos verificar si se sigue de la KB.

    Returns:
        True si la query es verdadera en todos los modelos donde la KB es verdadera.

    Ejemplo:
        >>> kb = [Implies(Atom('p'), Atom('q')), Atom('p')]
        >>> check_entailment(kb, Atom('q'))
        True

    Hint: KB |= q  si y solo si  KB ^ ~q es insatisfacible.
          Es decir, no existe un modelo donde toda la KB sea verdadera
          y la query sea falsa.
    """

#-----------------------------mi version del código check_entailment---------------------------
# def check_entailment(kb: list[Formula], query: Formula) -> bool:
#     atoms = set()
#
#     for formula in kb:
#         atoms = get_atoms(formula)
#
#     atoms = get_atoms(query)
#
#     for model in get_all_models(atoms):
#         if evaluate(query, model):
#             return True
#
#     return False
#-----------------------------------------------------------------------------------------------  

"""
Prompt Utilizado con Chat GPT:
Porfavor colabórame a corregir el siguiente codigo mostrándome los errores que puede haber
y además me indicas cual es la correción que realizaste en forma de comentarios. También 
porfavor optimizala en dado caso que se pueda. 
"""

#---------------------------VERSION OPTIMIZADA Y MEJORADA POR CHAT GPT-------------------------------
def check_entailment(kb: list[Formula], query: Formula) -> bool:
    atoms = set()

    for formula in kb:
        atoms |= get_atoms(formula)
    # Corrección: antes era "atoms = get_atoms(formula)"
    # Eso sobrescribía los átomos en cada iteración
    # Ahora se acumulan todos los átomos de la KB

    atoms |= get_atoms(query)
    # Corrección: antes era "atoms = get_atoms(query)"
    # Eso borraba los átomos de la KB
    # Ahora se agregan también los de la query

    for model in get_all_models(atoms):

        if all(evaluate(formula, model) for formula in kb):
        # Corrección: antes no se evaluaba la KB completa
        # Ahora se verifica que TODAS las fórmulas de la KB sean verdaderas

            if not evaluate(query, model):
                return False
            # Corrección: antes se retornaba True si query era verdadera
            # Eso no verifica entailment
            # Ahora si KB es verdadera y query es falsa → no hay entailment

    return True
    # Corrección: antes se retornaba False por defecto
    # Ahora si no existe contraejemplo entonces KB |= query
#-----------------------------------------------------------------------------------------------
    
    
    
    


def truth_table(formula: Formula) -> list[tuple[dict[str, bool], bool]]:
    """
    Genera la tabla de verdad completa de una formula.

    Args:
        formula: Formula logica.

    Returns:
        Lista de tuplas (modelo, resultado) para cada modelo posible.

    Ejemplo:
        >>> truth_table(And(Atom('p'), Atom('q')))
        [({'p': True, 'q': True}, True),
         ({'p': True, 'q': False}, False),
         ({'p': False, 'q': True}, False),
         ({'p': False, 'q': False}, False)]

    Hint: Combina get_all_models() y evaluate().
    """
    # === YOUR CODE HERE ===
    raise NotImplementedError("Implementa truth_table()")
    # === END YOUR CODE ===
