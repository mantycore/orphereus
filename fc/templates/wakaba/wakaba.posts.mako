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


%if c.pages:
<table border="1"><tbody><tr><td>
%if not c.showPagesPartial:
    %for pg in range(0,c.pages):
        %if pg == c.page:
            [${pg}]
        %else:
            [<a href='/${c.board}/page/${pg}/'>${pg}</a>]
        %endif
    %endfor
%else:
    %for pg in range(0,2):
        %if pg == c.page:
            [${pg}]
        %else:
            [<a href='/${c.board}/page/${pg}/'>${pg}</a>]
        %endif
    %endfor
    %if c.leftPage and c.leftPage>2:
    ...
    %endif
    %if c.leftPage and c.rightPage:
        %for pg in range(c.leftPage,c.rightPage):
            %if pg == c.page:
                [${pg}]
            %else:
                [<a href='/${c.board}/page/${pg}/'>${pg}</a>]
            %endif
        %endfor    
        %if  c.rightPage<c.pages-2:
            ...
        %endif
    %endif   
    %for pg in range(c.pages-2,c.pages):
        %if pg == c.page:
            [${pg}]
        %else:
            [<a href='/${c.board}/page/${pg}/'>${pg}</a>]
        %endif
    %endfor    
%endif
</td></tr></tbody></table>
%endif

<br clear="all" />

%if c.userInst.useAjax():
<script>popup_posts({ajax: true});</script>
%endif