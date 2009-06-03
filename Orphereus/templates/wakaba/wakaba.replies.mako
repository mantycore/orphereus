<%page args="thread"/>

%for post in thread.Replies:
   <%include file="wakaba.postReply.mako" args="thread=thread, post=post"/>
%endfor
