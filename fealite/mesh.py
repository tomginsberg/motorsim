import numpy as np
from typing import Tuple, List, Union, Iterable, Dict


class TriangleMesh:
    def __init__(self, file_name):
        # coordinate lookup for vertex i
        self.coordinates: List[Tuple[float, float]] = []

        # list of triangle elements with material markers
        self.mesh_elements: List[Tuple[Tuple[int, int, int], int]] = []

        # list of line elements with boundary markers
        self.boundary_elements: List[Tuple[Tuple[int, int], int]] = []

        # faces[v_i] = [(v_j, v_k) | {(v_j,v_i), (v_k,v_i), (v_j,v_k)} is a subset of E]
        # where E is the edge set of the mesh
        self.faces: List[List[Tuple[int, int]]] = []

        # material_markers[v_i] = material marker if v_i
        self.material_markers: Dict[int, int] = {}

        # boundary_markers[v_i] = material marker if v_i
        # not sure what this will do yet, but seems good to have
        self.boundary_markers: Dict[int, int] = {}

        # default: material[0] = permittivity of free space
        self.material_constants: List[float] = [8.854e-12]

        if file_name is not None:
            self.parse_file(file_name)

    def parse_file(self, file_name: str):
        with open(file_name, 'r') as f:
            lines = f.readlines()
        section = None
        for line in lines:
            if '#' in line:
                section = line[1:].strip()
            if section == 'Coordinates':
                self.coordinates.append(*[float(x) for x in line.split('\t')])
            if section == 'Triangle Elements':
                self.add_mesh_element(*[int(x) for x in line.split('\t')])
            if section == 'Boundary Elements':
                self.add_boundary_element(*[int(x) for x in line.split('\t')])

    def add_coordinate(self, x: float, y: float):
        self.coordinates.append((x, y))

    def add_mesh_element(self, v1: int, v2: int, v3: int, material_marker: int):
        self.mesh_elements.append(((v1, v2, v3), material_marker))

    def add_boundary_element(self, v1: int, v2: int, boundary_marker: int):
        self.boundary_elements.append(((v1, v2), boundary_marker))

    def add_face(self, v1: int, v2: int, v3: int):
        self.faces[v1].append((v2, v3))
        self.faces[v2].append((v1, v3))
        self.faces[v3].append((v1, v2))

    def set_material_constants(self, mapping: List[float]):
        self.material_constants = mapping

    # Not currently supported from mesh generated by file
    def face(self, n: int) -> List[Tuple[int, int]]:
        # Returns face of vertex n
        return self.faces[n]

    def coordinate(self, n: int) -> Tuple[float, float]:
        # Returns coordinate of vertex n
        return self.coordinates[n]

    def material(self, n: int) -> float:
        # Returns coordinate of vertex n
        return self.material_constants[self.material_markers[n]]
