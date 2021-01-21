"""Hermite elements on simplices."""

from ..core.finite_element import FiniteElement
from ..core.polynomials import polynomial_set
from ..core.functionals import PointEvaluation, PointDirectionalDerivativeEvaluation
from ..core.symbolic import sym_sum


class Hermite(FiniteElement):
    """Hermite finite element."""

    def __init__(self, reference, order):
        assert order == 3
        dofs = []
        for v_n, vs in enumerate(reference.sub_entities(0)):
            dofs.append(PointEvaluation(vs, entity=(0, v_n)))
            for i in range(reference.tdim):
                dir = tuple(1 if i == j else 0 for j in range(reference.tdim))
                dofs.append(PointDirectionalDerivativeEvaluation(vs, dir, entity=(0, v_n)))
        for e_n, vs in enumerate(reference.sub_entities(2)):
            midpoint = tuple(sym_sum(i) / len(i)
                             for i in zip(*[reference.vertices[i] for i in vs]))
            dofs.append(PointEvaluation(midpoint, entity=(2, e_n)))

        super().__init__(
            reference, order, polynomial_set(reference.tdim, 1, order), dofs, reference.tdim, 1
        )

    names = ["Hermite"]
    references = ["interval", "triangle", "tetrahedron"]
    min_order = 3
    max_order = 3
    mapping = "identity"
    continuity = "L2"