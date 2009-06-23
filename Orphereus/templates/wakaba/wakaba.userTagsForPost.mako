# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<div class="postarea">
<h3>${_("Tags of thread %d") % c.thread.id}</h3>
<table class="hlTable">
<tr>
    <td><b>${_("Name")}</b></td>
    <td><b>${_("Description")}</b></td>
    <td><b>${_("Actions")}</b></td>
</tr>

%for tag in c.userTags:
<tr>
    <td>${tag.tag}</td>
    <td>${tag.comment and tag.comment or '&nbsp;'}</td>
    <td><a href='${h.url_for('userTagsMapper', act='delete', post=c.thread.id, tagid=tag.id)}'>${_('Remove')}</a></td>
</tr>
%endfor
</table>

<h3>${_("Add user tag to thread %d") % c.thread.id}</h3>
<form id="appendForm" method="post" action="${h.url_for('userTagsMapper', act='add', post=c.thread.id)}">
<table class="hlTable">
<tr>
    <td>${_("Name")}</td>
    <td><input type='text' name='tagName' /></td>
</tr>
<tr>
    <td colspan="2"><input type='submit' value='${_('Append')}' /></td>
</tr>
</table>

<b>${_("Available tags")}</b>
<table class="hlTable">
<tr>
    <td><b>${_("Name")}</b></td>
    <td><b>${_("Description")}</b></td>
    <td><b>${_("Actions")}</b></td>
</tr>
%for tag in c.allTags:
%if not tag in c.userTags: 
<tr>
    <td>${tag.tag}</td>
    <td>${tag.comment}</td>
    <td><a href='${h.url_for('userTagsMapper', act='add', post=c.thread.id, tagid=tag.id)}'>${_('Add to thread')}</a></td>
</tr>
%endif
%endfor
</table>

</form>
</div>
<hr/>

