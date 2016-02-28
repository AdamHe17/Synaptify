function upload(){
    var x = document.getElementById("bmpfile");
    var txt = "";
    if ('files' in x) {
        if (x.files.length == 0) {
            //txt = "Select your fingerprint '.bmp' file.";
        } else {
            for (var i = 0; i < x.files.length; i++) { //iterate through files
                // txt += "<br><strong>" + (i+1) + ". file</strong><br>";
                // var file = x.files[i];
                // if ('name' in file) {
                //     txt += "name: " + file.name + "<br>";
                // }
                // if ('size' in file) {
                //     txt += "size: " + file.size + " bytes <br>";
                // }

                //RUN SCRIPT AND GENERATE MIDI FILE
            }
        }
    } 
    else {
        if (x.value == "") {
            //txt += "Select your fingerprint '.bmp' file.";
        } else {
            txt += "The files property is not supported by your browser!";
            txt  += "<br>The path of the selected file: " + x.value; // If the browser does not support the files property, it will return the path of the selected file instead. 
        }
    }
    document.getElementById("fileinfo").innerHTML = txt;
}

