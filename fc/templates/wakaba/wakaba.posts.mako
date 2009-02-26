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
%else:
<div id="hiddenThread${thread.id}" >
<!--    <img style="vertical-align:center;" src="${g.OPT.staticPathWeb}images/hidden.png" alt="Hidden"/> -->
    ${_('<b>Hidden</b> thread <a href=/%s>#%s</a> (%s replies) posted in %s') % (thread.id, thread.id, thread.replyCount, thread.tagLine)}
    [<a href="/ajax/showThread/${thread.id}/${c.tagLine}">${_('Unhide')}</a>]
</div>
%endif
    <br clear="left" />
    <hr />
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

<script type="text/javascript">
%if c.userInst.useAjax():
    popup_posts({ajax: true});
%endif
%if c.userInst.expandImages():
    click_expands({max_width: ${c.userInst.maxExpandWidth()}, max_height: ${c.userInst.maxExpandHeight()}});
%endif
</script>

<%include file="wakaba.paginator.mako" args="baselink=c.board"/>

<br clear="all" />

