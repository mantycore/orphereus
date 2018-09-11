# -*- coding: utf-8 -*-
<%inherit file="noema.main.mako" />

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
</form>

<h3>${_("Tags")}</h3>
<table class="hlTable">
<tr>
    <td><b>${_("Name")}</b></td>
    <td><b>${_("Description")}</b></td>
    <td><b>${_("Mapped threads")}</b></td>
    <td><b>${_("Actions")}</b></td>
</tr>
%for tag in c.userTags:
<tr>
    <td><a href="${h.url_for('boardBase', board = '$' + tag.tag)}">/$${tag.tag}/</a></td>
    <td>${tag.comment and tag.comment or '&nbsp;'}</td>
    <td>
    %for post in tag.posts:
    <a href="${h.url_for('thread', post=post.id)}">#${post.id}</a>
    %endfor
    </td>
    <td>
    %if not tag.posts:
        <a href='${h.url_for('userTagsManager', act='delete', tagid=tag.id)}'>${_('Remove')}</a>
    %else:
        <a href='${h.url_for('userTagsManager', act='removefromall', tagid=tag.id)}'>${_('Remove from all threads')}</a>
    %endif
    <a style="cursor:pointer;" href="#" onclick="toggle_div('tag_${tag.id}');">${_('Change description')}</a>
    <div id="tag_${tag.id}" style="display: none;">
    <form id="userTagsForm" method="post" action="${h.url_for('userTagsManager', act='rename', tagid=tag.id)}">
        <input type='text' name='tagDescr' />
        <input type='submit' value='${_('Change')}' />
    </form>
    </div>
    </td>
</tr>
%endfor
</table>

</div>
<hr/>