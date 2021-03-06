from ophyd import ( Component as Cpt, ADComponent, Signal,
                    EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV,
                    ROIPlugin, StatsPlugin, ImagePlugin,
                    SingleTrigger, PilatusDetector, Device)

from ophyd.areadetector.filestore_mixins import FileStoreIterativeWrite

from ophyd.utils import set_and_wait
from databroker.assets.handlers_base import HandlerBase
from ophyd.device import Staged
from pathlib import Path

import os,time,threading
from types import SimpleNamespace

global DETS
#global DET_replace_data_path
#global default_data_path_root
#global substitute_data_path_root
#DET_replace_data_path = False

global pilatus_trigger_lock
pilatus_trigger_lock = threading.Lock()

class PilatusFilePlugin(Device, FileStoreIterativeWrite):
    file_path = ADComponent(EpicsSignalWithRBV, 'FilePath', string=True)
    file_number = ADComponent(EpicsSignalWithRBV, 'FileNumber')
    file_name = ADComponent(EpicsSignalWithRBV, 'FileName', string=True)
    file_template = ADComponent(EpicsSignalWithRBV, 'FileTemplate', string=True)
    file_number_reset = 1
    sub_directory = None
    froot = data_file_path.gpfs
    enable = SimpleNamespace(get=lambda: True)

    # this is not necessary to record since it contains the UID for the scan, useful
    # to save in the CBF file but no need in the data store
    #file_header = ADComponent(EpicsSignal, "HeaderString", string=True)

    # this is not necessary to record in the data store either, move to the parent
    #reset_file_number = Cpt(Signal, name='reset_file_number', value=1)

    #filemover_files = Cpt(EpicsSignal, 'filemover.filename')
    #filemover_target_dir = Cpt(EpicsSignal, 'filemover.target')
    #filemover_move = Cpt(EpicsSignal, 'filemover.moving')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._datum_kwargs_map = dict()  # store kwargs for each uid
        self.filestore_spec = 'AD_CBF'

    def stage(self):
        global proposal_id
        global run_id
        global current_sample
        global data_path

        f_tplt = '%s%s_%06d_'+self.parent.detector_id+'.cbf'
        set_and_wait(self.file_template, f_tplt, timeout=99999)

        if self.parent.name == first_Pilatus() or self.parent.name == first_PilatusExt():
            #print("first Pilatus is %s" % self.parent.name)
            change_path()

        # if file number reset is Ture, use 1 as the next file #
        # if reset is False, when the first Pilatus/PilatusExt instance is staged, the file# will be
        # synchronized to the highest current value
        if PilatusFilePlugin.file_number_reset==1:
            print("resetting file number for ", self.parent.name)
            # it is a bad idea to wait since auto-increment may change this value immediately
            #set_and_wait(self.file_number, 1, timeout=99999)   
            self.file_number.put(1)
            print('done.')
        elif self.parent.name == first_Pilatus():
            next_file_number = np.max([d.file.file_number.get() for d in pilatus_detectors])
            for d in pilatus_detectors:
                print("setting file number for %s to %d." % (d.name, next_file_number))
                set_and_wait(d.file.file_number, next_file_number, timeout=99999)
        elif self.parent.name == first_PilatusExt():
            next_file_number = np.max([d.file.file_number.get() for d in pilatus_detectors_ext])
            for d in pilatus_detectors_ext:
                print("setting file number for %s to %d." % (d.name, next_file_number))
                set_and_wait(d.file.file_number, next_file_number, timeout=99999)

        if PilatusFilePlugin.sub_directory is not None:
            f_path = data_path+PilatusFilePlugin.sub_directory
            RE.md['subdir'] = PilatusFilePlugin.sub_directory
        else:
            f_path = data_path
            if 'subdir' in RE.md.keys():
                del RE.md['subdir']
        f_fn = current_sample
        # file_path must ends with '/'
        print('%s: setting file path ...' % self.name)
        #if DET_replace_data_path:
        if self.froot == data_file_path.ramdisk:
            #f_path = f_path.replace(default_data_path_root, substitute_data_path_root)
            f_path = f_path.replace(data_file_path.gpfs.value, data_file_path.ramdisk.value) 
        set_and_wait(self.file_path, f_path, timeout=99999) 
        #set_and_wait(self.file_path, f_path, timeout=99999)
        set_and_wait(self.file_name, f_fn, timeout=99999)
        self._fn = Path(f_path)

        fpp = self.get_frames_per_point()
        # when camserver collects in "multiple" mode, another number is added to the file name
        # even though the template does not specify it. 
        # Camserver doesn't like the template to include the second number
        # The template will be revised in the CBF handler if fpp>1

        print('%s: super().stage() ...' % self.name)
        super().stage()
        res_kwargs = {'template': f_tplt, # self.file_template(),
                      'filename': f_fn, # self.file_name(),
                      'frame_per_point': fpp,
                      'initial_number': self.file_number.get()}
        print('%s: _generate_resource() ...' % self.name)
        self._generate_resource(res_kwargs)

    def unstage(self):
        super().unstage()
        ##12/19/17 commented out
        # move the files from ramdisk to GPFS
        #if self.filemover_move.get()==1:
        #    print("files are still being moved from the detector server to ",self.filemover_target_dir.get())
        #    while self.filemover_move.get()==1:
        #        sleep(1)
        #    print("done.")
        #self.filemover_files.put(current_sample)
        #self.filemover_target_dir.put(data_path)
        #self.filemover_move.put(1)
        ##12/19/17 commented out
        #if self.parent.name == first_Pilatus() or self.parent.name == first_PilatusExt():
        #    release_lock()

    def get_frames_per_point(self):
        #return self.parent.cam.num_images.get()   # always return 1 before 2018
        return self.parent._num_images

