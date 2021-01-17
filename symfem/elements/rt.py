"""Raviart-Thomas elements on simplices."""

from ..core.finite_element import FiniteElement
from ..core.moments import make_integral_moment_dofs
from ..core.polynomials import polynomial_set, Hdiv_polynomials
from ..core.functionals import NormalIntegralMoment, IntegralMoment
from .lagrange import DiscontinuousLagrange, VectorDiscontinuousLagrange


class RaviartThomas(FiniteElement):
    """Raviart-Thomas Hdiv finite element."""

    def __init__(self, reference, order):
        poly = polynomial_set(reference.tdim, reference.tdim, order - 1)
        poly += Hdiv_polynomials(reference.tdim, reference.tdim, order)

        dofs = make_integral_moment_dofs(
            reference,
            facets=(NormalIntegralMoment, DiscontinuousLagrange, order - 1),
            cells=(IntegralMoment, VectorDiscontinuousLagrange, order - 2),
        )

        super().__init__(reference, order, poly, dofs, reference.tdim, reference.tdim)

    names = ["Raviart-Thomas", "RT", "N1div"]
    references = ["triangle", "tetrahedron"]
    min_order = 1
    mapping = "contravariant"
    continuity = "H(div)"
