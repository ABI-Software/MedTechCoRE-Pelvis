__author__ = 'hsor001'

from medtechcore.pelvisdemo.utils.zinc import createSurfaceGraphics

class PelvisScene(object):

    def __init__(self, model):
        self._model = model

        self._setupVisualisation()

    def _setupVisualisation(self):
        self._setupMaleVisualisation()
        self._setupFemaleVisualisation()

    def _setupMaleVisualisation(self):
        coordinate_field = self._model.male_coordinate_field()
        region = self._model.male_region()
        scene = region.getScene()
        materialmodule = scene.getMaterialmodule()
#         blue = materialmodule.findMaterialByName('blue')
        bone_material = materialmodule.findMaterialByName('bone')
#         self._selection_graphics = self._createPointGraphics(scene, coordinate_field, bone_material, None) # self._model.getSelectionGroupField())
#         self._node_graphics = self._createPointGraphics(scene, coordinate_field, red, None) # self._model.getNodeGroupField())
        self._male_mesh_surface_graphics = createSurfaceGraphics(scene, coordinate_field, bone_material)

    def _setupFemaleVisualisation(self):
        coordinate_field = self._model.female_coordinate_field()
        region = self._model.female_region()
        scene = region.getScene()
        materialmodule = scene.getMaterialmodule()
#         blue = materialmodule.findMaterialByName('blue')
        bone_material = materialmodule.findMaterialByName('bone')
#         self._selection_graphics = self._createPointGraphics(scene, coordinate_field, bone_material, None) # self._model.getSelectionGroupField())
#         self._node_graphics = self._createPointGraphics(scene, coordinate_field, red, None) # self._model.getNodeGroupField())
        self._female_mesh_surface_graphics = createSurfaceGraphics(scene, coordinate_field, bone_material)

    def set_female_graphics_visibility(self, flag):
        self._female_mesh_surface_graphics.setVisibilityFlag(flag)

    def set_male_graphics_visibility(self, flag):
        self._male_mesh_surface_graphics.setVisibilityFlag(flag)
