__author__ = 'hsor001'

from medtechcore.pelvisdemo.scene.pelvis import PelvisScene

class PelvisView(object):

    def __init__(self, model):
        self._model = model
        self._model.load()
        self._gender_options = []

        self._scene = PelvisScene(model)

    def register_visible_gender_options(self, gender_options):
        self._gender_options = gender_options

    def set_visible_gender(self, gender):
        if gender == self._gender_options[0]:
            self._scene.set_female_graphics_visibility(False)
            self._scene.set_male_graphics_visibility(True)
        elif gender == self._gender_options[1]:
            self._scene.set_male_graphics_visibility(False)
            self._scene.set_female_graphics_visibility(True)





