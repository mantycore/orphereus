# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<%include file="wakaba.postForm.mako" />

<form action="/${c.PostAction}/delete" method="post">
<input type="hidden" name="tagLine" value="${c.tagLine}">
%for thread in c.threads:
    <div id="thread-${thread.id}">
        <%include file="wakaba.postOp.mako" args="thread=thread"/>
        
        %for post in thread.Replies:
			<%include file="wakaba.postReply.mako" args="thread=thread, post=post"/>
        %endfor        
    </div>
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


<%include file="wakaba.paginator.mako" args="baselink=c.board"/>

<br clear="all" />

%if c.userInst.useAjax():
<script>popup_posts({ajax: true});</script>
%endif