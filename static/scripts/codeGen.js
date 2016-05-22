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

try
{
	currentDatFile = fnamelist.currentDatFile;
}
catch(err)
{
        alert("Current File Error: "+ err.message); 
}

var syntaxCaller;
var syntaxCaretPosition=0;

$(document).ready(
		function()
			{
				
                if(currentFile != "")
                	{
	                    $.post("/codegen/load", { Data: currentFile},
		       	 				function(result)
		       	 				{
									$("#textAreaId").val(result);
								    $("#editableDivId").val(result);
								}, "json");
                	}
                $("#fileUploadId").change(
                		function()
                		{
                			this.submit();
                		}
                		);
                $("#editableDivId").on("paste", 
                		function(e)
                		{
                	        e.preventDefault();
                			var data = e.originalEvent.clipboardData.getData('Text');
                			data = data.split("\n");
    						var container = document.getElementById("editableDivId");
                			for(var i=0; i<data.length; i++)
                			{
                				var text = data[i]; 
        						var sec = document.createElement("span");
        						var br = document.createElement("br");
        						sec.setAttribute("spellcheck", "false");
        						sec.innerHTML = text;
        						
        						container.appendChild(sec);
        						container.appendChild(br);
                				
                			}
                			
                		}
                );
                $("#editableDivId").keydown(function(e) {
                    // trap the return key being pressed
                    if (e.keyCode === 13) {
                      // insert 2 br tags (if only one br tag is inserted the cursor won't go to the next line)
                      document.execCommand('insertHTML', false, '<br>');
                      // prevent the default behaviour of return key pressed
                      return false;
                    }
                  });
				$("#saveButtonId").click(
					function()
						{
						    if(currentFile!="")
						    	{
						    		$.post("/codegen/save",
	    				       			//{ Data: $("#textAreaId").val(), fileName: currentFile},codeRegenerator()
						    			//{ Data: codeRegenerator(), fileName: currentFile},
						    			{Data: textNodesUnder(document.getElementById("editableDivId")), 
							    		fileName: currentFile},
	    				       			function(result)
		    				       			{
		    				       				$("#consoleAreaId").val(result);
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
							var obj = document.getElementsByClassName("selectedFile")[0];
    						$.get("/codegen/execute", { fileName: currentFile, action: "executeForCode"},
    				       	 				function(result)
    				       	 				{
    											$("#consoleAreaId").val(result);
    											getPrbDownloadLink(currentFile, obj);
    										}, "json");
    					}
					}
				);

				$("#dataSaveButtonId").click(
					function()
						{
						    if(currentDatFile!="")
						    	{
						    		$.post("/datagen/save",
	    				       			//{ Data: $("#textAreaId").val(), fileName: currentDatFile},
						    			//{ Data: codeRegenerator(), fileName: currentDatFile},
						    			{Data: textNodesUnder(document.getElementById("editableDivId")), 
						    			fileName: currentDatFile},
	    				       			function(result)
		    				       			{
		    				       				$("#consoleAreaId").val(result);
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
							var obj = document.getElementsByClassName("selectedFile")[0];
    						$.get("/datagen/execute", { fileName: currentDatFile, action: "executeForData"},
    				       	 				function(result)
    				       	 				{
    											$("#consoleAreaId").val(result);
    											getDataDownloadLink(currentFile, currentDatFile, obj);
    										}, "json");
    					}
					}
				);
	   		}
	   		);

function getCaretCharacterOffsetWithin(element) {
    var caretOffset = 0;
    if (typeof window.getSelection != "undefined") {
        var range = window.getSelection().getRangeAt(0);
        var preCaretRange = range.cloneRange();
        preCaretRange.selectNodeContents(element);
        preCaretRange.setEnd(range.endContainer, range.endOffset);
        caretOffset = preCaretRange.toString().length;
    } else if (typeof document.selection != "undefined" && document.selection.type != "Control") {
        var textRange = document.selection.createRange();
        var preCaretTextRange = document.body.createTextRange();
        preCaretTextRange.moveToElementText(element);
        preCaretTextRange.setEndPoint("EndToEnd", textRange);
        caretOffset = preCaretTextRange.text.length;
    }
    return caretOffset;
}

function getCaretPos() {
    var el = document.getElementById("editableDivId");
    var pos = getCaretCharacterOffsetWithin(el);
    console.log( "Caret position: " + pos);
    return pos;
}

//function overwriteDefault()
//{
//	if (e.keyCode === 13) 
//	{
//	      // insert 2 br tags (if only one br tag is inserted the cursor won't go to the next line)
//	      document.execCommand('insertHTML', false, '<br><br>');
//	      // prevent the default behaviour of return key pressed
//	      return false;
//	}
//}

function textNodesUnder(node){
	  var all = "";
	  for (node=node.firstChild;node;node=node.nextSibling)
	  {
			if (node.nodeType==3) 
			{
				var strVal = node.textContent;
				all = all + strVal;
//				if(node.parentNode.nodeName == "DIV" && node.parentNode.contentEditable==true )
//				{
//					all = all + "\n";
//				}
			}
			else if(node.nodeName == "BR")
			{
				all = all + "\n";
			}
			else 
			{
				all = all.concat(textNodesUnder(node));
			}
	  }
	  return all;
	}

function childFinder(division)
{
	var node;
	var code = "";
	for(var i=0; i<division.childElementCount; i++)
	{
		node = division.childNodes[i];
        console.log("this ->" + node.innerHTML);
		switch(node.tagName)
		{
			case "FONT":
				code = code + node.innerHTML;
				break;
			case "SPAN":
				code = code + node.innerHTML;
				break;
			case "BR":
				code = code + "\n";
				break;
			case "DIV":
				var res = childFinder(node);
				code = "\n" + code + node.innerHTML;
				break;
		}
	}
	return code;
}

var code;

function codeRegenerator()
{
	var area = document.getElementById("editableDivId");
	var node;
	//var code = "";
	for(var i=0; i<area.childElementCount; i++)
	{
		node = area.childNodes[i];
		switch(node.tagName)
		{
			case "SPAN":
				code = code + node.innerHTML;
				break;
			case "BR":
				code = code + "\n";
				break;
			case "DIV":
				var res = childFinder(node);
				code = "\n" + code + node.innerHTML;
				break;
		}
	}
	return code;
}

function cleanEditor()
{
	var container = document.getElementById("editableDivId");
	while (container.firstChild) 
	{
		container.removeChild(container.firstChild);
	}
}

function colorCodeGenerator(code, text)
{
	switch(code)
	{
		case "endline":
			var sec = document.createElement("br");
			break;
			
		default:
			var sec = document.createElement("span");
			sec.setAttribute("class", code);
			sec.setAttribute("spellcheck", "false");
			sec.innerHTML = text;
			break;
	}
	return sec;
}

function syntaxPrep(syntax)
{
	cleanEditor();
	var container = document.getElementById("editableDivId");
	for (count in syntax)
	{
		var line = syntax[count];
		for(keys in line)
		{
			var sec = colorCodeGenerator(keys, line[keys]);
			container.appendChild(sec);
		}
	}
}

function syntaxFetch()
{
//	$.get("/codegen/load", { Code: codeRegenerator()},
//			function(result)
//			{
//				syntaxPrep(result);
//			}, "json");
	var container = document.getElementById("editableDivId");
	syntaxCaretPosition = $('#editableDivId').caret('pos');
	$.get("/codegen/load", { Code: textNodesUnder(container)},
				function(result)
				{
					syntaxPrep(result);
					$('#editableDivId').caret('pos', syntaxCaretPosition);
				}, "json");
}

function syntaxCall()
{
	clearTimeout(syntaxCaller);
	syntaxCaller = setTimeout(syntaxFetch, 3000);
}

function createFileFormValidation() 
{
	var x = document.forms["createNewPRBId"]["fileName"].value;
	if (x == null || x == "") 
	{
	    alert("Select a file");
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

function setFormPrbAndDat(id)
{
	var createNewDatId = document.getElementById(id);
	var inp1 = document.createElement("input");
	inp1.name = "currentFile";
	inp1.value = currentFile;
	inp1.setAttribute("class", "displayNone");
	
	createNewDatId.appendChild(inp1);
	var x = document.forms[id]["fileName"].value;
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
	
	if(thisObj.childElementCount>0)
	{
		while( thisObj.childElementCount>0 )
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
			    return false;
			  }
			});
		$(thisObj).append($form);
		$form.animate({ 
			left: '90px'
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
		post("/codegen/save", { Data: $("#textAreaId").val(), fileName: currentFile} 
		);
	}

function loadTextArea() 
	{
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

function datFileListOnclick(event, obj)
{
	currentDatFile = obj.getAttribute('fileName');
	currentFile = obj.getAttribute('parentFile');
	
	if (event.stopPropagation) 
		{
	      event.stopPropagation();   //stop event propagation for Mozilla or Chrome
		} 
	else 
		{
	      event.cancelBubble = true; // IE model
		}
 
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
	obj.setAttribute("class", "selectedFile datEmWidth");
	
	if(currentFile == "")
		{
			alert("Prb file not selected");
		}
	document.getElementById("executeBtnAreaId").style.visibility = "hidden";
    document.getElementById("dataBtnAreaId").style.visibility = "visible";
    $.post("/datagen/load", { Data: currentDatFile, PRB: currentFile.split(".")[0]},
				       	 				function(result)
				       	 				{
    										syntaxPrep(result);
											//$("#textAreaId").val(result);
										}, "json");
}

function deleteBtn(event, currentFile, currentDatFile)
{
	propagationStopper(event);
	$.get("/datagen/delete", {fileName: currentDatFile, prbFileName: currentFile.split(".")[0]},
			function(result)
			{ 
				if(result == "success")
				{
					window.location.reload();
				}
			});
}

function addDatfileDeleteBtn(currentFile, currentDatFile, obj)
{
	var del = document.createElement("div");
	del.setAttribute("onclick", "deleteBtn(event, '" + currentFile + "', '" + currentDatFile + "')"); 
    		
	del.setAttribute("class", "deleteSign");
	obj.appendChild(del);
	
}

function addDownloadBtn(obj, link)
{
	var dwnld = document.createElement("div");
	
	for(var i=0; i<obj.childElementCount; i++)
	{
		if(obj.children[i].className == 'noDownload' | obj.children[i].className == 'downloadSign')
		{
			obj.removeChild(obj.children[i]);
		}
	}
	
	if(link == null)
	{
		dwnld.setAttribute("class", "noDownload");
	}
	else
	{
		dwnld.setAttribute("onclick", "location.href='" + link + "'");
		dwnld.setAttribute("class", "downloadSign");
	}
	$(obj).prepend(dwnld);
}

function getDataDownloadLink(currentFile, currentDatFile, obj)
{
	var addBtn = function(result){ addDownloadBtn(obj, result);}
    $.get("/datagen/downloadlink", {fileName: currentDatFile, PRB: currentFile.split(".")[0]}, 
    		function(result){ addBtn(result);}	
    		, "json");
}

function prbFileListOnclick()
{
	currentFile = this.fileName;
	var fileTree = fnamelist.fileTree;
    //this is to add the sub division of dat files in tree structure
    if(this.showDat == 0)
    	{
	        var each = document.createElement("div");
	        each.setAttribute("class", "fileTree");
	        
	        var newDatFileCreator = document.createElement("div");
            newDatFileCreator.setAttribute("id","newDatFile" + currentFile.split(".")[0] + "Id");
            newDatFileCreator.innerHTML = "+new .dat file"; //newDatFileCreator
            newDatFileCreator.setAttribute("class","newDatFileCreator");
            newDatFileCreator.setAttribute("onclick","newDatFile(event, this,'" + currentFile + "')");
	        each.appendChild(newDatFileCreator);
	        
            for(var i=0; i <fileTree[this.fileName].length; i++)
	        	{
	        	    var dd = document.createElement("dd");
	        	    getDataDownloadLink(this.fileName, fileTree[this.fileName][i], dd);
	        	    addDatfileDeleteBtn(this.fileName, fileTree[this.fileName][i], dd);
	        	    dd.setAttribute("fileName", fileTree[this.fileName][i]);
	        	    dd.setAttribute("parentFile", this.fileName);
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
    $.post("/codegen/load", { Data: currentFile},
				       	 				function(result)
				       	 				{
    										syntaxPrep(result);
										}, "json");
    
    document.getElementById("executeBtnAreaId").style.visibility = "visible";
    document.getElementById("dataBtnAreaId").style.visibility = "hidden";

}

function setAlreadySelectedFiles()
{
	if(currentFile!=null | currentFile.length>0)
	{
		var w = document.getElementsByClassName("prbList");
		for(var i=0; i<w.length; i++)
		{
			if(w[i].fileName == currentFile)
			{
				w[i].click();
				if(currentDatFile!=null | currentDatFile.length>0)
				{
					v = document.getElementsByClassName("datList");
					for(var j=0; j<v.length; j++)
					{
						if($(v[j]).attr("fileName") == currentDatFile)
						{
							v[j].click();
						}
					}
				}
			}
		}
	}
}

function deletePrbBtn(event, Filename)
{
	propagationStopper(event);
	$.get("/codegen/delete", {fileName: Filename},
			function(result)
			{ 
				console.log("res: " + result);
				if(result == "success")
				{
					console.log("suc: " + result);
					window.location.replace("/codegen/");
				}
			});
}

function addPrbfileDeleteBtn(Filename, obj)
{
	var del = document.createElement("div");
	del.setAttribute("onclick", "deletePrbBtn(event, '" + Filename + "')"); 
	del.setAttribute("class", "deleteSign");
	obj.appendChild(del);
}

function addPrbDownloadBtn(obj, link)
{
	var dwnld = document.createElement("div");
	
	for(var i=0; i<obj.childElementCount; i++)
	{
		if(obj.children[i].className == 'noDownload' | obj.children[i].className == 'downloadSign')
		{
			obj.removeChild(obj.children[i]);
		}
	}
	
	if(link == null)
	{
		dwnld.setAttribute("class", "noDownload");
	}
	else
	{
		dwnld.setAttribute("onclick", "location.href='" + link + "'");
		dwnld.setAttribute("class", "downloadSign");
	}
	$(obj).prepend(dwnld);
	//obj.appendChild(dwnld);
}

function getPrbDownloadLink(Filename, obj)
{
	var addBtn = function(result){ addDownloadBtn(obj, result);}
    $.get("/codegen/downloadlink", {fileName: Filename}, 
    		function(result){ addBtn(result);}	
    		, "json");
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
      item.fileName = names[i];         
      
	  if (names[i].split(".").pop()=="prb")
	  {
		  	var prbText = document.createElement("span");
			prbText.setAttribute("class", "prbList-filename");
			prbText.innerHTML = names[i];
		  	getPrbDownloadLink(names[i], item);
		  	addPrbfileDeleteBtn(names[i], item);
			item.onclick = prbFileListOnclick;
			
			item.appendChild(prbText);
			prbFileList.appendChild(item);
	  }
	  else
	  {
		  	console.log("Non Prb file type received");
	  }
    }
    setAlreadySelectedFiles();
}

function setCSS()
{
	if (document.getElementsByClassName("selectedFile").length == 0)
	{
		document.getElementById("executeBtnAreaId").style.visibility = "visible";
	    document.getElementById("dataBtnAreaId").style.visibility = "hidden";
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
