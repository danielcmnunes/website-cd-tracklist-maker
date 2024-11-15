import os
import json
import pydub
from datetime import datetime
from pydub import AudioSegment

class Util():
    def __init__(self, logger):
        self.logger = logger
        
    def loadOptions(self):
        json_file_path = r"options.json"
        
        with open(json_file_path, "r") as f:        
            return json.load(f)
        
    def setFFMpeg(self, path):
        #not working
        pydub.AudioSegment.ffmpeg = r"%s\\ffmpeg.exe" % path
        pydub.AudioSegment.ffplay = r"%s\\ffplay.exe" % path
        pydub.AudioSegment.ffprobe = r"%s\\ffprobe.exe" % path
  
    def createSamplesDirectory(self, path):
        """Creates an output directory at the folder given by the input path.

        Keyword arguments:    
        input_path -- the cd path
        """
        path += "_samples"
        try:
            os.mkdir(path)
            os.chmod(path, 0o775)
        except FileExistsError:
            self.logger.warning("folder already exists")        
        
        return path
    
    def getTotalFiles(self, input_path):
        """_summary_

        Args:
            input_path (_type_): _description_

        Returns:
            _type_: _description_
        """        
        total_files = 0
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if ".mp3" in file and "Sample" not in file:
                    total_files += 1
        return total_files
                
    def getAlbumFolders(self, input_path):
        album_folders = []
        for root, dirs, _ in os.walk(input_path):
            try:
                dirs.remove('__pycache__')
            except:
                print("")
                
            for dir in dirs:                
                if "_samples" in dir:
                    continue
                else:
                    album_folders.append( os.path.join(root, dir))
                    
            break
        return album_folders

    def getCDFolders(self, input_path):
        cd_folders = []
        for root, dirs, _ in os.walk(input_path):
            try:
                dirs.remove('__pycache__')
            except:
                print("")
            
            #filter existing sample directories
            for dir in dirs:
                if "_samples" in dir:
                    continue
                else:
                    cd_folders.append( os.path.join(root, dir))
            break
        return cd_folders
        
    def getAudioPaths(self, input_path):
        audios = []
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if ".mp3" in file:
                    audios.append(file)
        return audios

    def getAudioFile(self, folder_path, file_name):
        file_path = os.path.join(folder_path, file_name)
        audio = AudioSegment.from_file(file_path)
        return audio

    def getAudioDuration(self, audio_file):
        duration = audio_file.duration_seconds + 1
        return duration
