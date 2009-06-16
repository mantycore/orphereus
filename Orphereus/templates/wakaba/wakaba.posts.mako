# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<%include file="wakaba.paginator.mako" args="routeName='board', kwargDict={'board' : c.board}" />
%if c.pages:
<hr/>
%endif

%if c.currentUserCanPost:
<%include file="wakaba.postForm.mako" />
<hr/>
%endif

<form action="${h.url_for('delete', board=c.PostAction)}" method="post">
<input type="hidden" name="tagLine" value="${c.tagLine}" />
%for thread in c.threads:
%if not thread.hideFromBoards:
    <div
    %if thread.uidNumber != c.uidNumber or not c.userInst.hlOwnPosts:
    class="thread"
    %else:
    class="thread mythread"
    %endif
    id="thread-${thread.id}">
    <%include file="wakaba.postOp.mako" args="thread=thread"/>

    <div class="replies">
    <%include file="wakaba.replies.mako" args="thread=thread"/>
    </div>
    </div>
    <br clear="left" />
%else:
<div id="hiddenThread${thread.id}">
    <img style="vertical-align: bottom;" src="${g.OPT.staticPathWeb}images/hidden.png" alt="Hidden"/>
    ${_('Hidden thread <a href="%s">#%s</a> (%s replies) posted in /%s/') % (h.url_for('thread', post=thread.id) , thread.id, thread.replyCount, thread.tagLine)}
    [<a href="${h.url_for('ajShowThread', post=thread.id, redirect=u'%s%s' % (unicode(c.PostAction), c.curPage and '/page/'+str(c.curPage) or ''))}">${_('Unhide')}</a>]
</div>
%endif
    <hr/>
%endfor

<%include file="wakaba.paginator.mako" args="routeName='board', kwargDict={'board' : c.board}" />
%if c.pages:
<hr />
%endif

<table class="userdelete">
    <tbody>
        <tr><td>
            <input type="hidden" name="task" value="delete" />
          %if c.isAdmin:
            ${_('Reason')}: <input type="text" name="reason" size="35" />
           %endif

            %if c.userInst.Anonymous:
                ${_('Password')}: <input type="password" name="remPass" size="10" value="${c.remPass}" />
            %endif
            [<label><input type="checkbox" name="fileonly" value="on" />${_('Only file')}</label>]
            <input value="${_('Delete post(s)')}" type="submit" />
        </td></tr>
    </tbody>
</table>

</form>

<form action="${h.url_for('searchBase')}" method="post">
    <input type="text" name="query" size="20" />
    <input value="${_('Search')}" type="submit" />
</form>

<div class="y_replyform" style="display:none">
<form action="/1" method="post" enctype="multipart/form-data" id="y_replyform" class="y_replyform_anon">
    <div class="hidden">
    <input type="hidden" name="task" value="post" />
    <input type="hidden" name="title" value="" />
    <input type="hidden" name="tagLine" value="b" />
    <input type="hidden" name="curPage" value="0" />
    </div>
    <div><textarea id="y_replyform_text" name="message" rows="5" cols="40" tabindex="10"></textarea></div>

    <div class="y_replyform_fields">
        <p id="y_replyform_captcha">
            <label for="y_replyform_captcha_field">
                <img width="150" height="40" alt="Captcha" src="${g.OPT.staticPathWeb}images/placeholder.png"  onclick="update_captcha(this)"/>
            </label>
            <input type="text" size="35" name="captcha" id="y_replyform_captcha_field" class="inactive" value="${_('Captcha required')}" title="Captcha text" tabindex="20"/>
            <input type="password" value="risiku" size="35" name="remPass" id="y_replyform_password" title="You can use this password to remove posts"/>
        </p>
        <p id="y_replyform_file">
            <input type="file" id="y_replyform_file_field" name="file" size="10" tabindex="40" />
        </p>
        <p id="y_replyform_sage">
            <label for="y_replyform_sage_field" title="sage"><input type="checkbox" id="y_replyform_sage_field" name="sage" tabindex="50"/>sage</label>
        </p>
        <p id="y_replyform_goto">
            <label for="y_replyform_goto_field" title="goto">${_('Go to')}</label>
            <select name="goto" id="y_replyform_goto_field"  tabindex="60">
                <option value="0">Thread</option>
                <option value="1">First page of current board</option>
                <option value="2">Current page of current board</option>
                <option value="3">Overview</option>
                <option value="4">First page of destination board</option>
                <option value="5">Referrer</option>
            </select>
        </p>
        <p id="y_replyform_buttons"><input type="submit" value="${_('Post')}" tabindex="30"/><input type="button" value="${_('Close')}" class="close" /></p>
    </div>
    <div class="clear"></div>
</form>
<div class="clear"></div>
</div>

<%include file="wakaba.jsService.mako" />

<br clear="all" />

