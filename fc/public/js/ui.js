function insert(text)
{
    var textarea=document.forms.postform.message;
    if(textarea)
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
}

function highlight(post)
{
    var cells=document.getElementsByTagName("td");
    for(var i=0;i<cells.length;i++) if(cells[i].className=="highlight") cells[i].className="reply";

    var reply=document.getElementById("reply"+post);
    if(reply)
    {
        reply.className="highlight";
/*      var match=/^([^#]*)/.exec(document.location.toString());
        document.location=match[1]+"#"+post;*/
        return false;
    }

    return true;
}



function showDeleteBoxes() 
{
    var chboxes = getElementsByClass('delete');
    for(i=0; i<chboxes.length; i++) 
    {
        if(chboxes[i].style.display == 'none') 
        {
            chboxes[i].style.display = 'inline';
        }
        else
        {
            chboxes[i].style.display = 'none';
        }
    }
}

var g_objReplyForm = null; // "Global" variable
function getReplyForm(iThreadId)
{
    if (!g_objReplyForm)
    {
        g_objReplyForm = createElementEx('form',{
            'action': ('/' + iThreadId),
            'method': 'post',
            'enctype': 'multipart/form-data'
        });
        g_objReplyForm.id = 'x_replyform';
        g_objReplyForm.appendChild(createElementEx('input', {'name': 'task', 'value': 'post', 'type': 'hidden'}));
        g_objReplyForm.appendChild(createElementEx('input', {'name': 'akane', 'type': 'hidden'}));
        g_objReplyForm.appendChild(createElementEx('input', {'name': 'gb2', 'value': 'board', 'type': 'hidden'}));
        g_objReplyForm.appendChild(createElementEx('input', {'name': 'title', 'value': '', 'type': 'hidden'}));
        g_objReplyForm.appendChild(createElementEx('textarea', {'id': 'x_replyform_text', 'name': 'message', 'rows': '5', 'cols': '40'}));
        var objBottomDiv = document.createElement('div');
        var objFileLabel = createElementEx('label', {'for': 'x_replyform_file', 'title': 'File'});
        objFileLabel.appendChild(document.createTextNode('File: '));
        objFileLabel.appendChild(createElementEx('input', {'id': 'x_replyform_file', 'name': 'file', 'size': '20', 'type': 'file'}));
        var objSageLabel = createElementEx('label', {'for': 'x_replyform_sage', 'title': 'sage'});
        objSageLabel.appendChild(createElementEx('input', {'id': 'x_replyform_sage', 'type': 'checkbox', 'name': 'sage'}));
        objSageLabel.appendChild(document.createTextNode('sage'));
        objBottomDiv.appendChild(objFileLabel);
        objBottomDiv.appendChild(objSageLabel);
        objBottomDiv.appendChild(createElementEx('input', {'type': 'submit', 'value': 'Post'}));
        var objCloseBtn = document.createElement('button');
        objCloseBtn.addEventListener('click', hideQuickReplyForm, true);
        if (window.opera)
        {
            objCloseBtn.onclick = hideQuickReplyForm;
        }
        objCloseBtn.appendChild(document.createTextNode('Close'));
        objBottomDiv.appendChild(objCloseBtn);
        g_objReplyForm.appendChild(objBottomDiv);
    }
    else
    {
        var objInputParent = document.getElementById('x_replyform_iparent');
        if (!objInputParent)
        {
            return null;
        }
        objInputParent.value = iThreadId;
    }
    return g_objReplyForm;
}
function doQuickReplyForm(objEvent,iThreadId,iPostId)
{
    if (!iThreadId)
    {
        return;
    }
    var objRText = document.getElementById('x_replyform_text');
    if (!objRText || !objEvent.shiftKey)
    {
        var objPost = document.getElementById('quickReplyNode'+iPostId);
        var objReplyForm;
        if (!g_objReplyForm) 
            objReplyForm = getReplyForm(iThreadId);
        else
            objReplyForm = g_objReplyForm;
        objReplyForm.action = '/'+iThreadId;
        objReplyForm.style.display = 'block';
        objPost.parentNode.insertBefore(objReplyForm, objPost.nextSibling);
        var objRPass = document.getElementById('x_replyform_pass');
        if (objRPass)
        {
            try
            {
                var objRealPass = document.evaluate("//tr[@id='trpassword']/td/input[@name='password']", document,
                                              null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (objRealPass)
                {
                    if (objRPass.value == '')
                    {
                        objRPass.value = objRealPass.value;
                    }
                }
            }
            catch(e)
            {
                return;
            }
        }
    }
    if (!objRText)
    {
        objRText = document.getElementById('x_replyform_text');
    }
    if (objRText && iPostId)
    {
        objRText = document.getElementById('x_replyform_text');
        objRText.value += '>>' + iPostId + '\n';
    }
    objEvent.preventDefault();
}
function hideQuickReplyForm(objEvent)
{
    try
    {
        if (!g_objReplyForm)
        {
            return;
        }
        var objTemp = document.getElementById('x_replyform_text');
        if (objTemp)
        {
            objTemp.value = '';
        }
        g_objReplyForm.style.display = 'none';
    }
    catch(e)
    { ; }
    objEvent.preventDefault();
}
function getFullText(event, thread, post) {
    $.get('/ajax/getPost/' + post, {}, function(response){
      $('#postBQId' + post).html(response);
    });
}
window.onload=function(e)
{
    var match;

    if(match=/#i([0-9]+)/.exec(document.location.toString()))
    if(!document.forms.postform.message.value)
    insert(">>"+match[1]);

    if(match=/#([0-9]+)/.exec(document.location.toString()))
    highlight(match[1]);
}  