class LIXPilatus(SingleTrigger, PilatusDetector):
    # this does not get root is input because it is hardcoded above
    file = Cpt(PilatusFilePlugin, suffix="cam1:",
               write_path_template="", root='/')

    #roi1 = Cpt(ROIPlugin, 'ROI1:')
    #roi2 = Cpt(ROIPlugin, 'ROI2:')
    #roi3 = Cpt(ROIPlugin, 'ROI3:')
    #roi4 = Cpt(ROIPlugin, 'ROI4:')

    #stats1 = Cpt(StatsPlugin, 'Stats1:')
    #stats2 = Cpt(StatsPlugin, 'Stats2:')
    #stats3 = Cpt(StatsPlugin, 'Stats3:')
    #stats4 = Cpt(StatsPlugin, 'Stats4:')

    #reset_file_number = Cpt(Signal, name='reset_file_number', value=1)
    HeaderString = Cpt(EpicsSignal, "cam1:HeaderString")
    ThresholdEnergy = Cpt(EpicsSignal, "cam1:ThresholdEnergy")

    def __init__(self, *args, detector_id, **kwargs):
        self.detector_id = detector_id
        self._num_images = 1
        super().__init__(*args, **kwargs)

    def set_thresh(self, ene):
        """ set threshold
        """
        set_and_wait(self.ThresholdEnergy, ene)
        self.cam.threshold_apply.put(1)

    def set_num_images(self, num_images):
        self._num_images = num_images

    def stage(self):
        if self._staged == Staged.yes:
            return

        self.cam.num_images.put(self._num_images)
        time.sleep(.1)
        self.cam.trigger_mode.put(0, wait=True)
        super().stage()

    def unstage(self):
        if self._staged == Staged.no:
            return

        self.cam.num_images.put(1, wait=True)
        super().unstage()


############## below is based on code written by Bruno
############## hardware triggering for Pilatus detectors
class PilatusExtTrigger(PilatusDetector):
    armed = Cpt(EpicsSignal, "cam1:Armed")

    # Use self._image_name as in SingleTrigger?
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._num_images = 1
        self._acquisition_signal = self.cam.acquire
        self._counter_signal = self.cam.array_counter
        #self._trigger_signal = EpicsSignal('XF:16ID-TS{EVR:C1-Out:FP3}Src:Scale-SP')
        self._trigger_signal = EpicsSignal('XF:16IDC-ES{Zeb:1}:SOFT_IN:B0')
        
        self._status = None
        self.first = True
        self.acq_t = 0

    def set_num_images(self, num_images):
        self._num_images = num_images

    def stage(self, multitrigger=True):
        if self._staged == Staged.yes:
            return

        print(self.name, "staging")
        #self.stage_sigs.update([
        #    ('cam.trigger_mode', 3), # 2 DOESN'T WORK!
        #    ('cam.num_images', self._num_images)
        #])
        
        acq_t = self.cam.acquire_period.get()

        if multitrigger:
            self.cam.trigger_mode.put(3, wait=True)   # ExtMTrigger in camserver
            self.trig_wait = acq_t+0.02
        else:
            self.cam.trigger_mode.put(2, wait=True)   # ExtTrigger in camserver
            self.trig_wait = acq_t*self._num_images+0.02

        time.sleep(.1)

        self.cam.num_images.put(self._num_images, wait=True)
        print(self.name, "stage sigs updated")
        super().stage()
        print(self.name, "super staged")
        self._counter_signal.put(0)

        print(self.name, "checking armed status")
        self._acquisition_signal.put(1) #, wait=True)
        while self.armed.get() != 1:
            time.sleep(0.1)

        print(self.name, "staged")

    def unstage(self):
        if self._staged == Staged.no:
            return
        
        self._status = None
        self._acquisition_signal.put(0)
        
        time.sleep(.1)
        self.cam.trigger_mode.put(0, wait=True)
        time.sleep(.1)
        self.cam.num_images.put(1, wait=True)
        super().unstage()
        
    def trigger(self):
        print(self.name+" trigger")
        if self._staged != Staged.yes:
            raise RuntimeError("This detector is not ready to trigger."
                               "Call the stage() method before triggering.")

        status = DeviceStatus(self)
        # Only one Pilatus has to send the trigger
        if self.name == first_PilatusExt():
            while pilatus_trigger_lock.locked():
                time.sleep(0.005)
            print("triggering")
            self._trigger_signal.put(1, wait=True)
            self._trigger_signal.put(0, wait=True)
            ##set up callback to clear status after the end-of-exposure
            threading.Timer(self.trig_wait, status._finished, ()).start()
        else:
            status._finished()

        self.dispatch(f'{self.name}_image', ttime.time())
        return status


