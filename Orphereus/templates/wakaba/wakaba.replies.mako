<%page args="thread"/>

%if g.OPT.memcachedPosts and not(c.userInst.isAdmin()):
  ${h.repliesProxy(thread, controller)}
%else:
  %for post in thread.Replies:
       <%include file="wakaba.postReply.mako" args="thread=thread, post=post"/>
  %endfor
%endif
