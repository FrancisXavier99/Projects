
//--------------------To validate the input for integer only---------------------------------------------------------------------------------------------
function validateCost()
{

//    var z = document.forms["myForm"]["num"].value;
    var z = document.getElementById('subscrption_amt')
    if (isNaN(z))
//    	 if((!isNaN(z) || z < 1 || z > 10))
        {
        alert("Please only enter numeric characters only for Book cost!")
        }
    
//    		var charCode = (z.which) ? z.which : z.keyCode
//            if (charCode > 31 && (charCode < 48 || charCode > 57))
//               return false;

}


//----------------------To set Default Value for the selection field-------------------------------------------------------------------------------------------

//function set_default_category()
//{
////	var a = document.getElementById('gender')
//	var val = 'Cake';
//    $("#category_id").val(val);
//}


$(function() {
    var temp="Cake"; 
    $("#category_id").val(temp);
});

//<select name="MySelect" id="MySelect">
//    <option value="a">a</option>
//    <option value="b">b</option>
//    <option value="c">c</option>
//</select>