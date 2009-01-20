# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />

<table class="hlTable">
<tr>
<td>${_("Post number")}</td>
<td>${_("Timestamp")}</td>
</tr>
%for post in c.posts:
<tr>
<td>
<blockquote style="margin: 0; padding: 0;">

%if post.parentid == -1:
    <b><a href="/${post.id}#i${post.id}">&gt;&gt;${post.id}</a></b> 
%else:
    <a href="/${post.parentid}#i${post.id}">&gt;&gt;${post.id}</a> 
%endif

</blockquote>
</td>
<td>${post.date}</td>
</tr>
%endfor
</table>

%if c.userInst.useAjax():
    <script>popup_posts({ajax: true});</script>
%endif

