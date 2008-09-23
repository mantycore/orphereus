# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />

<form id="mapeditForm" method="post" action="/holySynod/manageMappings/show">
    Enter post ID:<br/>
    <input type='text' name='postId'>
    <input type='submit' value='${_('Manage mappings')}'>
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
            <td><a href='/holySynod/manageMappings/del/${c.post.id}/${tag.id}'>Remove</a></td>
        </tr>
    %endfor
    </tbody>
</table>

<form id="mapeditForm" method="post" action="/holySynod/manageMappings/add">
    <input type='text' name='tagName'>
    <input type='hidden' name='postId' value='${c.post.id}'>
    <input type='submit' value='${_('Append')}'>
</form>  
%endif


