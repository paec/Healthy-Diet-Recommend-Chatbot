// This example uses MediaRecorder to record from a live audio stream,
// and uses the resulting blob as a source for an audio element.
//
// The relevant functions in use are:
//
// navigator.mediaDevices.getUserMedia -> to get audio stream from microphone
// MediaRecorder (constructor) -> create MediaRecorder instance for a stream
// MediaRecorder.ondataavailable -> event to listen to when the recording is ready
// MediaRecorder.start -> start recording
// MediaRecorder.stop -> stop recording (this will generate a blob of data)
// URL.createObjectURL -> to create a URL from a blob, which we can use as audio src

var recordButton, stopButton, recorder;

function record_init() {
  
  recordButton = document.getElementById('record');
  stopButton = document.getElementById('stop');
  // get audio stream from user's mic
  navigator.mediaDevices.getUserMedia({
    audio: true
  })
  .then(function (stream) {
    recordButton.disabled = false;
    recordButton.addEventListener('click', startRecording);
    stopButton.addEventListener('click', stopRecording);
    //recorder = new MediaRecorder(stream, {mimeType: 'audio/webm'});
	var option={
	audioBitsPerSecond : 128000
	}
    recorder = new MediaRecorder(stream, option);
	//console.dir(recorder.mimeType);
    // listen to dataavailable, which gets triggered whenever we have
    // an audio blob available
    recorder.addEventListener('dataavailable', onRecordingReady);
  });
};

function startRecording() {
  recordButton.disabled = true;
  stopButton.disabled = false;

  recorder.start();
}

function stopRecording() {
  recordButton.disabled = false;
  stopButton.disabled = true;
  // Stopping the recorder will eventually trigger the `dataavailable` event and we can complete the recording process
  recorder.stop();
}

function onRecordingReady(e) {
  var audio = document.getElementById('audio');
  // e.data contains a blob representing the recording
  audio.src = URL.createObjectURL(e.data);
  //audio.play();
  upload(e.data);
}

function upload(blob) {
  var xhr=new XMLHttpRequest();
  xhr.onload=function(e) {
  if(this.readyState == 4) {
  	console.log(xhr);
    var array=JSON.parse(xhr.responseText);
	//var sp = xhr.responseText.split("\n");
	//console.log(sp);
	//var array=JSON.parse(sp[3]);
    //console.log(array.message);
    //console.log(xhr.responseText);
	console.log(array);
    var temp = array.message.split("result:");
	var order=temp[1].split("1.");
	var order2=order[1].split("2.");
	temp[1] = order2[0];
	document.getElementById("outputSentence").innerHTML=temp[1];
	console.log(temp[1]);
    //document.getElementById("outputSentence").innerHTML=temp[1];
	//if (temp[1].search("same with ori")== -1)
	//{
	//	document.getElementById("outputSentence").innerHTML =temp[1];
	//}
	//else
	//{
	//	var ori = temp[0].split("ori:");
	//	temp[1] = ori[1];
	//	document.getElementById("outputSentence").innerHTML = temp[1];
	//}
var httpRequest;
 httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
      alert('Giving up :( Cannot create an XMLHTTP instance');
      return false;
    }
        var oXHR=new XMLHttpRequest();
        para= "sentence="+temp[1];
        oXHR.open("POST", "./Android_app/SentencesAnalysis.php" ,true);
        oXHR.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        oXHR.onreadystatechange= function(){
                  if(oXHR.readyState==4 &&(oXHR.status==200||oXHR.status==304)){
                        console.log(oXHR.responseText);
			var sentence = temp[1];
			var string_all = oXHR.responseText;
                        var array_all = new Array();
                        var array_all = string_all.split(";");
                        //console.log(array_all[1]);
						document.getElementById("outputSentence").innerHTML= array_all[0];
                        var groupname = document.getElementById("groupname");
                        if(array_all[1]!=="NULL")
                                groupname.value = array_all[1];
                        var claissify = document.getElementById("classify");
                        if(array_all[2]!=="NULL")
                                classify.value = array_all[2];
                        var groupcity = document.getElementById("city");
                         if(array_all[4]!=="NULL")
                                groupcity.value = array_all[4];
                        var location1 = document.getElementById("location");
                         if(array_all[3]!=="NULL")
                                location1.value = array_all[3];
                        var date1 = document.getElementById("date");
                        if(array_all[5] !=="NULL")
                                date1.value = array_all[5];
                        var time = document.getElementById("time");
                        if(array_all[6] !=="NULL")
                                time.value = array_all[6];
      
                }
        }
        oXHR.send(para);
  }
  };
  xhr.open("POST","https://www.taiwanspeech.ilovetogether.com/tws-cgi/post_server.py",true);
  var formData = new FormData();
  formData.append('src', "W");
  formData.append('mod', "main");
  formData.append('file',blob);
  xhr.send(formData);
  
}