class LIXPilatusExt(PilatusExtTrigger):
    file = Cpt(PilatusFilePlugin, suffix="cam1:",
               write_path_template="")

    #roi1 = Cpt(ROIPlugin, 'ROI1:')
    #roi2 = Cpt(ROIPlugin, 'ROI2:')
    #roi3 = Cpt(ROIPlugin, 'ROI3:')
    #roi4 = Cpt(ROIPlugin, 'ROI4:')

    #stats1 = Cpt(StatsPlugin, 'Stats1:')
    #stats2 = Cpt(StatsPlugin, 'Stats2:')
    #stats3 = Cpt(StatsPlugin, 'Stats3:')
    #stats4 = Cpt(StatsPlugin, 'Stats4:')

    #reset_file_number = Cpt(Signal, name='reset_file_number', value=1)
    HeaderString = Cpt(EpicsSignal, "cam1:HeaderString")   # was missing before 2018

    def __init__(self, *args, **kwargs):
        self.detector_id = kwargs.pop('detector_id')
        super().__init__(*args, **kwargs)


try:
    pil1M = LIXPilatus("XF:16IDC-DT{Det:SAXS}", name="pil1M", detector_id="SAXS")
    pilW1 = LIXPilatus("XF:16IDC-DT{Det:WAXS1}", name="pilW1", detector_id="WAXS1")
    pilW2 = LIXPilatus("XF:16IDC-DT{Det:WAXS2}", name="pilW2", detector_id="WAXS2")

    pil1M_ext = LIXPilatusExt("XF:16IDC-DT{Det:SAXS}", name="pil1M_ext", detector_id="SAXS")
    pilW1_ext = LIXPilatusExt("XF:16IDC-DT{Det:WAXS1}", name="pilW1_ext", detector_id="WAXS1")
    pilW2_ext = LIXPilatusExt("XF:16IDC-DT{Det:WAXS2}", name="pilW2_ext", detector_id="WAXS2")

    pilatus_detectors = [pil1M, pilW1, pilW2]
    pilatus_detectors_ext = [pil1M_ext, pilW1_ext, pilW2_ext]
except:
    print("Could not initilize Pilatus detectors ...")
    pilatus_detectors = []
    pilatus_detectors_ext = []
    

def first_Pilatus():
    #print("checking first Pialtus")
    for det in DETS:
        if det.__class__ == LIXPilatus:
            #print(det.name)
            return det.name
    return None

def first_PilatusExt():
    #print("checking first Pialtus")
    for det in reversed(DETS):
        if det.__class__ == LIXPilatusExt:
            #print(det.name)
            return det.name
    print("Warning: No Pilatus detectors are being used.")
    return None

for det in pilatus_detectors+pilatus_detectors_ext:
    det.read_attrs = ['file']

def pilatus_number_reset(status):
    val = 1 if status else 0
    PilatusFilePlugin.file_number_reset = val

def pilatus_ct_time(exp):
    for det in pilatus_detectors:
        det.cam.acquire_time.put(exp)
        det.cam.acquire_period.put(exp+0.005)
        
def pilatus_use_sub_directory(sd=None):
    if sd is not None:
        if sd[-1]!='/':
            sd += '/'
        makedirs(data_path+sd)
    PilatusFilePlugin.sub_directory = sd

def pilatus_set_thresh():
    ene = int(getE()/10*0.5+0.5)*0.01
    for det in pilatus_detectors:
        det.set_thresh(ene)

def set_pil_num_images(num):
    for d in pilatus_detectors+pilatus_detectors_ext:
        d.set_num_images(num)

def stage_pilatus(multitrigger=True):
    for det in DETS:
        if det.__class__ == LIXPilatusExt:
            det.stage(multitrigger=multitrigger)
        elif det.__class__ == LIXPilatus:
            det.stage()
            
def unstage_pilatus():
    for det in DETS:
        if det.__class__ == LIXPilatusExt or det.__class__ == LIXPilatus:
            det.unstage()
