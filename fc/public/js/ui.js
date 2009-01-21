function popup_posts(options){
  if(!options) options = {}
  popup_posts.helper = $(document.createElement('blockquote'));
  popup_posts.helper.css('position','absolute');
  popup_posts.helper.addClass("popup_post");
  popup_posts.helper.hide();
  popup_posts.cache = {}
  $(document.body).append(popup_posts.helper)
  var show_it = function(html){
    popup_posts.helper.html('<table>' + html + '</table>')
    popup_posts.helper.find(".reply").removeClass("reply")
    popup_posts.helper.find(".highlight").removeClass("highlight")
    popup_posts.helper.addClass("highlight reply")
    var left = popup_posts.ui.offset().left + popup_posts.ui.width()
    var top  = popup_posts.ui.offset().top - popup_posts.helper.height() - 2
    
    popup_posts.helper.css('left',left).css('top',top).show()
    // if(popup_posts.helper.offset().top < $().scrollTop()) popup_posts.helper.css('top',$().scrollTop())
    if((popup_posts.helper.width() < 200) || (popup_posts.helper.offset().left + popup_posts.helper.width() > $(window).width() - 20)){
      popup_posts.helper.css('left', 10);
      popup_posts.helper.css('top',popup_posts.ui.offset().top - popup_posts.helper.height() - 4);
    }
    var under_link = popup_posts.ui.offset().top + popup_posts.ui.height()
    if((popup_posts.helper.offset().top < $().scrollTop()) &&
     (under_link + popup_posts.helper.height() <  $().scrollTop() + $(window).height())) popup_posts.helper.css('top',under_link + 10)
  }
  var hide_it = function(){
    popup_posts.helper.hide()
  }
  var load_on = function(e){
    e.attr('old_html',e.html())
    e.html("loading...")
  }
  var load_off = function(e){
    e.html(e.attr('old_html'))
  }
  var hover_it = function(ev){
    var m = $(this).html().match(/\d+$/)
    if (!m) return false;
    popup_posts.ev = ev
    popup_posts.ui = $(this)
    var content = $("#quickReplyNode"+m[0])
    if (content.size()){
      if (content[0].tagName == 'BLOCKQUOTE')
        show_it(content.parent().html().split(/<table|<TABLE/)[0])
      else
        show_it(content.html())
    }else if(popup_posts.cache[m[0]] == 404){
      $(this).html("Post not found");
    }else if (popup_posts.cache[m[0]]){
      show_it(popup_posts.cache[m[0]]);
    }else if(options.ajax){
        var e = $(this)
        load_on(e)
        $.ajax({type: 'get', url: "/ajax/getRenderedPost/"+m[0], success: function(html){
          load_off(e)
          html = html.replace(/<\/?table[^>]*>/,'')
          show_it(html);
          popup_posts.cache[m[0]] = html;
        }, error: function(a,b) {popup_posts.cache[m[0]] = 404; e.html("Post not found") } });
    }
  }
  
  $("blockquote a").filter(function(){
    return $(this).attr('href').match(/^\/-?\d+(\#i\d+)?$/)
  }).hover(hover_it,hide_it)
  
  popup_posts.repair = function(links){
    links.filter(function(){
      return $(this).attr('href').match(/^\/-?\d+(\#i\d+)?$/)
    }).hover(hover_it,hide_it)    
  }
}

function insert(text,notFocus)
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
        if (!notFocus)
        {
        	textarea.focus();
        }
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
        g_objReplyForm.appendChild(createElementEx('input', {'name': 'title', 'value': '', 'type': 'hidden'}));
        
        var origForm = document.getElementById('postform');
        g_objReplyForm.appendChild(createElementEx('input', {'name': 'tagLine', 'value': origForm.tagLine.value, 'type': 'hidden'}));
        g_objReplyForm.appendChild(createElementEx('input', {'name': 'curPage', 'value': origForm.curPage.value, 'type': 'hidden'}));

        g_objReplyForm.appendChild(createElementEx('textarea', {'id': 'x_replyform_text', 'name': 'message', 'rows': '5', 'cols': '40'}));
        var objBottomDiv = document.createElement('div');
        
        var objFileLabel = createElementEx('label', {'for': 'x_replyform_file', 'title': 'File'});
        objFileLabel.appendChild(document.createTextNode('File: '));
        objFileLabel.appendChild(createElementEx('input', {'id': 'x_replyform_file', 'name': 'file', 'size': '20', 'type': 'file'}));
        
        var objSageLabel = createElementEx('label', {'for': 'x_replyform_sage', 'title': 'sage'});
        objSageLabel.appendChild(createElementEx('input', {'id': 'x_replyform_sage', 'type': 'checkbox', 'name': 'sage'}));
        objSageLabel.appendChild(document.createTextNode('sage'));
        
        var objGotoLabel = createElementEx('label', {'for': 'x_replyform_goto', 'title': 'goto'});
        var GotoSelect = createElementEx('select', {'name': 'goto', 'id': 'x_replyform_goto'});
        for (i=0;i<origForm.goto.options.length;i++)
        {
        	var opt = createElementEx('option', {'value':origForm.goto.options[i].value});
        	opt.appendChild(document.createTextNode(origForm.goto.options[i].text));
        	if (origForm.goto.options[i].selected)
			opt.selected = true;
        	GotoSelect.appendChild(opt);
        }
        objGotoLabel.appendChild(document.createTextNode('Go to'));
        objGotoLabel.appendChild(GotoSelect);        
        
        objBottomDiv.appendChild(objFileLabel);
        objBottomDiv.appendChild(objSageLabel);
        objBottomDiv.appendChild(objGotoLabel);
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
function getFullText(event, thread, post)
{
    var bq = document.getElementById('postBQId' + post);
    if (!bq) bq = document.getElementById('quickReplyNode' + post);
    $("a.expandPost[href=/" + thread + "#i" + post + "]").html('loading…')
    $.get('/ajax/getPost/' + post, {}, function(response)
    {
      $(bq).html(response);
	  popup_posts.repair($(bq).find("a"))
    });	
    event.preventDefault();	
}
function userFiltersAdd(event)
{
	if ($('#newFilterInput').get()[0].value)
	{
		$.get('/ajax/addUserFilter/' + $('#newFilterInput').get()[0].value, {}, function(response)
		{
			$(response).insertBefore('#newFilterTR')
		});
	}
	event.preventDefault();
}
function userFiltersEdit(event,fid)
{
	$.get('/ajax/editUserFilter/' + fid + '/' + $('#filterId' + fid + 'Input').get()[0].value, {}, function(response)
	{
		$('#filterId' + fid + 'Input').get()[0].value = response
	});
	event.preventDefault();
}
function userFiltersDelete(event,fid)
{
	$.get('/ajax/deleteUserFilter/' + fid, {}, function(response)
	{
		$('#filterId' + fid).remove()
	});
	event.preventDefault();
}
window.onload=function(e)
{
    var match;
    if(match=/#i([0-9]+)/.exec(document.location.toString()))
    {
        if(!document.forms.postform.message.value)
            insert(">>"+match[1],1);
        highlight(match[1]);
    }
}  
