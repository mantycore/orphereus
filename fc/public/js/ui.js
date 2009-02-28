function click_expands(options){
  var default_options = {max_width: 800, max_height: 600}
  if(!options) options = default_options
  if(!options.max_width) options.max_width = default_options.max_width
  if(!options.max_width) options.max_height = default_options.max_height

  if(options.loading_icon_path) $("<img>").attr("src", options.loading_icon_path)

  var show_image = function() {
    var filesize = $(this).parent().parent().find("span.filesize em").html()
    var matcher = filesize.match(/(\d+)x(\d+)/)
    if (!matcher) return true;
    if(options.max_height || options.max_width){
        if (options.max_width  && options.max_width  < parseInt(matcher[1])) return true;
        if (options.max_height && options.max_height < parseInt(matcher[2])) return true;
    }

    if (this.src != this.parentNode.href){
      this._width = this.width
      this._height = this.height
      this._src = this.src

      // loader
      var loader = $("<span class='img_loading'>Loading…</span>")
      if (options.loading_icon_path) loader.html("<img src='"+options.loading_icon_path+"'>Loading…")
      loader.css("left", $(this).offset().left)
      $(this).parent().append(loader)
      $(this).load(function() {loader.remove()})

      //highlight
      $(this).addClass("highlight")

      this.removeAttribute('width');
      this.removeAttribute('height');
      this.src = this.parentNode.href;
    }else{
      this.width = this._width
      this.height = this._height
      this.src = this._src

      $(this).removeClass("highlight")
    }
    return false;
  }
  $("a img.thumb").click(show_image)
}

function popup_posts(options){
  if(!options) options = {}
  popup_posts.helper = $(document.createElement('blockquote'));
  popup_posts.helper.css('position','absolute');
  popup_posts.helper.addClass("popup_post");
  popup_posts.helper.hide();
  popup_posts.cache = {}

  if(options.loading_icon_path) $("<img>").attr("src", options.loading_icon_path)

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
    e.html("<img class='popup_loading_img' src='"+options.loading_icon_path+"'> Loading…")
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
        // new form fields:
        if($("#trcaptcha").size()){
          var captcha_label = $("<label style='float:none' id='x_replyform_captcha_label'>" + $("#trcaptcha td:first").html() + "</label>");
          var captcha_img = $("#trcaptcha img").clone().attr("id","x_replyform_captcha_img");
          var captcha_input = $("#trcaptcha input").clone().attr("id","x_replyform_captcha_input");
          var password_label = $("<label style='float:none' id='x_replyform_password_label'>" + $("#trrempass td:first").html() + "</label>");
          var password_input = $("#trrempass input").clone().attr("id","x_replyform_password_input");;
          $([captcha_label, captcha_img, captcha_input, password_label, password_input]).each(function() {$(objBottomDiv).append(this)})
        }
        // end of new form fields
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
    var loadingString = 'Loading…'
    if (window.loading_icon_path)
    {
        loadingString = "<img class='comment_loading_img' src='"+window.loading_icon_path+"'> Loading…"
    }
    $("a.expandPost[href=/" + thread + "#i" + post + "]").html(loadingString)
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

var YForm = function(){
    this.form = $("#y_replyform")

    if($("#trcaptcha img").size()){
        this.anon();
        this.captcha = new YForm.Captcha(this.form)
    }else{
        this.reg()
    }
}

YForm.open = function(e){
  try{
    if(!YForm.default) YForm.default = new YForm();
    if(!e || e['tagName'] != 'A') e = this;
    return YForm.default.open(e)
  }catch(e){ console.error(e); return false;}
}

YForm.init = function(){
  $(".reflink a").attr("onclick","").click(YForm.open)
}

YForm.prototype = {
    anon: function() {
        this.form.addClass("y_replyform_anon")
    },
    reg: function() {
        this.form.removeClass("y_replyform_anon")
        this.form.find("#y_replyform_password").remove() // no save password query!
    },
    set_fields: function(thread_id) {
        var form = this.form;
        var me = this;

        form.attr("action", this.form.attr("action").replace(/\d+/,thread_id) )

        var select = $("#trgetback select");
        if(select.size()) form.find("#y_replyform_goto_field").html(select.html())

        var captcha = $("#trcaptcha img")
        if(captcha.size()) this.captcha.cimg.attr("src",captcha.attr("src"))

        $(["tagLine", "curPage", "remPass"]).each(function() {
            var field = $("#postform input[name="+this+"]")
            if(field.size()) form.find("input[name="+this+"]").val(field.val())
        })

        $("#y_replyform_buttons .close").click(function() {me.close()})
    },
    quote: function(post_id){
      var value = $("#y_replyform_text").val();
      $("#y_replyform_text").val(value + ">>" + post_id + "\n")
    },
    thread_for_link: function(link){
      link = link[0]
      var match
      while(link = link.parentNode){
        if(match = link.id.match(/^thread\D*(\d+)$/)) return match[1];
      }
    },
    open: function(link) {
        link = $(link)
        var m = link.attr("href").match(/\/(\d+)\D+(\d+)$/)
        if(!m){ //thread
          m = ["", this.thread_for_link(link), link.html().match(/\d+/)[0]]
        };
        console.info("attaching"+m[2]+"(thread "+m[1]+")")
        this.form.parent().insertAfter($("#quickReplyNode" + m[2]))
        this.set_fields(m[1])
        this.quote(m[2])
        this.form.parent().show()
        return false;
    },
    close: function(){
        this.form.hide()
    }
}

YForm.Captcha = function(form){
    var me = this;
    this.cfield = form.find("#y_replyform_captcha_field");
    this.creq = this.cfield.attr("request")
    this.cimg = this.cfield.parent().find("img")
    var field = this.cfield;

    field.removeAttr("readonly")
    field.focus(function() {
        field.removeClass("inactive valid invalid").val("")
    })
    field.blur(function() {
        me.test()
    })
    form.submit(function() {
      if(me.captcha) me.cfield.removeAttr("readonly").val(me.captcha).attr("readonly","true")
      return true;
    })
}
YForm.Captcha.prototype = {
    request: function(){
        this.cfield.removeClass("inactive valid invalid").addClass("inactive").val(this.creq)
    },
    error: function() {
        this.cfield.removeClass("inactive valid invalid").addClass("invalid").val("Error! Refresh page please")
        if(window.console) console.error("errors in captcha uri");
    },
    test: function(){
        var me = this;
        var img = this.cimg;
        this.captcha = this.cfield.val()
        if(img.attr("src").match(/\d+/)) this.captcha_id = img.attr("src").match(/\d+/)[0];
        else return me.error();
        if(!this.captcha) return this.request();
        var field = this.cfield
        field.addClass("inactive").val("Validating…")

        var callback = function(response) {
            if(response == "ok"){
                setTimeout(function() {field.removeAttr("readonly").val(me.captcha).attr("readonly","true")}, 2000)
                field.val("You are human!")
                field.addClass("valid").attr("readonly","true")
            }else{
                field.addClass("invalid").val("Try again")
                img.attr("src", img.attr("src").replace(/\d+/, response))
            }
        }
        var error = function() {
            me.error()
        }

        $.ajax({type: 'get', url: "/ajax/checkCaptcha/" + this.captcha_id + '/' + this.captcha, success: callback, error: error });
    }
}


