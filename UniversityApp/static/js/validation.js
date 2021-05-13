function validatepass()
{	
	var pass = document.getElementById("pass").value;
	
	if(pass.length<6)
	{
		document.getElementById("passcheck").innerHTML = "Password must be atleast 6 characters long.";
		document.getElementById("register_button").disabled = true;
		return false;
	}
	else
	{
		document.getElementById("passcheck").innerHTML = "";
		return true;
	}
}

function validatecpass()
{	
	var pass = document.getElementById("pass").value;
	var cpass = document.getElementById("confirmpass").value;
	
	if(pass != cpass)
	{
		document.getElementById("cpasscheck").innerHTML = "Password and Confirm Password do not match.";
		document.getElementById("register_button").disabled = true;
		return false;
	}
	else
	{
		document.getElementById("cpasscheck").innerHTML = "";
		document.getElementById("register_button").disabled = false;
		return true;
	}
}

function validateemail()
{
	var email_id = document.getElementById("email").value;
	var pattern= /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
	
	if(email_id.match(pattern))
	{
		document.getElementById("emailcheck").innerHTML = "";
		document.getElementById("register_button").disabled = false;
		return true;
	}
	else
	{
		document.getElementById("emailcheck").innerHTML = "Invalid Email ID.";
		document.getElementById("register_button").disabled = true;
		return false;
	}
}

function validateprn()
{	
	var pass = document.getElementById("prn").value;
	
	if(pass.length==11)
	{
		document.getElementById("prncheck").innerHTML = "";
		document.getElementById("register_button").disabled = false;
		return true;
	}
	else
	{		
		document.getElementById("prncheck").innerHTML = "PRN no. is incorrect";
		document.getElementById("register_button").disabled = true;
		return false;
	}
}
