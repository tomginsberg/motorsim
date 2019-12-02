from typing import Union, Optional
import numpy as np
from mesh import TriangleMesh, Meshes
from poisson import NonLinearPoissonProblemDefinition, NonLinearPoisson
#import ..\bldc need to figure out how to do relative import

import sys
sys.path.append("..\\")
import bldc as bldc

from math import e


class SampleProblem(NonLinearPoissonProblemDefinition):
    def __init__(self, mesh: Union[str, TriangleMesh] = Meshes.unit_disk, name: str = 'laplace'):
        super().__init__(mesh, name)

    def non_linear_material(self, element_marker: int, coordinate: np.ndarray, norm_grad_phi: Optional[float] = None,
                            div: bool = False) -> Optional[float]:
        if element_marker == 1:
            return bldc.one_over_mu(norm_grad_phi, False)
        return 1

    def source(self, element_marker: int, coordinate: np.ndarray) -> Optional[float]:
        return 0

    def dirichlet_boundary(self, boundary_marker: int, coordinate: np.ndarray) -> Optional[float]:
        return coordinate[0] * coordinate[1]

    def neumann_boundary(self, boundary_marker: int, coordinate: np.ndarray) -> Optional[float]:
        return None

class TestProblem(NonLinearPoissonProblemDefinition):
    def __init__(self, mesh: Union[str, TriangleMesh] = Meshes.unit_disk, name: str = 'laplace'):
        super().__init__(mesh, name)

    def non_linear_material(self, element_marker: int, coordinate: np.ndarray, norm_grad_phi: Optional[float] = None,
                            div: bool = False) -> Optional[float]:
        return e ** norm_grad_phi

    def source(self, element_marker: int, coordinate: np.ndarray) -> Optional[float]:
        return 0

    def dirichlet_boundary(self, boundary_marker: int, coordinate: np.ndarray) -> Optional[float]:
        return 0

    def neumann_boundary(self, boundary_marker: int, coordinate: np.ndarray) -> Optional[float]:
        return None

if __name__ == '__main__':
    problem = NonLinearPoisson(TestProblem(Meshes.annulus))
    problem.export_solution()