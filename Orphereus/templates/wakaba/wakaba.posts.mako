# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

%if g.OPT.useTopPaginator:
<%include file="wakaba.paginator.mako" args="routeName='board', kwargDict={'board' : c.board}" />
%if c.pages:
<hr/>
%endif
%endif

%if c.currentUserCanPost:
<%include file="wakaba.postForm.mako" />
<hr/>
%endif

<form action="${h.url_for('process', board=c.currentRealm)}" method="post">
<input type="hidden" name="tagLine" value="${c.tagLine}" />
%for thread in c.threads:
%if not thread.hideFromBoards:
    <div
    %if not (c.userInst.hlOwnPosts and c.userInst.ownPost(thread)): #thread.uidNumber != c.uidNumber or not c.userInst.hlOwnPosts:
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
    [<a href="${h.url_for('ajShowThread', post=thread.id, redirect='board', realm=unicode(c.currentRealm), page=c.curPage)}">${_('Unhide')}</a>]
</div>
%endif
    <hr/>
%endfor
<%include file="wakaba.paginator.mako" args="routeName='board', kwargDict={'board' : c.board}" />
%if c.pages:
<hr />
%endif

%if not(c.minimalRender):
<table class="userdelete">
    <tbody>
			%for tmpl in c.multifileTemplates:
			<tr><td>
        	<%include file="wakaba.${tmpl}.mako" />
			</tr></td>
			%endfor
    </tbody>
</table>

</form>

<form action="${h.url_for('searchBase')}" method="post">
    <input type="text" name="query" size="20" />
    <input value="${_('Search')}" type="submit" />
%endif

</form>

<%include file="wakaba.jsService.mako" />

<br clear="all" />

