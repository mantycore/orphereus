<%page args="thread"/>

%if not (hasattr(thread, 'hideFromBoards') and thread.hideFromBoards):
%if g.OPT.memcachedPosts and not(c.userInst.isAdmin()):
	${h.repliesProxy(thread, controller)}
%else:
	%for post in thread.Replies:
	   	<%include file="noema.postReply.mako" args="thread=thread, post=post"/>
	%endfor
%endif
</div>
%endif
