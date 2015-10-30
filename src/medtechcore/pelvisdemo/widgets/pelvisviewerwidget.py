from math import sqrt, cos, sin, fabs

from opencmiss.zincwidgets.sceneviewerwidget import SceneviewerWidget

import time

time_0 = time.time()

initial_view = [[49.79080069116709, 588.9318153465964, -363.0583058231066],
                [2.285999298095703, -71.78712940216064, -44.651397705078125],
                [0.022226151722452247, -0.43531795844346366, -0.9000023740170076]]


class PelvisViewerWidget(SceneviewerWidget):

    def __init__(self, parent):
        super(PelvisViewerWidget, self).__init__(parent)
        self._initial_eye = None
        self._initial_up = None
        self._up_prev = None

        self.graphicsInitialized.connect(self.setInitialView)

    def resetView(self, gender):
        sv = self.getSceneviewer()
        # print(sv.getLookatParameters())
        sv.setLookatParametersNonSkew(initial_view[0], initial_view[1], initial_view[2])
            # if self._visibleGender == self._ui.radioButtonMale.text():
            #     self._ui.widgetScene.setLookatParameters(male_initial_view)
            # else:
            #     self._ui.widgetScene.setLookatParameters(female_initial_view)

    def setInitialView(self):
        sv = self.getSceneviewer()
        self._up_prev = initial_view[2][:]
        sv.setLookatParametersNonSkew(initial_view[0], initial_view[1], initial_view[2])

    def resetInitial(self):
        sv = self.getSceneviewer()
        print(sv.getLookatParameters())
        _, self._initial_eye = sv.getEyePosition()
        # _, la = sv.getLookatPosition()
        _, self._initial_up = sv.getUpVector()

    def updateFromIMU(self, axis, angle):
        # print('axis = ', axis)
        # print('angle = ', angle)
        # print('time = {0}: angle = {1}, axis = {2}'.format(time.time() - time_0, angle, axis))

        sv = self.getSceneviewer()

        sv.beginChange()
        # _, eye = sv.getEyePosition()
        _, la = sv.getLookatPosition()
        # _, up = sv.getUpVector()
        eye = self._initial_eye[:]
        up = self._initial_up[:]

        # double a[3] = { axis[0], axis[1], axis[2] };
        a = axis[:]

        # /* get coordinate system moving with rotation, consisting of the axis a */
        # /* and two othogonal vectors b and c in the plane normal to a. */
        # /* v = vector towards viewer */
        # v[0]=rel_eyex=scene_viewer->eyex-scene_viewer->lookatx;
        # v[1]=rel_eyey=scene_viewer->eyey-scene_viewer->lookaty;
        # v[2]=rel_eyez=scene_viewer->eyez-scene_viewer->lookatz;
        v = [1.0, 0.0, 0.0]
        v[0] = eye[0] - la[0]
        v[1] = eye[1] - la[1]
        v[2] = eye[2] - la[2]

        view_vec = v[:]

        # /* check v is not too closely in line with a */
        # if (0.8 < fabs(v[0]*a[0]+v[1]*a[1]+v[2]*a[2]))
        # {
        # 	/* use up-vector instead */
        # 	v[0]=scene_viewer->upx;
        # 	v[1]=scene_viewer->upy;
        # 	v[2]=scene_viewer->upz;
        # }
        if 0.8 < fabs(v[0] * a[0] + v[1] * a[1] + v[2] * a[2]):
            v = up[:]

        # normalize3(v);
        v_mag = sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
        v[0] /= v_mag
        v[1] /= v_mag
        v[2] /= v_mag

        # /* b = axis (x) a, a vector in plane of rotation */
        # b[0]=a[1]*v[2]-a[2]*v[1];
        # b[1]=a[2]*v[0]-a[0]*v[2];
        # b[2]=a[0]*v[1]-a[1]*v[0];
        b = [1.0, 0.0, 0.0]
        b[0] = a[1] * v[2] - a[2] * v[1]
        b[1] = a[2] * v[0] - a[0] * v[2]
        b[2] = a[0] * v[1] - a[1] * v[0]

        # normalize3(b);
        b_mag = sqrt(b[0] * b[0] + b[1] * b[1] + b[2] * b[2])
        b[0] /= b_mag
        b[1] /= b_mag
        b[2] /= b_mag

        # /* c = b (x) axis, another unit vector in plane of rotation */
        # c[0]=a[1]*b[2]-a[2]*b[1];
        # c[1]=a[2]*b[0]-a[0]*b[2];
        # c[2]=a[0]*b[1]-a[1]*b[0];
        c = [1.0, 0.0, 0.0]
        c[0] = a[1] * b[2] - a[2] * b[1]
        c[1] = a[2] * b[0] - a[0] * b[2]
        c[2] = a[0] * b[1] - a[1] * b[0]

        # /* define eye position and up vector relative to a, b and c */
        # rel_eyea=a[0]*rel_eyex+a[1]*rel_eyey+a[2]*rel_eyez;
        # rel_eyeb=b[0]*rel_eyex+b[1]*rel_eyey+b[2]*rel_eyez;
        # rel_eyec=c[0]*rel_eyex+c[1]*rel_eyey+c[2]*rel_eyez;
        view_vec_new = [1.0, 0.0, 0.0]
        view_vec_new[0] = a[0] * view_vec[0] + a[1] * view_vec[1] + a[2] * view_vec[2]
        view_vec_new[1] = b[0] * view_vec[0] + b[1] * view_vec[1] + b[2] * view_vec[2]
        view_vec_new[2] = c[0] * view_vec[0] + c[1] * view_vec[1] + c[2] * view_vec[2]

        # upa=a[0]*scene_viewer->upx+a[1]*scene_viewer->upy+a[2]*scene_viewer->upz;
        # upb=b[0]*scene_viewer->upx+b[1]*scene_viewer->upy+b[2]*scene_viewer->upz;
        # upc=c[0]*scene_viewer->upx+c[1]*scene_viewer->upy+c[2]*scene_viewer->upz;
        # /* get new b and c from clockwise rotation by <angle> radians about a */
        up_prime = [1.0, 0.0, 0.0]
        up_prime[0] = a[0] * up[0] + a[1] * up[1] + a[2] * up[2]
        up_prime[1] = b[0] * up[0] + b[1] * up[1] + b[2] * up[2]
        up_prime[2] = c[0] * up[0] + c[1] * up[1] + c[2] * up[2]

        # cos_angle=cos(angle);
        # sin_angle=sin(angle);
        cos_angle = cos(angle)
        sin_angle = sin(angle)

        # new_b[0]=cos_angle*b[0]+sin_angle*c[0];
        # new_b[1]=cos_angle*b[1]+sin_angle*c[1];
        # new_b[2]=cos_angle*b[2]+sin_angle*c[2];
        b_new = [1.0, 0.0, 0.0]
        b_new[0] = cos_angle * b[0] + sin_angle * c[0]
        b_new[1] = cos_angle * b[1] + sin_angle * c[1]
        b_new[2] = cos_angle * b[2] + sin_angle * c[2]

        # new_c[0]=cos_angle*c[0]-sin_angle*b[0];
        # new_c[1]=cos_angle*c[1]-sin_angle*b[1];
        # new_c[2]=cos_angle*c[2]-sin_angle*b[2];
        c_new = [1.0, 0.0, 0.0]
        c_new[0] = cos_angle * c[0] - sin_angle * b[0]
        c_new[1] = cos_angle * c[1] - sin_angle * b[1]
        c_new[2] = cos_angle * c[2] - sin_angle * b[2]

        # /* get eye position and up vector back in world coordinates */
        # scene_viewer->eyex=scene_viewer->lookatx+
        # 	a[0]*rel_eyea+new_b[0]*rel_eyeb+new_c[0]*rel_eyec;
        # scene_viewer->eyey=scene_viewer->lookaty+
        # 	a[1]*rel_eyea+new_b[1]*rel_eyeb+new_c[1]*rel_eyec;
        # scene_viewer->eyez=scene_viewer->lookatz+
        # 	a[2]*rel_eyea+new_b[2]*rel_eyeb+new_c[2]*rel_eyec;
        eye_new = [1.0, 0.0, 0.0]
        eye_new[0] = la[0] + a[0] * view_vec_new[0] + b_new[0] * view_vec_new[1] + c_new[0] * view_vec_new[2]
        eye_new[1] = la[1] + a[1] * view_vec_new[0] + b_new[1] * view_vec_new[1] + c_new[1] * view_vec_new[2]
        eye_new[2] = la[2] + a[2] * view_vec_new[0] + b_new[2] * view_vec_new[1] + c_new[2] * view_vec_new[2]

        # scene_viewer->upx=a[0]*upa+new_b[0]*upb+new_c[0]*upc;
        # scene_viewer->upy=a[1]*upa+new_b[1]*upb+new_c[1]*upc;
        # scene_viewer->upz=a[2]*upa+new_b[2]*upb+new_c[2]*upc;
        up_new = [1.0, 0.0, 0.0]
        up_new[0] = a[0] * up_prime[0] + b_new[0] * up_prime[1] + c_new[0] * up_prime[2]
        up_new[1] = a[1] * up_prime[0] + b_new[1] * up_prime[1] + c_new[1] * up_prime[2]
        up_new[2] = a[2] * up_prime[0] + b_new[2] * up_prime[1] + c_new[2] * up_prime[2]

        sv.setEyePosition(eye_new)
        sv.setUpVector(up_new)

        sv.endChange()
