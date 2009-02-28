# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<%include file="wakaba.paginator.mako" args="baselink=c.board"/>
%if c.pages:
<hr/>
%endif

%if c.currentUserCanPost:
<%include file="wakaba.postForm.mako" />
<hr/>
%endif

<form action="/${c.PostAction}/delete" method="post">
<input type="hidden" name="tagLine" value="${c.tagLine}" />
%for thread in c.threads:
%if not thread.hidden:
    <div id="thread-${thread.id}">
        <%include file="wakaba.postOp.mako" args="thread=thread"/>

        %for post in thread.Replies:
           <%include file="wakaba.postReply.mako" args="thread=thread, post=post"/>
        %endfor
    </div>
    <br clear="left" />
%else:
<div id="hiddenThread${thread.id}">
    <img style="vertical-align: bottom;" src="${g.OPT.staticPathWeb}images/hidden.png" alt="Hidden"/>
    ${_('Hidden thread <a href="/%s">#%s</a> (%s replies) posted in /%s/') % (thread.id, thread.id, thread.replyCount, thread.tagLine)}
    [<a href="/ajax/showThread/${thread.id}/${c.tagLine}">${_('Unhide')}</a>]
</div>
%endif
    <hr/>
%endfor

<table class="userdelete">
    <tbody>
        <tr><td>
            <input type="hidden" name="task" value="delete" />
          %if c.isAdmin:
            Reason: <input type="text" name="reason" size="35" />
           %endif

            %if c.userInst.Anonymous:
                Password: <input type="password" name="remPass" size="10" value="${c.remPass}" />
            %endif
            [<label><input type="checkbox" name="fileonly" value="on" />Only file</label>]
            <input value="Delete post(s)" type="submit" />
        </td></tr>
    </tbody>
</table>

</form>

<form action="/search" method="post">
    <input type="text" name="query" size="20" />
    <input value="Search" type="submit" />
</form>

<div class="y_replyform" style="display:none">
    <form action="/1" method="post" enctype="multipart/form-data" id="y_replyform">
        <div class="hidden"><input type="hidden" name="task" value="post" /><input type="hidden" name="akane" /><input type="hidden" name="title" value="" /><input type="hidden" name="tagLine" value="b" /><input type="hidden" name="curPage" value="0" /></div>
        <div><textarea id="y_replyform_text" name="message" rows="5" cols="40"></textarea></div>

        <div class="y_replyform_fields">
            <p id="y_replyform_captcha">
                <label for="y_replyform_captcha_field"><img alt="Captcha" src="http://anoma.li/captcha/11198"/></label>
                <input type="text" size="35" name="captcha" id="y_replyform_captcha_field" class="inactive" request="Captcha required" value="Captcha required" title="Capthca text" />
                <input type="password" value="risiku" size="35" name="remPass" id="y_replyform_password" title="You can use this password to remove posts"/>
            </p>
            <p id="y_replyform_file"><input type="file" id="y_replyform_file_field" name="file" size="10" /></p>
            <p id="y_replyform_sage"><label for="y_replyform_sage_field" title="sage"><input type="checkbox" id="y_replyform_sage_field" name="sage" />sage</label></p>

            <p id="y_replyform_goto"><label for="y_replyform_goto_field" title="goto">Go to</label> <select name="goto" id="y_replyform_goto_field">
                <option value="0">Thread</option>
                <option value="1">First page of current board</option>
                <option value="2">Current page of current board</option>
                <option value="3">Overview</option>
                <option value="4">First page of destination board</option>
                <option value="5">Referrer</option></select>
            </p>
            <p id="y_replyform_buttons"><input type="submit" value="Post" /><input type="button" value="Close" class="close" /></p>
        </div>
        <div class="clear"></div>
    </form>
    <div class="clear">
</div>

<%include file="wakaba.jsService.mako" />

<%include file="wakaba.paginator.mako" args="baselink=c.board"/>

<br clear="all" />

