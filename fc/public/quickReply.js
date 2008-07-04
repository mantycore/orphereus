originalPostAction = ''
function showNewThreadForm(event)
{
	var form = document.getElementById('postFormDiv');
	var div = document.getElementById('newThreadPlaceholder');
	form.parentNode.removeChild(form);
	form.action = originalPostAction;
	div.appendChild(form);
	event.preventDefault();
}
function showReplyForm(event,pid)
{
	var form = document.getElementById('postFormDiv');
	var textarea = document.getElementById('replyText');
	var QRNode = document.getElementById('quickReplyNode'+pid);
	form.parentNode.removeChild(form);
	if (!originalPostAction)
	{
		originalPostAction = form.action;
	}
	form.action = '/'+pid+'/';
	addTextToTextarea(textarea,"&gt;&gt;"+pid);
	QRNode.parentNode.insertBefore(form, QRNode.nextSibling);
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