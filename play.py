#!/C:\Program Files (x86)\Python27\python
from __future__ import division
from operator import itemgetter
import sys
import matlab.engine
import math
import numpy
import matlab_to_python as mtp
import cgi
import cgitb
import image_to_midi as itm

form = cgi.FieldStorage()
filename = form['bmp'].value
print filename
in_file_path = "C:\\Images\\Fingerprint Images\\" + filename

image_data = mtp.process_image(in_file_path)
out_file_path = "C:\\Users\\Admin\\Desktop\\Final Music\\" + filename
itm.make_MIDI(image_data, out_file_path)

print "Content-type: text/html \r\n\r\n"

print '<!doctype html>\n<html>\n   <link rel="stylesheet" type="text/css" href="./lib/style.css">\n   <head>\n      <script src = "./lib/angular.min.js"></script>\n      <script src = "./lib/generate.js"></script>\n      <script type=\'text/javascript\' src=\'http://www.midijs.net/lib/midi.js\'></script>\n      <script src = "./lib/runpy.php"></script>\n      <title>Synaptify</title>\n   </head>\n   \n   <body ng-app = "myapp" onload="upload()">\n\n      <div id="header"><h1>Synaptify<img src="./lib/pixelnote.png" height="4.7%" width="4.7%" position="relative"/></h1></div>\n\n      <div id="spacer"><h1></h1></div>\n\n      <div id="instructions">\n         <h4>Make a unique song with your fingerprint!</h4>\n         <p>Upload your "bmp" file:</p>\n      </div>\n\n      <form id="myform" action="play.py">\n         <input type="file" id="bmpfile" name="bmp" accept=".bmp" multiple size="50" onchange="upload()">\n         <input type="submit" value="Submit" onClick="/lib/runpy.php">\n      </form>\n\n\n      <p id="fileinfo"></p>\n      <div id="play">\n         <h4><br>Listen to your fingerprint:</h4>\n         <a href="#play" onClick="MIDIjs.play('+ out_file_path + ');"><img src="./lib/play.png" height="5%" width="5%"/></a>\n         <a href="#stop" onClick="MIDIjs.stop();"><img src="./lib/stop.png" height="5.8%" width="5.8%"/></a>\n      </div>\n\n\n      <div id="info">\n         <p>Pitch, key, rhythm, and tempo are based on characteristics of your fingerprint ridges:\n            <ul text-align="left">\n               <li>"spread": the distance between ridges</li>\n               <li>"splits": a ridge splits into two</li>\n               <li>"ends": a ridge discontinues</li>\n            </ul>\n         </p>\n      </div>\n      <!-- <div ng-controller = "HelloController" >\n         <h2>Welcome to {{helloTo.title}}!</h2>\n         <p>Enter your Name: <input type = "text" ng-model = "name"></p>\n         <p>Hello <span ng-bind = "name"></span>!</p>\n      </div>  -->\n      \n      <script>\n         angular.module("myapp", []).controller("HelloController", function($scope) {\n            $scope.helloTo = {};\n            $scope.helloTo.title = "Synaptify";\n         });\n\n         angular.module("myapp", []).controller(\'AppController\', function($scope) {\n         $scope.toggle = true;\n         $scope.$watch(\'toggle\', function(){\n         $scope.toggleText = $scope.toggle ? \'Toggle!\' : \'some text\';\n         })\n         })\n\n         \n      </script>\n\n\n      <div id="footer">\n      <button ng-click="toggle = !toggle">Created at HackTech2016</button>\n         <div class="box on" ng-show="toggle" ng-animate="\'box\'">\n            <p><b>By Adam He, Dylan Ong, Eric Hao, and Max Schuman:<b><br>\n            <a href="https://github.com/AdamHe17/Synaptify" color="white"><img src="./lib/github.png" height="10%" width="10%"/></a></p>\n         </div>\n      </div>\n      \n   </body>\n</html>\n'

