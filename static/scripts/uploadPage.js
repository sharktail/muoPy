

        var arg = "{{arg}}";
		var flist = "{{arg2}}";
		
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
	                    a.innerHTML = "Current File Set to:" + currentFile;
	                    document.getElementById("downloadLink").href = fnamelist.downloadLink;
	                    
    					$("#saveButtonId").click(
    						function()
    							{
    							    if(currentFile=="")
    							    	{
    							    		alert("Set current file by clicking on the list");
    							    	}
    							    else
    							    {
	        							$.post("/upload/save",
	        				       			{ Data: $("#textAreaId").val(), fileName: currentFile} 
	        				      			);
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
	        						$.post("/upload/execute", { fileName: currentFile},
	        				       	 				function(result)
	        				       	 				{
	        											$("#consoleAreaId").html(result);
	        										}, "json");
	        					}
    						}
    					);
			   		}
			   		);
		
		function loadTextArea() 
			{
			   document.getElementById("textAreaId").innerHTML = parsedText;
			}
	    function fileListOnclick()
	    {
	        var a = document.getElementById("currentFileName");
	        currentFile = this.fileName;
	        a.innerHTML = "Current File Set to:" + currentFile;
	        $.post("/upload/load", { Data: currentFile},
        				       	 				function(result)
        				       	 				{
        											$("#textAreaId").html(result);
        										}, "json");
	        
	    }
        function loadListOfFiles()
            {
                var names = fnamelist.fileNames;
                var list = document.getElementById("fileList");
                
                for(var i=0; i<names.length; i++)
                    { 
                      var item = document.createElement('li');
                      item.fileName = names[i];
                      item.onclick = fileListOnclick; //this function is to make it a method and prvents it from calling the fileListOnclick function itself
                      item.appendChild(document.createTextNode(names[i]));
                      list.appendChild(item);
                      
                    }
            }
		window.onload = function(){
		loadTextArea();
		loadListOfFiles();
		}