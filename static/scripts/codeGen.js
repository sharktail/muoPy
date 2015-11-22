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
                //document.getElementById("downloadLink").href = fnamelist.downloadLink;
                //document.getElementById("downloadJSONLink").href = ;
                if(currentFile != "")
                	{
	                    $.post("/codegen/load", { Data: currentFile},
		       	 				function(result)
		       	 				{
									$("#textAreaId").html(result);
								}, "json");
                	}
				$("#saveButtonId").click( //saveFile);
					function()
						{
						    if(currentFile!="")
						    	{
						    		$.post("/codegen/save",
	    				       			{ Data: $("#textAreaId").val(), fileName: currentFile},
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
    						$.get("/codegen/execute", { fileName: currentFile, action: "executeForCode"},
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
				$("#nextButtonId").click(
						function()
						{
							if(currentFile=="")
							    	{
							    		alert("Set current file by clicking on the list");
							    	}
							else
							{
//	    						$.get("/codegen/datagen", { fileName: currentFile, action: "redirect"},
//	    								function(result)
//	    								{
//	    									alert("hello");
//	    								}, "json");
								$form = $('<form></form>');
								$form.attr('action', '/codegen/datagen');
								$form.attr('method', 'get');
								$form.append('<input name="fileName" value="' + currentFile.split(".")[0] + '">');
								$form.appendTo('body').submit();
	    					}
						}
					);
	   		}
	   		);

//function prbToDat()
//{
//	get("/codegen/datagen", {fileName : currentFile})
//	}

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
		post("/codegen/save", { Data: $("#textAreaId").val(), fileName: currentFile} 
		);
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
	var fileTree = fnamelist.fileTree;
    var a = document.getElementById("currentFileName");
    
    //this is to add the sub division of dat files in tree structure
    if(this.showDat == 0)
    	{
	        var each = document.createElement("div");
	        //each.setAttribute("style", "position: relative; left:20px;"); 
	        each.setAttribute("class", "fileTree");
	        
	        for(var i=0; i <fileTree[this.fileName].length; i++)
	        	{
	        	    var dd = document.createElement("dd");
	        	    dd.appendChild(document.createTextNode(fileTree[this.fileName][i]));
	        	    each.appendChild(dd);
	        	}
	        this.appendChild(each);
	        this.showDat = 1;
    	}
    else if(this.showDat == 1)
    	{
    	    //this.find(".fileTree") //Using Jquery
    	    var fileTree = this.getElementsByClassName("fileTree")[0]; //getElementByClassName returns a list
    	    fileTree.style.display = "none";
    	    this.showDat = 2;
    	}
    
    else if(this.showDat == 2)
    	{
    	    var fileTree = this.getElementsByClassName("fileTree")[0] //getElementByClassName returns a list
    	    fileTree.style.display = "block";
	        this.showDat = 1;
    	}
    
    currentFile = this.fileName;
    a.innerHTML = "Current File Set to:" + currentFile;
    $.post("/codegen/load", { Data: currentFile},
				       	 				function(result)
				       	 				{
											$("#textAreaId").html(result);
    										//document.getElementById("textAreaId").innerHTML = result;
										}, "json");
    
    $.get("/codegen/downloadlink", {fileName: currentFile}, 
    		function(result)
    		{
    			dwnld = document.getElementById("downloadZIPLink");
    			dwnld.href = result;
    			if (result==null)
    				{
    					dwnld.style.visibility = "hidden";
    				}
    			else
    				{
    					dwnld.style.visibility = "visible";
    				}
    		}, "json");
}

function datFileListOnclick()
{
	var a = document.getElementById("currentDatFileName");
	currentDatFile = this.fileName;
    a.innerHTML = "Current Data File Set to:" + currentDatFile;
    $.post("/codegen/load", { Data: currentDatFile},
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
	          var item = document.createElement('dt');
	          item.showDat = 0;
	          item.fileName = names[i]; //just to carry some data to the onclick function
	          
        	  if (names[i].split(".").pop()=="prb")
        		  {
        		  	item.onclick = prbFileListOnclick; //this function is to make it a method and prevents it from calling the fileListOnclick function itself
        		  	//item.setAttribute("class", "listItems");
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