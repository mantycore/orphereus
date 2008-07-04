  function addGlobalStyle(strCSS) {
    var objHead = document.getElementsByTagName('head')[0];
    if (!objHead) { return; }
    var objStyle = document.createElement('style');
    objStyle.type = 'text/css';
    objStyle.appendChild(document.createTextNode(strCSS));
    objHead.appendChild(objStyle);
  }

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
/*		var match=/^([^#]*)/.exec(document.location.toString());
		document.location=match[1]+"#"+post;*/
		return false;
	}

	return true;
}

function getElementsByClass( searchClass, domNode, tagName) {
	if (domNode == null) domNode = document;
	if (tagName == null) tagName = '*';
	var el = new Array();
	var tags = domNode.getElementsByTagName(tagName);
	var tcl = " "+searchClass+" ";
	for(i=0,j=0; i<tags.length; i++) {
		var test = " " + tags[i].className + " ";
		if (test.indexOf(tcl) != -1)
		el[j++] = tags[i];
	}
	return el;
}

function showDeleteBoxes() {
	var chboxes = getElementsByClass('delete');
	for(i=0; i<chboxes.length; i++) {
		if(chboxes[i].style.display == 'none') {
			chboxes[i].style.display = 'inline';
		} else {
			chboxes[i].style.display = 'none';
		}
	}
}

  function createElementEx(strTagName, arrAttrs, arrChildren) {
    var objElement = document.createElement(strTagName);
    for (strIndex in arrAttrs) {
      objElement.setAttribute(strIndex, arrAttrs[strIndex]);
    }
    for (strIndex in arrChildren) {
      objElement.appendChild(arrChildren[strIndex]);
    }
    return objElement;
  }

  var g_objReplyForm = null; // "Global" variable
  function getReplyForm(iThreadId) {
    if (!g_objReplyForm) {
      g_objReplyForm = createElementEx('form', {
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
      if (window.opera) { objCloseBtn.onclick = hideQuickReplyForm; }
      objCloseBtn.appendChild(document.createTextNode('\u2716'));
      objBottomDiv.appendChild(objCloseBtn);
      g_objReplyForm.appendChild(objBottomDiv);
    } else {
      var objInputParent = document.getElementById('x_replyform_iparent');
      if (!objInputParent) { return null; } // Someone touched our document. Bail out.
      objInputParent.value = iThreadId;
    }
    return g_objReplyForm;
  }


  function doQuickReplyForm(objEvent,iThreadId,iPostId) {
    if (!iThreadId) { return; }
    var objRText = document.getElementById('x_replyform_text');
    if (!objRText || !objEvent.shiftKey) {
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
      if (objRPass) {
        try {
          var objRealPass = document.evaluate("//tr[@id='trpassword']/td/input[@name='password']", document,
                                              null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
          if (objRealPass) {
            if (objRPass.value == '') {
              objRPass.value = objRealPass.value;
            } /* else if (objRealPass.value != objRPass.value) {
              objRealPass.value = objRPass.value; // Should we?
            } */
          }
        } catch(e) { window.alert(e); }
      }
    }
    if (!objRText) { objRText = document.getElementById('x_replyform_text'); }
    if (objRText && iPostId) {
	  objRText = document.getElementById('x_replyform_text');
//      if (objRText.value.match(/^>>\d+\s*$/) && !objEvent.shiftKey) { objRText.value = ''; }
      objRText.value += '>>' + iPostId + '\n';
    }
    objEvent.preventDefault();
  }

  function hideQuickReplyForm(objEvent) {
    try {
      if (!g_objReplyForm) { return; }
      var objTemp = document.getElementById('x_replyform_text');
      if (objTemp) { objTemp.value = ''; }
      g_objReplyForm.style.display = 'none';
    } catch(e) { ; }
    objEvent.preventDefault();
  }
  
  addGlobalStyle(
    '.postername, .postertrip, .commentpostername { display: inline; visibility: visible; font-weight: bold; color: #339; } \
    .postertrip { color: #993; } \
    .hidden-thread { color: #666; padding: 5px 0 0 28px; min-height: 24px; vertical-align: middle; background: url(' +
      'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAMAAADXqc3KAAAC5VBMVEUAAIlvDBBzDQ6ZAACNCQuXBgaQCguSDQ6OEhKdDAw4O' +
      'EZ%2FHSOaExOcFRWbFxebGBhAQECbGRmcHx%2BgHx9HRkalHh5IR0elICBISEijISFvOTqlIyKlJCOWKiymJCSnJCSnJSU%2FT2CmJiWnJiaoJiZOTU2oJy' +
      'enKCdvP0WnKChHTmSoKCipKCieLS2oKSmpKSmpKipTT0%2BpKyuqKyuqLCyrLS1cUFCZNjaeNjatNjaeQUCfQUFeXV2MSkmvQD9jY2OxQkGgTEyzRERVaX6' +
      '0RUVqZWVnZ2dpZW%2B1Rka1R0e0TEuJYGB5aWm1UlC5UVG1U1K3VlW4VlSiYGB9cnK7WFiiY2O8WFiaZmq8WVm8Wlq9WlqkZWW9XFt8eHi%2BXV2%2BXl6%' +
      '2FX1%2BpaWmjbGu%2FYGB%2BfHzAYmLAY2OEf36DgoKEhIO%2BbGm%2FbWuFjpeOjIzHdXXIdnbId3enhoaRkZHJeXnGe3rIfn2VlZaZlJKmj462iIinkZD' +
      'Lg4KampqmlpXKiYfKionKi4menp68kpGpmpqnnZyonp2poKCloqKqoaGpo6PSkpHSk5KmpqXTk5POlpPAnJyop6aqpqbUlJSop6eoqKepqamqqanPmpfVl5' +
      'eqqqmqqqrVmJirq6qrq6vQnJmsrKzKoJ2tra21qqqurq6nsLqvr66xsLDYoaGysrKzs7Pao6O1tLO6sbbZpqW3t7bbqKjcqamzusHdqqrdq6vLtLLZr6%2F' +
      'cubfExMTFxcXjurrevrrKx8nNzc3hxcPOzs3Q0M%2Fgysfa0M%2FhzczpysrlzMzk0M3X19ft1tbf3dvv2Njg39zf39%2Fg393n3Nru2dnv2dnh4N%2Fw2t' +
      'rp3trh4eDi4d%2Fw3Nzl5eXp5eHq5eDr5uLr5%2BPo6Ojs6OTt6Ojt6ubx6Oft7Ojs7Oz06%2Bru7u707Ozw8PD47u7z8vH39PT39vX49%2Fb69vb79%2Ff' +
      '6%2BPf5%2Bff5%2Bfj7%2BPj8%2BPj6%2Bfn8%2Bfn7%2Bvr8%2B%2FsqJSU76%2FbaAAAAAXRSTlMAQObYZgAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxMA' +
      'AAsTAQCanBgAAAAHdElNRQfXBQcQAg8od%2B2dAAABbUlEQVQoz2NgoCfYXBwVVbwJQ3i2p6majo6asccMFOHzaSoGCb07d06KN1BJOw8V3L%2B4p9aKzyK' +
      'poqWzs7UqSJDHunnWwttAiZmn7jRIe207e%2BLMhcuXD1kyyyt0v3i4ECjR8%2BCAnVLfwdUZqgISPrrMetX6Tue%2BTAVKTLg1XdN%2FS65NWY4ilywzR%' +
      '2F%2BRSKO1n%2BYCJaZcz5JMDBbZsdHZnZGZtzJlUb1K3of5IIkbvsLe32oeL9FiYmYJv9to2KQQ8hoqIbOgXOzaGm5mdo3d2%2B1dtyqHvQFL3MyWq7u0z' +
      '8ycmU0qtshtz6MulfzPIInJ9%2BZpBu7dFcDMapueue752%2BMx%2Buu%2FgixfeuWog3qJNjNn6f2Xr969f7Jc2%2BXq05VAiWPL2kP5hJiZHdtmzZozra' +
      'PQgj964orT0GBJFTVNO%2Fzs48dnF1f5iScjBeLJVHn9OFAgxunLp55EC3YTNSAwQQt2ENhUEBFRsIGCmAYAfnmQEILCdB4AAAAASUVORK5CYII%3D' +
    ') no-repeat left center; } \
    form > div + br[clear="left"] { display: block; height: 1px; } \
    .reply label { font-size: 80%; color: #666; } .reply label span { font-size: 125%; } \
    .reply label a[href="mailto:sage"] { color: #f33; padding-left: 16px; background: url(' + 
      'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAMAAAAolt3jAAAABGdBTUEAAK%2FINwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYm' + 
      'UgSW1hZ2VSZWFkeXHJZTwAAAClUExURcA%2FP5APD5wcHJgXF40MDMJBQZMTE%2Fr6%2BqEgIOjo6PHx8aw5ObZDQ79MTLU0NN7e3qYlJbk4OKsqKrAvL%' +
      '2BPj4%2B3t7fb29sxgYKA5OdXV1d%2Bfn708PKU6OrxUVKc0NJ4qKshcXOCgoLJKSqhAQPns7PPm5tDQ0LE%2BPsVdXdnZ2caFhbtHR6A0NMeHh9qXl81w' +
      'cM6EhMNPT8VoaMV7e798fK5HR7tfX0Qr1q0AAADCSURBVHjaYlBRFGeFAnFFFYAAYpBiQAJSAAHEoCCtxw4B%2BobSCgABxCAoKKbBy8sLxGJigoIAAcTA' +
      'x8cFBAZG2tpcXHx8AAHEICwsKsvDwwPEoqLCwgABxCAkxAkExmbq6pycQkIAAcQgICCixM3NDcQiIgICAAHEwMFhws%2FPbyonx88BBAABxMAEBprKypog' +
      'GiCAGJjBQFJeXhJEAwQQgwwbCEioqUkAKRmAAGLQZUQCugABxKCqpcMCBTpaqgABBgA0Xgxlx6wWOwAAAABJRU5ErkJggg%3D%3D) no-repeat left center; } \
    label, label input { vertical-align: middle; } \
    a.loading { padding-left: 16px; \
      background: url(data:image/gif;base64,R0lGODlhEAAQAOYAAP%2F%2F%2F9TU1JSUlGBgYEBAQERERG5ubqKiotzc3KSkpCQkJCgoK' +
      'DAwMDY2Nj4%2BPmpqarq6uhwcHHJycuzs7O7u7sLCwoqKilBQUF5eXr6%2BvtDQ0Do6OhYWFoyMjKqqqlxcXHx8fOLi4oaGhg4ODmhoaJycnGZmZra2tkZ' +
      'GRgoKCrCwsJaWlhgYGAYGBujo6PT09Hh4eISEhPb29oKCgqioqPr6%2Bvz8%2FMDAwMrKyvj4%2BNbW1q6urvDw8NLS0uTk5N7e3s7OzsbGxry8vODg4Nj' +
      'Y2PLy8tra2np6erS0tLKyskxMTFJSUlpaWmJiYkJCQjw8PMTExHZ2djIyMurq6ioqKo6OjlhYWCwsLB4eHqCgoE5OThISEoiIiGRkZDQ0NMjIyMzMzObm5' +
      'ri4uH5%2BfpKSkp6enlZWVpCQkEpKSkhISCIiIqamphAQEAwMDKysrAQEBJqamiYmJhQUFDg4OHR0dC4uLggICHBwcCAgIFRUVGxsbICAgAAAAAAAAAAAA' +
      'AAAACH%2FC05FVFNDQVBFMi4wAwEAAAAh%2BQQFAAAAACwAAAAAEAAQAAAHjYAAgoOEhYUaIigshoUHGyMpLYI1OTaFCQocJCougjYvPDWDAQURHYY1ExO' +
      'WAAIKEowAPD48ggMLELEyPz6CBAwTsQA6RIIFDRSxNkA9ggYOFbETQTqCBwUWsT1CQ4IIDxcehjoqFUWDEBgfJRovMgg3BzvdhBkgJgYwMx0rOwiMIU6si' +
      'NGBBo5gwhIGAgAh%2BQQFCgAAACwBAAEADgAOAAAHg4AAgjoCVlcLWlwagow7F1QKWCxbI14ljElOUkcQE1NJXSlbgkYDT5eMgjGMCQUiqbA2AEdKULCpO' +
      'TUDSzy3jEVFJkxFvoITFBZNQMU5YRRIDwfFUz88PhZRGbcuAUM1ADgxM0gIOTkuRF8aFIxAJVUrWR5JQmBTsFM4SDQqQQgvjAIBACH5BAUKAAAALAEAAQA' +
      'OAA4AAAeDgACCCAkSaAVdKwGCjEIGSgUODQwLaWuMN11mZ1AUFEJRagsHACFjTTuMjGcsTxpiD2Wqqg9sXCsSPbOMSW1pMUcvu4JTLSwdMzLDqjQWRsuMX' +
      '2RCyzU5ABMeZbqzOTzKAEY0HkBTNjYvEy4UNYw%2FQidCQUA6Py7XqkUIGjg9Q%2ByMAgEAIfkEBQoAAAAsAQABAA4ADgAAB4WAAII%2BJx0PTSBrRoKMO' +
      'BYGJhhmWmlNSYxAIkdrGkU8QVwOTjsAUyUxN4yMZV5LOjhVJ6qqRwsCSSsIs4wQalZrZTm7ghMRVG5rwsNTHHEVO2HDAElsSkYnPdJNKSJFXzchw28MQAA' +
      'uXzghL4I27QBwjBNEAQghUzwyNbs5E2FhEy%2F0MQoEACH5BAUKAAAALAEAAQAOAA4AAAeEgACCE2BuZB0lED6CjAgqcGQWM0cSMRWMQzsJFT8yMgEJJA8' +
      'ZAEU3OzqMjEkfEj8%2FYhqqqmRaaz03U7OMQWl0YEE2u4IUDko9QMLDFA0FPwEvwwBCdV0UCLrDdHECNWE%2B0bMdWCgBADJTEzKMKiZyCgmMNUUvOYItb' +
      'XMHuzbKBSKyBAUCACH5BAUKAAAALAEAAQAOAA4AAAeDgACCLz84JyoQQBOCjFNAN2JJHgdwCT2MFBpfRlM1OSEZVVVAADU%2FPS6MjEEzZGE8CKmqjG5RE' +
      'FNDMrOMPQZnU2G7jEVdBhSLwgBFTCYvRTbJQUtjNTLQwlxpawA217MlDk1GqgMqU1NiMFJOSap1dm1bLFhxFzuzQCJoCgtmZDqMAgEAIfkEBQoAAAAsAQA' +
      'BAA4ADgAAB4CAAII2PD46PTohL4KMOVNDCAFAQTdQIYw1FC4UMgA2FDonSD%2BCLzw5jIxGHkkUNjKoqYxQZUA2NbKpQys7ubIyHWS%2BqTIzHQUtvb4BM' +
      'CUxKV3DWQYQGg1bFrk7TXuXWWosd2ITFBVVeV03jAdOeHF1DQ5pekKyAWQYDgUGBwiMgQAh%2BQQFCgAAACwBAAEADgAOAAAHf4AAggA2OUUUFEU1g4w1M' +
      'kUTYUNDPIMljII5E0Q6EwBADC2YglNAPTIiKU2jgggVQ0ojKqwAE0I4CltTtDVJYgssu6w5HipmWCe0Q1kQZAp0tBArQAFKV3CjFRYHu25PczFQPEVAayA' +
      'WGoMqH05pS0xdBh1gmEYHMBgmFic%2Bg4EAOw%3D%3D) no-repeat left center; } \
    .x_unfoldreply td { border-color: #999; } \
    .x_qrattached:hover { border-bottom: 1px #ccc dotted; } \
    div a.show-hide-thread { display: block; float: right; font-size: 70%; text-decoration: none; } \
    div a.show-hide-thread:hover { text-decoration: underline; color: #f33; } \
    #x_replyform { display: block; border: 1px #ccc solid; margin: 0 2px 2px 2px; padding: 5px; \
                   background-color: #ddd; -moz-border-radius: 5px; } \
    #x_replyform textarea { width: 100%; border: 1px #888 solid; } \
    #x_replyform div { overflow: hidden; margin-top: 5px; } \
    #x_replyform label { float: left; margin-right: 10px; } \
    #x_replyform input[type="text"], #x_replyform input[type="password"] { border: 1px #888 solid; } \
    #x_replyform input[type="file"] > input[type="text"] { border: 1px #888 solid; } /* doesn`t work, however... */ \
    #x_replyform input[type="submit"] { /* float: right; */ border: 1px #666 solid; margin-left: 10px; } \
    #x_replyform button { /* float: right; */ border: 1px #666 solid; margin-left: 10px; }'
  );

  window.onload=function(e)
{
	var match;

	if(match=/#i([0-9]+)/.exec(document.location.toString()))
	if(!document.forms.postform.message.value)
	insert(">>"+match[1]);

	if(match=/#([0-9]+)/.exec(document.location.toString()))
	highlight(match[1]);
}
  