# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

<table class="hlTable">
<tr>
<td>${_("IP from which this post was created")}</td>
<td>${h.intToDotted(int(c.ip))}</td>
<td><a href="${h.url_for('hsIpBanAttempt', pid=c.firstPost.id)}">${_("Ban")}</a></td>
</tr>
<tr>
<td>${_("Posts count for this IP")}</td>
<td>${c.postsCount}</td>
<td><a href="${h.url_for('hsManageByIp', ip = c.ip, act='showAll')}">${_("Show all posts")}</a></td>
</tr>
<tr>
<td>${_("Posts count for this IP (by unregistered users)")}</td>
<td>${c.unregPostsCount}</td>
<td><a href="${h.url_for('hsManageByIp', ip = c.ip, act='showUnreg')}">${_("Show posts from unregistered users")}</a></td>
</tr>
</table>

%if c.postsList:
${_("Posts:")}
<%include file="wakaba.lookupList.mako" args="postsList=c.postsList" />

<form id="postform" action="${h.url_for('hsManageByIp', ip = c.ip, act=c.act)}" method="post">
    <input type='hidden' name='removeAll' />
    ${_("Remove reason:")}    
    <input type="text" name="deletereason" size="35" value="" /><br/>
    <input type='submit' value="${_("Remove all listed posts")}"/>
</form>
%endif