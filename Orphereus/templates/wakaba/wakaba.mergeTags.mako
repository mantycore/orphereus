# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

%if c.result:
<table class="hlTable">
<tr>
<td>${_("Post")}</td>
<td>${_("Tags")}</td>
<td>${_("New tags")}</td>
<td>${_("Action")}</td>
</tr>
%for post in c.result:
<tr>
<td>${post[0]}</td>
<td>${post[1]}</td>
<td>${post[2]}</td>
<td>${post[3]}</td>
</tr>
%endfor
</table>
%else:
    <form method="post" action="${h.url_for('hsMergeTags', act='merge')}">
        ${_('Move all posts from:')}<br/>
        <input type='text' name='sourceTags' /> ${_("(comma-separated list)")}<br/>
        ${_('into:')}<br/>
        <input type='text' name='targetTag' /><br/>
        <input type='submit' value='${_('Merge')}' />
    </form>
%endif

