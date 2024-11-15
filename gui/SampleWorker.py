from PyQt5.QtCore import QThread, pyqtSignal
from TracklistLibrary import Util
from TracklistLibrary import TracklistGenerator
from TracklistLibrary import SampleGenerator

class SampleWorker(QThread):
    _signal_log = pyqtSignal(str)
    _signal_progress = pyqtSignal(int)
    
    def __init__(self, logger, cds_path):
        super(SampleWorker, self).__init__()
        self.cds_path = cds_path
        self.logger = logger
        self.util = Util.Util(logger)
        self.options = self.util.loadOptions()
        
        self.total_progress_steps = 0
        self.progress_steps = 0
    
    def log(self, msg):
        """_summary_

        Args:
            msg (_type_): _description_
        """
        self._signal_log.emit(msg)

    def updateProgress(self):
        """ increments progress_steps and emits a signal to the UI with the calculated percentage
        """
        self.progress_steps += 1        
        percentage = self.progress_steps / self.total_progress_steps * 100
        percentage = int(round(percentage))
        self._signal_progress.emit(percentage)

    def stop(self):
        self.isRunning = False
        
    def processTrack(self, track_path, track_name, samples_path):
        """ creates the audio sample, adds entry to the tracklist and updates progress

        Args:
            track_path (str): path where the audio file is located
            track_name (str): audio file name
            samples_path (str): path where to save the new sample
        """
        audio_file = self.util.getAudioFile(track_path, track_name)
        duration = self.util.getAudioDuration(audio_file)
        
        #audio samples                
        sample = self.sample_generator.createSample(audio_file)                    
        sample_path = self.sample_generator.getSamplePath(samples_path, track_name)
        self.sample_generator.saveSample(sample, sample_path)
        
        self.updateProgress()
        
        #tracklist                
        self.tracklist_generator.addTrack(sample_path, track_name, duration)
        
        self.updateProgress()
        
        self.log("created sample from [%s, %s]" % (track_name, self.tracklist_generator.humanizeAudioDuration(duration)))

    def run(self):
        """ SampleWorker main thread loop
        """      
        self.isRunning = True
        
        # each file will 2 progress update: one when the audio sample is created, a second one when the tracklist row is created
        self.total_progress_steps = 2* self.util.getTotalFiles(self.cds_path)
                
        album_paths = self.util.getAlbumFolders(self.cds_path)
                
        self.log("found %d albums" % len(album_paths))
        
        for album_path in album_paths:
            cd_paths = self.util.getCDFolders(album_path)
            
            self.log("found %d cds at album %s" % (len(cd_paths), str(album_path.split('\\')[-1])))        
            
            if len(cd_paths) == 0:
                audio_names = self.util.getAudioPaths(album_path)
                
                self.sample_generator = SampleGenerator.SampleGenerator(self.options, album_path)
                self.tracklist_generator = TracklistGenerator.TracklistGenerator(self.options, album_path)   
                
                samples_path = self.util.createSamplesDirectory(album_path)
                self.tracklist_generator.createFile(samples_path)
                
                for audio_name in audio_names:
                    if not self.isRunning:
                        break
                    
                    self.processTrack(album_path, audio_name, samples_path)
            else:            
                for cd_path in cd_paths:                            
                    audio_names = self.util.getAudioPaths(cd_path)
                    
                    self.sample_generator = SampleGenerator.SampleGenerator(self.options, album_path, cd_path)
                    self.tracklist_generator = TracklistGenerator.TracklistGenerator(self.options, album_path, cd_path)            
                    
                    self.log("found %d audio files at %s" % (len(audio_names), self.tracklist_generator.getCDName()))
                                
                    samples_path = self.util.createSamplesDirectory(cd_path)
                    self.tracklist_generator.createFile(samples_path)
                    
                    for audio_name in audio_names:
                        if not self.isRunning:
                            break
                        
                        self.processTrack(cd_path, audio_name, samples_path)
                    
                self.tracklist_generator.closeFile()
            