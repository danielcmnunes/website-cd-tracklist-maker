import os
import unidecode
import time
import datetime

class TracklistGenerator():
    def __init__(self, options, album_path=str, cd_path=None):
        self.html = ""
        self.options = options
        self.plugin_shortcode = options['plugin_shortcode']
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
    
    def getTrackNumber(self, audio_name):
        return audio_name.split(" - ")[0]    
      
    def getTrackName(self, audio_name):
        return audio_name.split(" - ", 1)[1].replace(".mp3", "")
    
    def humanizeAudioDuration(self, duration):
        return time.strftime('%M\'%S', time.gmtime(duration))
         
    def assembleURL(self, path, audio_name):
        wp_url = self.options['upload_url']
        
        wp_file_name = audio_name.replace(" ", "-")
        wp_file_name = wp_file_name.replace("---", "-")
        wp_file_name = wp_file_name.replace(",-", "-")
        wp_file_name = wp_file_name.replace(u'ß', "s")
        wp_file_name = unidecode.unidecode(wp_file_name)

        wp_file_name = wp_file_name.replace('\'', "")
        wp_file_name = wp_file_name.replace("(", "")
        wp_file_name = wp_file_name.replace(")", "")
        
        now = datetime.datetime.now()
        year = str(now.year)
        month = str(now.month)
        if(len(month) == 1):
            month = "0"+month
            
        if self.cd_name:
            url = wp_url + year +"/"+ month +"/" + self.album_name + '-Sample-' + self.cd_name + '-' + wp_file_name
        else:
            url = wp_url + year +"/"+ month +"/" + self.album_name + '-Sample-' + wp_file_name
        
        return url
    
    def createFile(self, path):
        self.out = open(r""+ path+"_tracklist.txt","w")
        
        #top left of the table
        self.out.write("<table>\n")
        self.out.write("<tr>\n")
        self.out.write("<th>"+ self.getCDName() +"</th>\n")
        self.out.write("<th></th>\n")
        self.out.write("<th></th>\n")
        self.out.write("<th></th>\n")
        self.out.write("<th></th>\n")
        self.out.write("</tr>")
        
    def addTrack(self, sample_file_path, audio_name, duration):
        track_number = self.getTrackNumber(audio_name)
        track_name = self.getTrackName(audio_name)
        duration = self.humanizeAudioDuration(duration)
        
        url = self.assembleURL(sample_file_path, audio_name)
        
        shortcode = self.plugin_shortcode % url

        self.out.write("<tr>\n")
        self.out.write("<th></th>\n")
        self.out.write("<th>"+ track_number +"</th>\n")
        self.out.write("<th>"+ track_name +"</th>\n")
        self.out.write("<th>"+ duration +"</th>\n")
        self.out.write("<th>"+ shortcode +"</th>\n")
        self.out.write("</tr>")

    def closeFile(self):
        self.out.write("</table>")
        self.out.close()