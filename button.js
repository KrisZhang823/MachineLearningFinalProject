var newArr= new Object();
function myFunction()
{

	var gray_scale=new Array();
	var canvas = document.getElementById('canvas'),
    dataUrl = canvas.toDataURL(),
    imageFoo = document.createElement('img');
	imageFoo.src = dataUrl;
	imageFoo.setAttribute('id', 'imageFoo');
// Style your image here
	imageFoo.style.width = '140px';
	imageFoo.style.height = '140px';
	var ntx = canvas.getContext("2d");
	var newcanvas = document.getElementById("newcanvas");
	newcanvas.setAttribute('width',28);
	newcanvas.setAttribute('height',28);
	var ctx = newcanvas.getContext("2d");
	ctx.drawImage(imageFoo,0,0,28,28);
    
    var canvasData = ctx.getImageData(0,0,28,28);
    for ( var x = 0; x < canvasData.width; x++) {    
        for ( var y = 0; y < canvasData.height; y++) {    
    
            // Index of the pixel in the array    
            var idx = (x + y * canvasData.width) * 4;    
            var r = canvasData.data[idx + 0];    
                var g = canvasData.data[idx + 1];    
                var b = canvasData.data[idx + 2];    
                    
                // calculate gray scale value    
                var gray =255-( .299 * r + .587 * g + .114 * b);
            // assign gray scale value
            canvasData.data[idx + 0] = gray; // Red channel    
            canvasData.data[idx + 1] = gray; // Green channel    
            canvasData.data[idx + 2] = gray; // Blue channel    
            canvasData.data[idx + 3] = 255; // Alpha channel    
        }
    }
    for(var i=0;i<canvasData.data.length;i+=4){
        gray_scale.push(canvasData.data[i]);
    }
	ctx.putImageData(canvasData, 0, 0); 
    var weights=newArr.weights;
    var biases=new Array();
    for(var i=0;i<newArr.biases.length;i++){
        biases[i]=new Array();
        for(var j=0;j<newArr.biases[i].length;j++){
            var tmp=newArr.biases[i][j][0];
            biases[i].push(tmp);
        }
    }
    var activations=gray_scale;
    for(var i = 0;i<weights.length;i++){
        var weight=weights[i];
        var bias=biases[i];
        activations =numeric.add(numeric.dot(weight,activations),bias);
        activations =sigmoid(activations);

    }

    var max=indexOfMax(activations);
    alert("it is "+max);

// After you are done styling it, append it to the BODY element
	
	
}

function sigmoid(z){
    return numeric.div(1,numeric.add(numeric.exp(numeric.dot(z,-1)),1));
}

function indexOfMax(arr) {
    if (arr.length === 0) {
        return -1;
    }

    var max = arr[0];
    var maxIndex = 0;

    for (var i = 1; i < arr.length; i++) {
        if (arr[i] > max) {
            maxIndex = i;
            max = arr[i];
        }
    }

    return maxIndex;
}

function loadFile() {
    var input, file, fr;

    if (typeof window.FileReader !== 'function') {
        alert("The file API isn't supported on this browser yet.");
        return;
    }

    input = document.getElementById('fileinput');
    if (!input) {
        alert("Um, couldn't find the fileinput element.");
    }
    else if (!input.files) {
        alert("This browser doesn't seem to support the `files` property of file inputs.");
    }
    else if (!input.files[0]) {
        alert("Please select a file before clicking 'Load'");
    }
    else {
        file = input.files[0];
        fr = new FileReader();
        fr.onload = receivedText;
        fr.readAsText(file);
    }

    function receivedText(e) {
        lines = e.target.result;
        newArr = JSON.parse(lines);

    }
}

// function loadJSON(callback) {
//
//     var xobj = new XMLHttpRequest();
//         xobj.overrideMimeType("application/json");
//     xobj.open('GET', 'C:\Users\Tingyu\WebstormProjects\MachineLearningFinalProject-master\the_data2.json', true); // Replace 'my_data' with the path to your file
//     xobj.onreadystatechange = function () {
//           if (xobj.readyState == 4 && xobj.status == "200") {
//             // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
//             callback(xobj.responseText);
//           }
//     };
//     xobj.send(null);
//  }
//
// function init() {
//  	loadJSON(function(response) {
//   // Parse JSON string into object
//     var actual_JSON = JSON.parse(response);
//     return actual_JSON;
//  });
// }

