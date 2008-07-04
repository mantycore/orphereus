originalPostAction = ''
function showNewThreadForm(event)
{
	var formDiv = document.getElementById('postFormDiv');
	var form = document.getElementById('postform');
	var div = document.getElementById('newThreadPlaceholder');
	formDiv = formDiv.parentNode.removeChild(formDiv);
	if (originalPostAction)
		form.action = originalPostAction;
	div.appendChild(formDiv);
        formDiv.style.display = 'block';
        formDiv.childNodes[1].style.display = 'block';
        if (formDiv.childNodes[1].childNodes[0].style)
	        formDiv.childNodes[1].childNodes[0].style.display = 'block';
        form.style.display = 'block';
	event.preventDefault();
}
function showReplyForm(event,pid)
{
	var formDiv = document.getElementById('postFormDiv');
	var textarea = document.getElementById('replyText');
	var form = document.getElementById('postform');
	var QRNode = document.getElementById('quickReplyNode'+pid);
	formDiv = formDiv.parentNode.removeChild(formDiv);
	if (!originalPostAction)
	{
		originalPostAction = form.action;
	}
	form.action = '/'+pid+'/';
	QRNode.parentNode.insertBefore(formDiv, QRNode.nextSibling);
        formDiv.style.display = 'block';
        formDiv.childNodes[1].style.display = 'block';
        if (formDiv.childNodes[1].childNodes[0].style)
	        formDiv.childNodes[1].childNodes[0].style.display = 'block';
        form.style.display = 'block';
	event.preventDefault();
}
function addTextToTextarea(textarea,text)
{
	if(textarea.createTextRange && textarea.caretPos) // IE
	{
		var caretPos=textarea.caretPos;
		caretPos.text=caretPos.text.charAt(caretPos.text.length-1)==" "?text+" ":text;
	}
	else if(textarea.setSelectionRange) // Firefox
	{
		var start=textarea.selectionStart;
		var end=textarea.selectionEnd;
		textarea.value=textarea.value.substr(0,start)+text+textarea.value.substr(end);
		textarea.setSelectionRange(start+text.length,start+text.length);
	}
	else
	{
		textarea.value+=text+" ";
	}
	textarea.focus();
}
