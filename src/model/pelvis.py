__author__ = 'hsor001'

import os

from meshparser.stlparser.parser import STLParser
from opencmiss.zinc.context import Context

from utils.zinc import createMesh, createNodes, createElements, createMeshTime
from utils.zinc import createFiniteElementField


class PelvisModel(object):
    def __init__(self):
        self._context = Context("pelvis")
        glyph_module = self._context.getGlyphmodule()
        glyph_module.defineStandardGlyphs()
        material_module = self._context.getMaterialmodule()
        material_module.defineStandardMaterials()

        self._time_keeper = self._context.getTimekeepermodule().getDefaultTimekeeper()
        self._nodes_start = []
        self._nodes_end = []
        self._elements = []

        # First create coordinate field
        self._male_region = self._context.getDefaultRegion().createSubregion("male")
        self._male_coordinate_field = createFiniteElementField(self._male_region)
        self._female_region = self._context.getDefaultRegion().createSubregion("female")
        self._female_coordinate_field = createFiniteElementField(self._female_region)

    def context(self):
        return self._context

    def load(self):
        if os.getcwd() == '/':
            resources_path = os.path.join('/Applications', 'MedTech-Core Pelvis Demo.app', 'Contents', 'Resources')
        else:
            file_path = os.path.dirname(os.path.realpath(__file__))
            resources_path = os.path.join(file_path, '..', 'resources')

        self._loadFemaleMesh(resources_path)
        self._loadMaleMesh(resources_path)

    def _loadFemaleMesh(self, resources_path):
        mp = STLParser()
        mp.parse(os.path.join(resources_path, 'data', 'ship_01.zip'))
        nodes_start = mp.getPoints(pared=True)
        elements = mp.getElements(zero_based=False, pared=True)
        mp.parse(os.path.join(resources_path, 'data', 'ship_02.zip'))
        nodes_end = mp.getPoints(pared=True)
        createMeshTime(self._female_coordinate_field, nodes_start, 12, nodes_end, 64, elements)

    def _loadMaleMesh(self, resources_path):
        mp = STLParser()
        mp.parse(os.path.join(resources_path, 'data', 'pelvis_stl_01.zip'))
        nodes_start = mp.getPoints(pared=True)
        elements = mp.getElements(zero_based=False, pared=True)
        mp.parse(os.path.join(resources_path, 'data', 'pelvis_stl_02.zip'))
        nodes_end = mp.getPoints(pared=True)
        createMeshTime(self._male_coordinate_field, nodes_start, 12, nodes_end, 64, elements)

    def set_time(self, value):
        self._time_keeper.setTime(value)

    def male_coordinate_field(self):
        return self._male_coordinate_field

    def male_region(self):
        return self._male_region

    def female_coordinate_field(self):
        return self._female_coordinate_field

    def female_region(self):
        return self._female_region

