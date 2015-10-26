__author__ = 'hsor001'

import os

from meshparser.stlparser.parser import STLParser
from opencmiss.zinc.context import Context

from medtechcore.pelvisdemo.utils.zinc import createMeshTime
from medtechcore.pelvisdemo.utils.zinc import createFiniteElementField


class PelvisModel(object):
    def __init__(self):
        self._context = Context("pelvis")
        glyph_module = self._context.getGlyphmodule()
        glyph_module.defineStandardGlyphs()
        material_module = self._context.getMaterialmodule()
        material_module.defineStandardMaterials()

        self._time_keeper = self._context.getTimekeepermodule().getDefaultTimekeeper()
        self._time_keeper.setMaximumTime(324)
        self._time_keeper.setMinimumTime(236)
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
            resources_path = os.path.join(file_path, '..', '..', '..', 'resources')

        self._loadFemaleMesh(resources_path)
        self._loadMaleMesh(resources_path)

    def _loadFemaleMesh(self, resources_path):
        mp = STLParser()
        mp.parse(os.path.join(resources_path, 'data', 'pelvis_female_238mm.stl'))
        nodes_start = mp.getPoints(pared=True)
        elements = mp.getElements(zero_based=False, pared=True)
        mp.parse(os.path.join(resources_path, 'data', 'pelvis_female_322mm.stl'))
        nodes_end = mp.getPoints(pared=True)
        createMeshTime(self._female_coordinate_field, nodes_start, 238, nodes_end, 322, elements)

    def _loadMaleMesh(self, resources_path):
        mp = STLParser()
        mp.parse(os.path.join(resources_path, 'data', 'pelvis_male_236mm.stl'))
        nodes_start = mp.getPoints(pared=True)
        elements = mp.getElements(zero_based=False, pared=True)
        mp.parse(os.path.join(resources_path, 'data', 'pelvis_male_324mm.stl'))
        nodes_end = mp.getPoints(pared=True)
        createMeshTime(self._male_coordinate_field, nodes_start, 236, nodes_end, 324, elements)

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

