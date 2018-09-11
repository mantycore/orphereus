# -*- coding: utf-8 -*-
<%inherit file="noema.management.mako" />

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
        <input type='text' name='sourceTags' value='${c.proposedTags}' /> ${_("(comma-separated list)")}<br/>
        ${_('into:')}<br/>
        <input type='text' name='targetTag' value='b' /><br/>
        <input type='submit' value='${_('Merge')}' />
    </form>
%endif

