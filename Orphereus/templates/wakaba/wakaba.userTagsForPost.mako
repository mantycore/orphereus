# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<b>Tags:</b>
<table border="1">
<tbody>
%for tag in c.userTags:
    <tr>
        <td>${tag.tag}</td>
        <td><a href='${h.url_for('userTagsMapper', act='delete', post=c.thread.id, tagid=tag.id)}'>${_('Remove')}</a></td>
    </tr>
%endfor
</tbody>
</table>

<form id="appendForm" method="post" action="${h.url_for('userTagsMapper', act='add', post=c.thread.id)}">
    <input type='text' name='tagName' />
    <input type='submit' value='${_('Append')}' />
</form>

