flist = flist.replace(/&quot;/ig,'"');
flist = flist.replace(/&amp;/ig,'&');
var fnamelist = JSON.parse(flist);

var arg = arg.replace(/&quot;/ig,'"');
var arg = arg.replace(/&amp;/ig,'&');
try
    {
        var st = JSON.parse(arg);
        var parsedText = st.data;
    }
catch(err)
    {
        var parsedText = "Unable to parse the data. \n Error: " + err.message; 
    }

var currentFile = "";
var currentDatFile = "";

try
{
    currentFile = fnamelist.currentFile;
}
catch(err)
    {
        alert("Current File Error: "+ err.message); 
    }

$(document).ready(
		function()
			{
			    var a = document.getElementById("currentFileName");
                a.innerHTML = "Current PRB File Set to:" + currentFile;
                $("#dataGenPage").slideUp("slow");
                //document.getElementById("downloadLink").href = fnamelist.downloadLink;
                //document.getElementById("downloadJSONLink").href = ;
                
				//$("#saveButtonId").click( saveFile);
				$("#saveButtonId").click(
					function()
						{
						    if(currentDatFile!="")
						    	{
						    		$.post("/datagen/save",
	    				       			{ Data: $("#textAreaId").val(), fileName: currentDatFile},
	    				       			function(result)
		    				       			{
		    				       				$("#consoleAreaId").html(result);
		    				       			} 
	    				      			);    	
						    	}
						    else
						    {
						    	alert("Set current file by clicking on the list");
    				      	}
						}
				);
				
				$("#executeButtonId").click(
					function()
					{
						if(currentFile=="")
						    	{
						    		alert("Set current file by clicking on the list");
						    	}
						else
						{
    						$.get("/datagen/execute", { fileName: currentFile, action: "executeForCode"},
    				       	 				function(result)
    				       	 				{
    											$("#consoleAreaId").html(result);
    										}, "json");
    					}
					}
				);
//				$("#executeDataButtonId").click(
//						function()
//						{
//							if(currentFile=="")
//							    	{
//							    		alert("Set current file by clicking on the list");
//							    	}
//							else
//							{
//	    						$.get("/codegen/execute", { fileName: currentDatFile, action: "executeForData"},
//	    				       	 				function(result)
//	    				       	 				{
//	    											$("#consoleAreaId").html(result);
//	    										}, "json");
//	    					}
//						}
//					);
				$("#previousButtonId").click(
						function()
						{
							if(currentFile=="")
							    	{
							    		alert("Set current file by clicking on the list");
							    	}
							else
							{
	    						$.get("/datagen", { fileName: currentFile, action: "executeForData"},
	    				       	 				function(result)
	    				       	 				{
	    											$("#consoleAreaId").html(result);
	    											//$("#dataGenPage").html(result);
	    											$("#codeGenPage").slideDown("slow");
	    											$("#dataGenPage").slideDown("slow");
	    											
	    										}, "json");
	    					}
						}
					);
	   		}
	   		);

function toggleDataSection()
{
	$("#dataGenPage");
	}

function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}

function saveFile()
	{
		//post("/codegen/save", { Data: document.getElementById("textAreaId").innerHTML, fileName: currentFile})
		post("/datagen/save", { Data: $("#textAreaId").val(), fileName: currentDatFile})
	}

function loadTextArea() 
	{
	   //document.getElementById("textAreaId").innerHTML = parsedText;
		$("#textAreaId").html(parsedText);
	}

function fileValidate()
	{
	    var a=document.getElementById("fileInput");
	    if(a.files.length==0)
	    	{
	    	    alert("File not selected");
	    		return false;
	    		}
	    else
	    	{
	    		return true;
	    		}
		}

function prbFileListOnclick()
{
    var a = document.getElementById("currentFileName");
    currentFile = this.fileName;
    a.innerHTML = "Current File Set to:" + currentFile;
    $.post("/codegen/load", { Data: currentFile},
				       	 				function(result)
				       	 				{
											$("#textAreaId").html(result);
    										//document.getElementById("textAreaId").innerHTML = result;
										}, "json");
}

function datFileListOnclick()
{
	var a = document.getElementById("currentDatFileName");
	currentDatFile = this.fileName;
    a.innerHTML = "Current Data File Set to:" + currentDatFile;
    $.post("/datagen/load", { Data: currentDatFile},
				       	 				function(result)
				       	 				{
											$("#textAreaId").html(result);
    										//document.getElementById("textAreaId").innerHTML = result;
										}, "json");
}

function loadListOfFiles()
    {
        var names = fnamelist.fileNames;
        var list = document.getElementById("datFileList");
        var prbFileList = document.getElementById("prbFileList");
        
        for(var i=0; i<names.length; i++)
            { 
	          var item = document.createElement('li');
	          item.fileName = names[i];
	          
        	  if (names[i].split(".").pop()=="prb")
        		  {
        		  	item.onclick = prbFileListOnclick; //this function is to make it a method and prevents it from calling the fileListOnclick function itself
        		  	item.setAttribute("class", "listItems");
        		  	item.appendChild(document.createTextNode(names[i]));
        		  	prbFileList.appendChild(item);
        		  }
        	  else
        		  {
        		  	item.onclick = datFileListOnclick; //this function is to make it a method and prevents it from calling the fileListOnclick function itself
        		  	item.setAttribute("class", "listItems");
        		  	item.appendChild(document.createTextNode(names[i]));
        		  	list.appendChild(item);
        		  }
              
              
            }
    }

function toggle_visibility(showId, hideId)
{
    alert("I do nothing right now !!!");
}

window.onload = function(){
loadTextArea();
loadListOfFiles();
}