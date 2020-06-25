var video = document.querySelector("#videoElement");
		var canvas = document.getElementById("c");

		function takeSnapshot() {
			// debugger;
			// alert ('helllo');
			var img = document.querySelector('img') || document.createElement('img');
			var context;
			var width = video.offsetWidth,
				height = video.offsetHeight;

			canvas = canvas || document.createElement('canvas');
			canvas.width = width;
			canvas.height = height;

			context = canvas.getContext('2d');
			context.drawImage(video, 0, 0, width, height);

			var image = canvas.toDataURL('image/png');

			img.src = image;

			image = image.replace('data:image/png;base64,', '');

			var imageToSend = image;

			document.body.appendChild(img);
			imageToSend = imageToSend.replace(/\//g, '~');

			console.log(imageToSend);

			var string3 = "http://localhost:8000/faceRecognitionApp/recog/";

			console.log(string3);

			var http = new XMLHttpRequest();
			var url = 'http://localhost:8000/faceRecognitionApp/recog/';
			var params = imageToSend;
			http.open('POST', url, true);

			//Send the proper header information along with the request
			// http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

			http.onreadystatechange = function() { //Call a function when the state changes.
				if (http.readyState == 4 && http.status == 200) {
					return http.responseText;
				}
			}
			http.send(params);


		}


		function startStream() {
			var res;
			if (navigator.mediaDevices.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia) {
				navigator.mediaDevices.getUserMedia({
						video: {
							facingMode: "user"
						}
					})
					.then(function(stream) {
						// do
						// {
						video.srcObject = stream;
						// 	res = takeSnapshot();
						// }while(res == "Sorry face not found, Please try again!" || res == null || res == 'undefined');

						// alert("Out of function: " + res);
						// webcamStream = stream;
					})
					.catch(function(err0r) {
						console.log("Something went wrong!: " + err0r);
					});
			}
		}

		function stopStream() {
			var stream = video.srcObject;
			var tracks = stream.getTracks();

			for (var i = 0; i < tracks.length; i++) {
				var track = tracks[i];
				track.stop();
			}

			video.srcObject = null;
		}