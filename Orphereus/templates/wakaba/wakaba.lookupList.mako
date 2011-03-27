<%page args="postsList"/>

<table class="hlTable">
<tr>
<td>${_("Post number")}</td>
<td>${_("Timestamp")}</td>
</tr>
%for post in postsList:
<tr>
<td>
<blockquote style="margin: 0; padding: 0;">


<a target="_blank" href="${h.postUrl(post.parentid, post.id)}">&gt;&gt;${post.id}</a>
%if not(post.parentPost):
    <b>[op]</b>
%endif

</blockquote>
</td>
<td>${h.tsFormat(post.date)}</td>
</tr>
%endfor
</table>

%if c.userInst.useAjax:
    <script type="text/javascript">popup_posts({ajax: true});</script>
%endif
