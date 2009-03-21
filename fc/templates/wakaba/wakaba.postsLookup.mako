# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

<table class="hlTable">
<tr>
<td>${_("Post number")}</td>
<td>${_("Timestamp")}</td>
</tr>
%for post in c.posts:
<tr>
<td>
<blockquote style="margin: 0; padding: 0;">


<a href="${h.postUrl(post.parentid, post.id)}">&gt;&gt;${post.id}</a>
%if post.parentPost:
    <b>[op]</b>
%endif

</blockquote>
</td>
<td>${post.date}</td>
</tr>
%endfor
</table>

%if c.userInst.useAjax():
    <script type="text/javascript">popup_posts({ajax: true});</script>
%endif

