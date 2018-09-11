# -*- coding: utf-8 -*-
<%inherit file="noema.management.mako" />

<form id="mapeditForm" method="post" action="${h.url_for('hsMappings', act='show')}">
    ${_('Enter post ID:')}<br/>
    <input type='text' name='postId' />
    <input type='submit' value='${_('Manage mappings')}' />
</form>

%if c.post:
<hr />

<div class="reply">
<b>#${c.post.id}</b><br/>
<blockquote class="postbody">
${c.post.message}
</blockquote>
</div>

<b>Tags:</b>
<table border="1"><tbody>
    %for tag in c.post.tags:
        <tr>
            <td>${tag.tag}</td>
            <td><a href='${h.url_for('hsMappings', act='del', id=c.post.id, tagid=tag.id)}'>${_('Remove')}</a></td>
        </tr>
    %endfor
    </tbody>
</table>

<form id="appendForm" method="post" action="${h.url_for('hsMappings', act='add')}">
    <input type='text' name='tagName' />
    <input type='hidden' name='postId' value='${c.post.id}' />
    <input type='submit' value='${_('Append')}' />
</form>
%endif


