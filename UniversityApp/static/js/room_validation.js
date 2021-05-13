function validateroom()
{	
	var class_no = document.getElementById("classno").value;
	
	if(class_no.length<3 || class_no.length>3)
	{
		document.getElementById("classno_valid").innerHTML = "Invalid Class room number";
		document.getElementById("cleanliness_button").disabled = true;
		return false;
	}
	else
	{
		document.getElementById("classno_valid").innerHTML = "";
		document.getElementById("cleanliness_button").disabled = false;
		return true;
	}
}