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
			    //var a = document.getElementById("currentFileName");
                //a.innerHTML = "Current PRB File Set to:" + currentFile;
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
                $("#fileUploadId").change(
                		function()
                		{
                			this.submit();
                		}
                		);
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
				
				//$("#saveButtonId").click( saveFile);
				$("#saveButtonId").click(
					function()
						{
						    if(currentDatFile != "")
						    	{
						    		$.post("/datagen/save",
	    				       			{ Data: $("#textAreaId").val(), fileName: currentDatFile},
	    				       			function(result)
		    				       			{
		    				       				$("#consoleAreaId").html(result);
		    				       			}, "json");    	
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
						if(currentDatFile=="")
						    	{
						    		alert("Set current file by clicking on the list");
						    	}
						else
						{
    						$.get("/datagen/execute", { fileName: currentDatFile, action: "executeForData"},
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
				
				//data btn section
				//$("#saveButtonId").click( saveFile);
				$("#dataSaveButtonId").click(
					function()
						{
						    if(currentDatFile!="")
						    	{
						    		$.post("/datagen/save",
	    				       			{ Data: $("#textAreaId").val(), fileName: currentDatFile},
	    				       			function(result)
		    				       			{
		    				       				$("#consoleAreaId").html(result);
		    				       			}, "json");    	
						    	}
						    else
						    {
						    	alert("Set current file by clicking on the list");
    				      	}
						}
				);
				
				$("#dataExecuteButtonId").click(
					function()
					{
						if(currentDatFile=="")
						    	{
						    		alert("Set current file5 by clicking on the list");
						    	}
						else
						{
    						$.get("/datagen/execute", { fileName: currentDatFile, action: "executeForData"},
    				       	 				function(result)
    				       	 				{
    											$("#consoleAreaId").html(result);
    										}, "json");
    					}
					}
				);
				
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
								$form.attr('style', 'visibility:hidden');
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

function createFileFormValidation() 
{
    var x = document.forms["createNewPRBId"]["fileName"].value;
    if (x == null || x == "") 
    {
        alert("Name must be filled out");
        return false;
    }
    else
    {
        return true;	
    }
}

function propagationStopper(event)
{
	if (event.stopPropagation) 
	{
      event.stopPropagation();   //stop event propagation for Mozilla or Chrome
	} 
	else 
	{
      event.cancelBubble = true; // IE model
	}
}

function createNewPrb()
{
	var createNewPRBId = $("#createNewPRBId");
	if (createNewPRBId.css("display") == "none")
	{
		createNewPRBId.css("display", "block");
		createNewPRBId.animate({ 
			left: '50px',
	        height: '30px',
	        width: '120px'
	    });
	}
	else if(createNewPRBId.css("display") == "block")
	{
		createNewPRBId.animate({ 
			left: '0px',
	        height: '50px',
	        width: '15px'
	    });
		createNewPRBId.css("display", "none");
	}
}

function newDatFile(event, thisObj, prbFileName)
{
	if (event.stopPropagation) 
	{
      event.stopPropagation();   //stop event propagation for Mozilla or Chrome
	} 
	else 
	{
      event.cancelBubble = true; // IE model
	}
	
	if(thisObj.hasChildNodes())
	{
		while( thisObj.hasChildNodes() )
			{
				thisObj.removeChild(thisObj.children[0])
			}
	}
	else
	{
		$form = $('<form></form>');
		$form.attr('action', '/datagen/createNewFile');
		$form.attr('method', 'post');
		$form.attr('class','newDatFileCreator-form');
		$form.append('<input style="display:none" name="prbFileName"  value ="' + prbFileName + '">');
		$form.append('<input class="newDatFileCreator-input" name="fileName" onclick="propagationStopper(event)" placeholder="filename">');
		$form.keypress(function (e) {
			  if (e.which == 13) {
			    $form.submit();
			    return false;    //<---- Add this line
			  }
			});
		//var obj = document.getElementById("newDatFile" + prbFileName + "Id");
		//obj.appendChild($form);
		$(thisObj).append($form);
		$form.animate({ 
			left: '-90px'
	    });
	}
	
}

function redirectToDat()
{
	if(currentFile=="")
	{
		alert("Set current file by clicking on the list");
	}
	else
	{
		$form = $('<form></form>');
		$form.attr('action', '/codegen/datagen');
		$form.attr('method', 'get');
		$form.attr('style', 'visibility:hidden');
		$form.append('<input name="fileName" value="' + currentFile.split(".")[0] + '">');
		$form.appendTo('body').submit();
	}
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
	currentFile = this.fileName;
	var fileTree = fnamelist.fileTree;
    //var a = document.getElementById("currentFileName");
    //this is to add the sub division of dat files in tree structure
    if(this.showDat == 0)
    	{
	        var each = document.createElement("div");
	        //each.setAttribute("style", "position: relative; left:20px;"); 
	        each.setAttribute("class", "fileTree");
	        
	        for(var i=0; i <fileTree[this.fileName].length; i++)
	        	{
	        	    var dd = document.createElement("dd");
	        	    //Sdd.fileName = fileTree[this.fileName][i];
	        	    dd.setAttribute("fileName", fileTree[this.fileName][i]);
	        	    dd.setAttribute("parentFile", this.fileName);
	        	    //dd.setAttribute("onclick", "redirectToDat()");
	        	    dd.setAttribute("onclick", "datFileListOnclick(event, this)");
	        	    dd.setAttribute("class", "datList");
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
    
//    child = document.getElementById("prbFileList").children;
//    for (var i=0; i<child.length; i++)
//    	{
//    	    child[i].className = "prbList";
//    	}
    deselect = document.getElementsByClassName("selectedFile");
    for(var i=0; i<deselect.length; i++)
    	{
    	    if(deselect[i].tagName == "DD")
    	    	{
    	    		deselect[i].className = "datList";
    	    	}
    	    else if (deselect[i].tagName == "DT")
    	    	{
    	    		deselect[i].className = "prbList";
    	    	}
    	}
    this.setAttribute("class", "selectedFile");
    //a.innerHTML = "Current File Set to:" + currentFile;
    $.post("/codegen/load", { Data: currentFile},
				       	 				function(result)
				       	 				{
											$("#textAreaId").val(result);
    										//document.getElementById("textAreaId").innerHTML = result;
										}, "json");
    
    $.get("/codegen/downloadlink", {fileName: currentFile}, 
    		function(result)
    		{
    			document.getElementById("downloadLink").style.visibility = "hidden";
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
    
    //document.getElementById("executeBtnAreaId").style.display = "block";
    //document.getElementById("dataBtnAreaId").style.display = "None";
    document.getElementById("executeBtnAreaId").style.visibility = "visible";
    document.getElementById("dataBtnAreaId").style.visibility = "hidden";
}

//function datFileListOnclick()
//{
//	var a = document.getElementById("currentDatFileName");
//	currentDatFile = this.fileName;
//    a.innerHTML = "Current Data File Set to:" + currentDatFile;
//    $.post("/codegen/load", { Data: currentDatFile},
//				       	 				function(result)
//				       	 				{
//											$("#textAreaId").html(result);
//    										//document.getElementById("textAreaId").innerHTML = result;
//										}, "json");
//}

function datFileListOnclick(event, obj)
{
	//var a = document.getElementById("currentDatFileName");
	currentDatFile = obj.getAttribute('fileName');
	currentFile = obj.getAttribute('parentFile');
	//event.stopPropagation();  //stop event propagation for Mozilla or Chrome
	
	if (event.stopPropagation) 
		{
	      event.stopPropagation();   //stop event propagation for Mozilla or Chrome
		} 
	else 
		{
	      event.cancelBubble = true; // IE model
		}
//	child = document.getElementById("datFileList").children;
//    for (var i=0; i<child.length; i++)
//	{
//	    child[i].className = "datList";
//	}
//    this.setAttribute("class", "selectedFile");
    //a.innerHTML = "Current Data File Set to:" + currentDatFile;
    deselect = document.getElementsByClassName("selectedFile");
    for(var i=0; i<deselect.length; i++)
    	{
    	    if(deselect[i].tagName == "DD")
    	    	{
    	    		deselect[i].className = "datList";
    	    	}
    	    else if (deselect[i].tagName == "DT")
    	    	{
    	    		deselect[i].className = "prbList";
    	    	}
    	}
	obj.setAttribute("class", "selectedFile");
	
	if(currentFile == "")
		{
			alert("Prb file not selected");
		}
    $.post("/datagen/load", { Data: currentDatFile, PRB: currentFile.split(".")[0]},
				       	 				function(result)
				       	 				{
											$("#textAreaId").val(result);
    										//document.getElementById("textAreaId").innerHTML = result;
										}, "json");
    $.get("/datagen/downloadlink", {fileName: currentDatFile, PRB: currentFile.split(".")[0]}, 
    		function(result)
    		{
    			dwnld = document.getElementById("downloadLink");
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
    
//    document.getElementById("executeBtnAreaId").style.display = "None";
//    document.getElementById("dataBtnAreaId").style.display = "block";
    document.getElementById("executeBtnAreaId").style.visibility = "hidden";
    document.getElementById("dataBtnAreaId").style.visibility = "visible";
    
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
	          item.setAttribute("class", "prbList");
	          item.fileName = names[i]; //just to carry some data to the onclick function
	          
	          
	          
        	  if (names[i].split(".").pop()=="prb")
        		  {
        		      var newDatFileCreator = document.createElement("div");
    	              newDatFileCreator.setAttribute("id","newDatFile" + names[i].split(".")[0] + "Id");
    	              newDatFileCreator.setAttribute("class","newDatFileCreator");
    	              newDatFileCreator.setAttribute("onclick","newDatFile(event, this,'"+names[i].split(".")[0]+"')");
    	              
    	              item.onclick = prbFileListOnclick; //this function is to make it a method and prevents it from calling the fileListOnclick function itself
    	              //item.setAttribute("class", "listItems");
    	              item.appendChild(newDatFileCreator);
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

function setCSS()
{
	child = document.getElementById("prbFileList").children;
	for(var i=0; i<child.length; i++)
		{
		    if(child[i].innerHTML==currentFile)
		    	{
		    	    child[i].className = "selectedFile";
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
setCSS();
}