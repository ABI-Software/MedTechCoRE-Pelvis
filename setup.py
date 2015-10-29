import platform, sys, os
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop

name = u'MedTech-CoRE Pelvis Demo'
version = '0.2.0'

dependencies = ['meshparser==0.3.2']

long_description = """A demonstration of how the pelvis changes for the population.  Specifically looking at the
difference in characteristics between the male and female pelvis and the impact the width of the hip has.
"""

try:
    import PySide
    pyside_version = PySide.__version__
    pyside_requirement = 'PySide==' + pyside_version
    # PySide version 1.1.0 is not known about by PyPi
    # but it will work for the MAP Client software
    if pyside_version == '1.1.0':
        pyside_requirement = None
    else:
        try:
            import site
            site_packages = site.getsitepackages()
            if len(site_packages) > 1:
                site_package_dir = site_packages[1]
                egg_info_file = os.path.join(site_package_dir, 'PySide-' + pyside_version + '.egg-info')
                if not os.path.exists(egg_info_file):
                    with open(egg_info_file, 'a'):
                        pass
        except ImportError:
            pass # Ah well an old version of Python perhaps
except ImportError:
    # If we don't have PySide we will need to build it
    pyside_requirement = 'PySide'

if pyside_requirement is not None:
    dependencies.append(pyside_requirement)

def createApplication(install_dir):
    from subprocess import call
    call([sys.executable, 'shimbundle.py', name, version],
          cwd=os.path.join(install_dir, 'resources', 'osxapp'))


# For OS X we want to install MAP Client into the Applications directory
class install(_install):

    def run(self):
        _install.run(self)
        mac_release, _, _ = platform.mac_ver()
        if mac_release:
            self.execute(createApplication, (self.install_lib,),
                         msg="Creating OS X Application")


# For OS X we want to install MAP Client into the Applications directory
class develop(_develop):

    def run(self):
        _develop.run(self)
        mac_release, _, _ = platform.mac_ver()
        if mac_release:
            self.execute(createApplication, ('src',),
                         msg="Creating OS X Application")

setup(name=name,
      version=version,
      description='A simple demonstration that visualises demographic characteristics of the pelvis.',
      long_description=long_description,
      classifiers=[],
      author=u'Hugh Sorby',
      author_email='',
      url='https://github.com/ABI-Software/MedTech-Core-PelvisDemo',
      license='Apache',
      packages=find_packages('src', exclude=['tests', 'tests.*', ]),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=True,
      install_requires=dependencies,
      entry_points={'console_scripts': [name + '=medtechcore.pelvisdemo.main:main']},
      cmdclass={'install': install, 'develop': develop}
      )
