# -*- coding: utf-8 -*-
//copy-pasted from 0chan.
function menu_show(id) {
  if(menu_current != '')
  {
    document.getElementById(menu_current).style.display = 'none';
  }
  if(id != '' && document.getElementById(id))
  {
    document.getElementById(id).style.display = 'block';
    menu_current = id;
  }
}

function toggle_div(id) {
    $('#'+id).slideToggle('fast');
}

function update_captcha(e) {
    e.src = e.src.replace(/[0-9]*$/, Math.floor(Math.random() * 9000).toString());
    }

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
      var loader = $("<span class='img_loading'>"+"${_('Loading')}"+"…</span>")
      if (options.loading_icon_path) loader.html("<img src='"+options.loading_icon_path+"'>"+"${_('Loading')}"+"…")
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

  click_expands.repair = function(node){
    node.find("a img.thumb").click(show_image)
  }
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
    e.html("<img class='popup_loading_img' src='"+options.loading_icon_path+"'> "+"${_('Loading')}"+"…")
  }
  var load_off = function(e){
    e.html(e.attr('old_html'))
  }
  var hover_it = function(ev){
    var m = $(this).attr('href').match(/\/(\d+)\#i(\d+)$/);
    if (!((m) && ($(this).html().match(/(\d+)|(op)$/i)))) return false;
    popup_posts.ev = ev
    popup_posts.ui = $(this)
    var content = $("#quickReplyNode"+m[2])
    if (content.size()){
      if (content[0].tagName == 'BLOCKQUOTE')
      {
        var re = new RegExp( "<div class=\"replies\">", "gi" );
        show_it(content.parent().html().split(re)[0])
      }
      else
        show_it(content.html())
    }else if(popup_posts.cache[m[2]] == 404){
      $(this).html("${_('Post not found')}");
    }else if (popup_posts.cache[m[2]]){
      show_it(popup_posts.cache[m[2]]);
    }else if(options.ajax){
        var e = $(this)
        load_on(e)
        $.ajax({type: 'get', url: "${g.OPT.urlPrefix}ajax/getRenderedPost/"+m[2], success: function(html){
          load_off(e)
          html = html.replace(/<\/?table[^>]*>/,'')
          show_it(html);
          popup_posts.cache[m[2]] = html;
        }, error: function(a,b) {popup_posts.cache[m[0]] = 404; e.html("${_('Post not found')}") } });
    }
  }

  $("blockquote a").filter(function(){
    return $(this).attr('href').match(/^\/(.*\/)*-?\d+(\#i\d+)?$/)
  }).hover(hover_it,hide_it)

  popup_posts.repair = function(links){
    links.filter(function(){
      return $(this).attr('href').match(/^\/(.*\/)*-?\d+(\#i\d+)?$/)
    }).hover(hover_it,hide_it)
  }
}

/* YForm */
var YForm = function(){
    this.form = $("#y_replyform")

    var nonreggedField = $('#postform input[name=nonregged]');
    var captchaForbiddenField = $('#postform input[name=forbidCaptcha]');
    var repliesAllowedWithoutCaptchaField = $('#postform input[name=allowAnswersWithoutCaptcha]');
    var nonregged = nonreggedField && nonreggedField.val();
    var captchaForbidden = captchaForbiddenField && captchaForbiddenField.val();
    var repliesAllowedWithoutCaptcha = repliesAllowedWithoutCaptchaField && repliesAllowedWithoutCaptchaField.val();
    if(nonregged && !(captchaForbidden || repliesAllowedWithoutCaptcha)){
        this.anon();
        this.captcha = new YForm.Captcha(this.form)
    }else{
        this.reg()
    }
}

YForm.open = function(e){
    if(!YForm.def) YForm.def = new YForm();
    if(!e || e['tagName'] != 'A') e = this;
    return YForm.def.open(e)
}

YForm.init = function(){
  $(".reflink a").attr("onclick","").click(YForm.open)
}

YForm.repair = function(node){
  node.find(".reflink a").attr("onclick","").click(YForm.open)
}

YForm.prototype = {
    anon: function() {
        this.form.addClass("y_replyform_anon");
    },
    reg: function() {
        var passField = $("#postform input[name=remPass]");
        if (passField.size()) {
            $("#y_replyform_captcha_field").attr("disabled", true);
            $("#y_replyform_captcha img").attr("onclick", "");
        }
        else {
            this.form.removeClass("y_replyform_anon");
            this.form.find("#y_replyform_password").remove() // no save password query!
        }
    },
    set_fields: function(thread_id) {
        var form = this.form;
        var me = this;

        form.attr("action", this.form.attr("action").replace(/\d+/,thread_id) )

        var select = $("#trgetback select");
        if(select.size()) form.find("#y_replyform_goto_field").html(select.html())

        var captcha = $("#trcaptcha img");
        if(captcha.size() && this.captcha) this.captcha.cimg.attr("src",captcha.attr("src"))

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
          m = ["", this.thread_for_link(link), link.attr('href').match(/[^\d]+(\d+)\'/)[1]];
        };
        this.form.parent().insertAfter($("#quickReplyNode" + m[2]))
        this.set_fields(m[1])
        this.quote(m[2])
        this.form.parent().show()
        return false;
    },
    close: function(){
        this.form.parent().hide()
    }
}

YForm.Captcha = function(form){
    var me = this;
    this.cfield = form.find("#y_replyform_captcha_field");
    this.creq = "${_('Captcha required')}"
    this.captcha = ""
    this.cimg = this.cfield.parent().find("img")
    var field = this.cfield;

    field.removeAttr("readonly")
    field.focus(function() {
        if(field.hasClass("valid")) return false;
        field.removeClass("inactive valid invalid").val(me.captcha)
    })
    field.blur(function() {
        if(field.hasClass("valid")) return false;
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
        field.addClass("inactive").val("${_('Validating')}"+"…")

        var callback = function(response) {
            if(response == "ok"){
                setTimeout(function() {field.removeAttr("readonly").val(me.captcha).attr("readonly","true")}, 2000)
                field.val("${_('You are human!')}")
                field.addClass("valid").attr("readonly","true")
            }else{
                field.addClass("invalid").val("${_('Try again')}")
                me.captcha = ""
                img.attr("src", img.attr("src").replace(/\d+/, response))
            }
        }
        var error = function() {
            me.error()
        }

        $.ajax({type: 'get', url: "${g.OPT.urlPrefix}ajax/checkCaptcha/" + this.captcha_id + '/' + this.captcha, success: callback, error: error });
    }
}

function expandable_threads(){
  expandable_threads.mass_repair =  function(node){
    popup_posts.repair(node.find("blockquote a"))
    click_expands.repair(node)
    YForm.repair(node)
  }

  expandable_threads.repair_deleteboxes = function(visible)
  {
     var allDeleteBoxesSpans = $(".delete");
     if (visible) {
        allDeleteBoxesSpans.show()
     }
     else {
        allDeleteBoxesSpans.hide()
     }
  }
  $(".thread .omittedposts a").click(function() {
    var me = $(this)
    var thread = me.parent().parent();
    var deleteBoxesShown = thread.find('.delete').is(':visible');
    if(me.data("oldreplies")){
      var t = me.data("oldreplies")
      me.data("oldreplies", thread.find(".replies").html())
      thread.find(".replies").html(t)

      t = me.data("orig_html")
      me.data("orig_html", me.html())
      me.html(t)

      expandable_threads.mass_repair(thread.find(".replies"))
      expandable_threads.repair_deleteboxes(deleteBoxesShown);
      me.parent().toggleClass("expanded")
    }else{
      me.data("orig_html", me.html())
      me.data("oldreplies", thread.find(".replies").html())
      me.html("<img src='"+window.loading_icon_path+"'>"+"${_('Loading')}"+"…")
      thread.find(".replies").load("${g.OPT.urlPrefix}ajax/getRenderedReplies/" + thread.attr("id").match(/\d+/)[0], function() {
        me.parent().toggleClass("expanded")
        me.html("${_('Collapse thread')}")
        expandable_threads.mass_repair(thread.find(".replies"))
        expandable_threads.repair_deleteboxes(deleteBoxesShown);
      })
    }
    return false;
  })
}

function showDeleteBoxes()
{
    $('.delete').animate({'opacity' : 'toggle'}, 250);
}

function tagCheckComplete(data) {
    if (data) {
        $("#paramPlaceholder").html(data);
        $("#additionalPostParameters input").attr('disabled', '');
    }
    else {
        $("#postform").submit();
    }
}

function checkForTagNames(){
    var checkedField = $('#postform input[name=tagsChecked]');
    if (!checkedField.val() && $('#postform input[name=newThread]').val())
    {
        var tags = $('#postform input[name=tags]').val();
        $.post("${h.url_for('ajTagsCheck')}", { tags: tags}, tagCheckComplete);
        $("#additionalPostParameters input").attr('disabled', 'disabled');
        $("#oekakiForm").hide();
        $("#postControls").hide();
        $("#postFormBanner").hide();
        $("#additionalPostParameters").show();
        $("#paramPlaceholder").html($("#paramPlaceholderContent").html());
        checkedField.val('yes');
        return false;
    }
    else
    {
        checkedField.val('');
        return true;
    }
}

function restoreForm() {
    $("#additionalPostParameters").hide();
    $("#postControls").show();
    $("#oekakiForm").show();
    $("#postFormBanner").show();
    $('#postform input[name=tagsChecked]').val('');
    $("#paramPlaceholder").html('&nbsp;');
}


function getFullText(event, thread, post)
{
    var bq = document.getElementById('postBQId' + post);
    if (!bq) bq = document.getElementById('quickReplyNode' + post);
    var loadingString = "${_('Loading')}"+'…'
    if (window.loading_icon_path)
    {
        loadingString = "<img class='comment_loading_img' src='"+window.loading_icon_path+"'> "+"${_('Loading')}"+"…"
    }
    $("a.expandPost[href=/" + thread + "#i" + post + "]").html(loadingString)
    $.get('${g.OPT.urlPrefix}ajax/getPost/' + post, {}, function(response)
    {
      $(bq).html(response);
    popup_posts.repair($(bq).find("a"))
    });
    event.preventDefault();
}

function userFiltersAdd(event)
{
  if ($('#newFilterInput').val())
  {
    $('#newFilterInput').fadeTo("fast", 0.2);
    $.get('${g.OPT.urlPrefix}ajax/addUserFilter/' + $('#newFilterInput').val(), {}, function(response)
    {
      $('#newFilterInput').fadeTo("fast", 1, function() {$('#newFilterInput').val('');});
      $(response).insertBefore('#newFilterTR');
    });
  }
  event.preventDefault();
}
function userFiltersEdit(event,fid)
{
  var input = $('#filterId' + fid + 'Input');
  input.fadeTo('fast', 0.2, function(){
    var filterText = input.val();
    input.val('${_('Updating...')}');
    $('#changeLinkId' + fid).hide();
    $.get('${g.OPT.urlPrefix}ajax/editUserFilter/' + fid + '/' + filterText, {}, function(response)
    {
      $('#changeLinkId' + fid).show();
      $('#filterId' + fid + 'Input').val(response);
      $('#filterId' + fid + 'Input').fadeTo("slow", 1);
    });
  });
  event.preventDefault();
}
function userFiltersDelete(event,fid)
{
  $('#filterId' + fid + 'Input').fadeTo('fast', 0.2, function(){
      $.get('${g.OPT.urlPrefix}ajax/deleteUserFilter/' + fid, {}, function(response)
      {
            $('#filterId' + fid).remove();
      });
  })
  event.preventDefault();
}

function addFileRow() {
  var currentCount = parseInt($("#createdRows").attr("value"));
  var additionalFilesCount = parseInt($("#additionalFilesCount").attr("value"));
  if (currentCount > additionalFilesCount - 1) {
    return;
  } else
  {
    if (currentCount == additionalFilesCount - 1)
        $("#addFileBtn").attr("disabled", "disabled");
    $("#createdRows").attr("value", currentCount + 1);

     var currentId = parseInt($("#nextRowId").attr("value"));
     $("#nextRowId").attr("value", currentId + 1);

     var newRow = $("#trfile_").clone();
     newRow.attr("id", "trfile_" +  currentId);
     var fileField = $("input[name = file_]", newRow);
     fileField.attr("name", "file_" + (currentId + 1));
     var fileIdField = $("input[name = fileRowId]", newRow);
     fileIdField.attr("value", currentId);
     var spolierField = $("input[name = spoiler_]", newRow);
     if (spolierField) {
      spolierField.attr("name", "spoiler_" + (currentId + 1));
     }
    newRow.insertBefore("#filesBlockEnd");
  }
}

function addFileRowOnChange(input) {
  if (!input.previousValue)
    addFileRow();
  input.previousValue = input.value;
}

function removeRow(input)
{
  var idToRemove = $(input).next().val();
  $("#trfile_" + idToRemove).remove();
  var currentCount = parseInt($("#createdRows").attr("value"));
  $("#createdRows").attr("value", currentCount - 1 );
  $("#addFileBtn").attr("disabled", "");
}

function installPopupHintsOnFiles(){
$('.file_thread img').each(function (i) {
  var popupInfo = $(this).parents(".file_thread").children(".popupDiv").get()[0];
  if (popupInfo)
  {
   $(this).qtip({
     content: $(popupInfo).html(),
     show : {
       delay: 10,
       when: {event : 'mouseover'}
     },
     hide: 'mouseout',
     style: { name: 'light', tip: true },
     position: {
        corner: {
           target: 'topLeft',
           tooltip: 'bottomLeft'
        }
     }
   });
  }
});
}

function resetRow(id, attr, value) {
  var rowToModify = $(id);
  if (rowToModify){
    rowToModify.attr(attr, value);
  }
}

// code below should be rewritten using JQuery
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
        document.location=match[1]+"#"+post;
*/
        return false;
    }
    return true;
}

window.onload=function(e)
{
    var match = /#i([0-9]+)/.exec(document.location.toString());
    if(match)
    {
       var postId = match[1];
       highlight(postId);
      /*
        // Annoying Wakaba behavior
        if(!document.forms.postform.message.value)
          insert(">>"+postId,1);
       */
    }
    installPopupHintsOnFiles();
}


