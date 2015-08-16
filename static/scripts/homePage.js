function toggleClass(idOne, idTwo)
{
	var idOne = document.getElementById(idOne);
	var idTwo = document.getElementById(idTwo);
	var cl = idOne.className;
	idOne.className = idTwo.className;
	idTwo.className = cl;
}


function toggle_visibility(showId, hideId) 
{
	var show = document.getElementById(showId);
	var hide = document.getElementById(hideId);
	show.style.display = 'block';
	hide.style.display = 'none';
	
	toggleClass("signInBtnId", "signUpBtnId");
}