# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<div class="postarea">
<h3>${_("Add user tag")}</h3>
<form id="userTagsForm" method="post" action="${h.url_for('userTagsManager', act='add')}">
<table class="hlTable">
<tr>
    <td>${_("Name")}</td>
    <td><input type='text' name='tagName' /></td>
</tr>
<tr>
    <td>${_("Description")}</td>
    <td><input type='text' name='tagDescr' /></td>
</tr>
<tr>
    <td colspan="2"><input type='submit' value='${_('Append')}' /></td>
</tr>
</table>

<h3>${_("Tags")}</h3>
<table class="hlTable">
<tr>
    <td><b>${_("Name")}</b></td>
    <td><b>${_("Description")}</b></td>
    <td><b>${_("Actions")}</b></td>
</tr>
%for tag in c.userTags:
<tr>
    <td>${tag.tag}</td>
    <td>${tag.comment}</td>
    <td><a href='${h.url_for('userTagsManager', act='delete', tagid=tag.id)}'>${_('Remove')}</a></td>
</tr>
%endfor
</table>

</form>
</div>
<hr/>