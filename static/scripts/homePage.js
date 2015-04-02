
function myFunction() 
{
   var txt = "Paragraph changed" + ": " + st.lastname;
   document.getElementById("demo").innerHTML = txt;
}

function toggle_visibility(showId, hideId) 
{
	var show = document.getElementById(showId);
	var hide = document.getElementById(hideId);
	show.style.display = 'block';
	hide.style.display = 'none';
}
