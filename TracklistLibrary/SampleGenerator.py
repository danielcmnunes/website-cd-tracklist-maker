import os


class SampleGenerator():
    def __init__(self, options, album_path=str, cd_path=None):
        self.options = options
        self.album_name = album_path.split(os.sep)[-1]
        
        if cd_path != None:
            self.cd_name = cd_path.split(os.sep)[-1]
        else:
            self.cd_name = None
        
    def getCDName(self):
        if self.cd_name:
            return self.cd_name
        else:
            return self.album_name
    
    def createSample(self, audio_file):
        sample_duration = int(self.options['sample_duration']) * 1000
        fade_out_duration = int(self.options['fade_out_duration']) * 1000
        
        clipped_audio = audio_file[0:sample_duration]
            
        faded_audio = clipped_audio.fade_out(fade_out_duration)
        
        return faded_audio
    
    def getSamplePath(self, samples_path, audio_name):
        if self.cd_name:
            sample_name = "%s %s %s %s" % (self.album_name, self.cd_name, "Sample", audio_name)
        else:            
            sample_name = "%s %s %s" % (self.album_name, "Sample", audio_name)
            
        path = os.path.join(samples_path, sample_name)        
        return path
    
    def saveSample(self, audio_file, path):                
        audio_file.export(path, format="mp3")