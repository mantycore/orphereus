# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<b>Tags:</b>
<table class="hlTable"><tbody>
    %for tag in c.userTags:
        <tr>
            <td>${tag.tag}</td>
            <td>${tag.comment}</td>
            <td><a href='${h.url_for('userTagsManager', act='delete', tagid=tag.id)}'>${_('Remove')}</a></td>
        </tr>
    %endfor
    </tbody>
</table>

<form id="userTagsForm" method="post" action="${h.url_for('userTagsManager', act='add')}">
    <input type='text' name='tagName' />
    <input type='text' name='tagDescr' />
    <input type='submit' value='${_('Append')}' />
</form>