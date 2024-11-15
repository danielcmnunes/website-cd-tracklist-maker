from TracklistLibrary import Util
from TracklistLibrary import TracklistGenerator
from TracklistLibrary import SampleGenerator
import argparse
import logging
import sys

from PyQt5.QtWidgets import QApplication
from gui import App

options = {}

util = None
sample_generator = None
tracklist_generator = None

def parseArguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-v", "--verbose",
                        action='append_const',
                        help="Turn on Verbosity",
                        const=1, default=[])
    
    parser.add_argument("-g", "--gui",
                        action='store_true',
                        help="Turn on GUI")
    
    args = parser.parse_args()
    return args
    
def startlogger(args):    
    VERBOSE = len(args.verbose)
    if VERBOSE == 0:
        logging.basicConfig(level=logging.ERROR)
    elif VERBOSE == 1:
        logging.basicConfig(level=logging.WARNING)
    elif VERBOSE == 2:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger("SampleTracklistCreator")
    return logger

def processTrack(track_directory, track_name, samples_directory):
    audio_file = util.getAudioFile(track_directory, track_name)
    duration = util.getAudioDuration(audio_file)
    
    #audio samples                
    sample = sample_generator.createSample(audio_file)                    
    sample_path = sample_generator.getSamplePath(samples_directory, track_name)
    sample_generator.saveSample(sample, sample_path)
        
    #tracklist                
    tracklist_generator.addTrack(sample_path, track_name, duration)
        
    logger.info("created sample from [%s, %s]" % (track_name, tracklist_generator.humanizeAudioDuration(duration)))

if __name__ == '__main__':
    args = parseArguments()    
    logger = startlogger(args)
    util = Util.Util(logger)
    
    if args.gui:        
        qapp = QApplication(sys.argv)
        app = App.App(logger)
        sys.exit(qapp.exec_())
    
    options = util.loadOptions()
        
    cds_path = options['cds_path']
        
    album_paths = util.getAlbumFolders(cds_path)
        
    logger.info("found albums: %s", str(album_paths))
    
    for album_path in album_paths:
        cd_paths = util.getCDFolders(album_path)
        
        logger.info("found cds %s at album %s" % (str(cd_paths), str(album_path)))        
        
        if len(cd_paths) == 0:
            audio_names = util.getAudioPaths(album_path)
            
            sample_generator = SampleGenerator.SampleGenerator(options, album_path)
            tracklist_generator = TracklistGenerator.TracklistGenerator(options, album_path)   
            
            logger.info("found %d audio files from album  %s (%s)" % (len(audio_names), tracklist_generator.getCDName(), album_path))
            
            samples_path = util.createSamplesDirectory(album_path)
            tracklist_generator.createFile(samples_path)
            
            for audio_name in audio_names:
                processTrack(album_path, audio_name, samples_path)
        else:            
            for cd_path in cd_paths:
                audio_names = util.getAudioPaths(cd_path)
                
                sample_generator = SampleGenerator.SampleGenerator(options, album_path, cd_path)
                tracklist_generator = TracklistGenerator.TracklistGenerator(options, album_path, cd_path)            
                
                logger.info("found %d audio files from cd  %s (%s)" % (len(audio_names), tracklist_generator.getCDName(), cd_path))
                            
                samples_path = util.createSamplesDirectory(cd_path)
                tracklist_generator.createFile(samples_path)
                
                for audio_name in audio_names:
                    processTrack(cd_path, audio_name, samples_path)
                
            tracklist_generator.closeFile()
