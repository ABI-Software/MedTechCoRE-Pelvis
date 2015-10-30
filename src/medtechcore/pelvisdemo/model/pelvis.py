__author__ = 'hsor001'

import os
import threading
import subprocess
import Queue
from math import pi

from PySide import QtCore

from meshparser.stlparser.parser import STLParser
from opencmiss.zinc.context import Context

from medtechcore.pelvisdemo.utils.zinc import createMeshTime
from medtechcore.pelvisdemo.utils.zinc import createFiniteElementField
from medtechcore.pelvisdemo.utils.mathext import quaternionToMatrix, quaternionToAxisAngle, quaternionMultiply


class PelvisModel(QtCore.QObject):

    imuInputReceived = QtCore.Signal(object, object)
    resetInitialParameters = QtCore.Signal()

    def __init__(self):
        super(PelvisModel, self).__init__()
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


        self._command = ['node', os.environ['IMU_BLE']]
        self._process = None
        self._stdout_reader = None
        self._timer = QtCore.QTimer()
        self._timer.setInterval(10)
        self._timer.timeout.connect(self._readData)
        self._timer_active = False

        # First create coordinate field
        self._male_region = self._context.getDefaultRegion().createSubregion("male")
        self._setupMaleRegion(self._male_region)
        self._female_region = self._context.getDefaultRegion().createSubregion("female")
        self._setupFemaleRegion(self._female_region)

    def _setupMaleRegion(self, region):
        fieldmodule = self._male_region.getFieldmodule()
        self._male_coordinate_field = createFiniteElementField(self._male_region)
        self._male_matrix_field = fieldmodule.createFieldConstant([1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0])
        self._male_graphics_coordinate_field = fieldmodule.createFieldMatrixMultiply(3, self._male_matrix_field, self._male_coordinate_field)

    def _setupFemaleRegion(self, region):
        fieldmodule = self._female_region.getFieldmodule()
        self._female_coordinate_field = createFiniteElementField(self._female_region)
        self._female_matrix_field = fieldmodule.createFieldConstant([1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0])
        self._female_graphics_coordinate_field = fieldmodule.createFieldMatrixMultiply(3, self._female_matrix_field, self._female_coordinate_field)

    def context(self):
        return self._context

    def listen(self, state=True):
        if state:
            self._activateListener()
        else:
            self._deactivateListener()

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

    def _activateListener(self):
        # Launch the command as subprocess.
        self._process = subprocess.Popen(self._command, stdout=subprocess.PIPE)

        # Launch the asynchronous readers of the process' stdout and stderr.
        self._stdout_queue = Queue.LifoQueue()
        self._stdout_reader = AsynchronousFileReader(self._process.stdout, self._stdout_queue)
        self._stdout_reader.start()
        self._timer.start()
        self._timer_active = True
        self.resetInitialParameters.emit()

    def _deactivateListener(self):
        self._timer_active = False
        self._timer.stop()
        self._stdout_reader.stop()
        # Let's be tidy and join the threads we've started.
        self._stdout_reader.join()
        # Close subprocess' file descriptors.
        self._process.stdout.close()

    def _extractQuaternion(self, line):
        q = []
        parts = line.split(' ')
        if len(parts) == 13:
            quaternion = parts[9:]
            q = [float(q_) for q_ in quaternion]

        return q

    def _readData(self):
        if self._timer_active:
            quaternion = self._extractQuaternion(self._stdout_queue.get())
            while not quaternion:
                if self._stdout_queue.empty():
                    return
                quaternion = self._extractQuaternion(self._stdout_queue.get())

            imu_orientation = [1.0, 0.0, 0.0, pi/2.0]
            axis, angle = quaternionToAxisAngle(quaternion)
            self.imuInputReceived.emit(axis, -angle)
            # matrix = quaternionToMatrix(quaternion)
            # self._updateGraphicsMatrix(matrix)

            # we've dealt with as much as we can remove anything else
            while not self._stdout_queue.empty():
                self._stdout_queue.get_nowait()

    def _updateGraphicsMatrix(self, matrix):
        fieldmodule = self._male_graphics_coordinate_field.getFieldmodule()
        fieldmodule.beginChange()
        fieldcache = fieldmodule.createFieldcache()
        self._male_matrix_field.assignReal(fieldcache, matrix)
        fieldmodule.endChange()

        fieldmodule = self._female_graphics_coordinate_field.getFieldmodule()
        fieldmodule.beginChange()
        fieldcache = fieldmodule.createFieldcache()
        self._female_matrix_field.assignReal(fieldcache, matrix)
        fieldmodule.endChange()

    def set_time(self, value):
        self._time_keeper.setTime(value)

    def male_coordinate_field(self):
        return self._male_coordinate_field

    def male_graphics_coordinate_field(self):
        return self._male_graphics_coordinate_field

    def male_region(self):
        return self._male_region

    def female_coordinate_field(self):
        return self._female_coordinate_field

    def female_region(self):
        return self._female_region


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class AsynchronousFileReader(StoppableThread):
    '''
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''

    def __init__(self, fd, queue):
        assert isinstance(queue, Queue.Queue)
        assert callable(fd.readline)
        super(AsynchronousFileReader, self).__init__()
        self._fd = fd
        self._queue = queue

    def run(self):
        '''The body of the thread: read lines and put them on the queue.'''
        while not self.stopped():
            line = self._fd.readline()
            if line != '':
                self._queue.put(line.strip())



