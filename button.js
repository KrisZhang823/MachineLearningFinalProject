
function myFunction()
{
	var training_data = JSON.parse("the_data.json");
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
                gray_scale.push(gray/255);
            // assign gray scale value    
            canvasData.data[idx + 0] = gray; // Red channel    
            canvasData.data[idx + 1] = gray; // Green channel    
            canvasData.data[idx + 2] = gray; // Blue channel    
            canvasData.data[idx + 3] = 255; // Alpha channel    
        }
    }
	ctx.putImageData(canvasData, 0, 0); 
    


// After you are done styling it, append it to the BODY element
	
	
}