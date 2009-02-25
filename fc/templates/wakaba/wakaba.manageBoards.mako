# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />

<a href="/holySynod/manageBoards/edit">${_('Create new board')}</a>
<hr />

<table class="hlTable">
<tr>
    <td>${_('Section')}</td>
    <td>${_('Boards')}</td>
</tr>

%for s in c.sectionList:
<tr>
    <td>
    %if s>=0:
    ${s}
    %else:

    %endif
    </td>
    <td>
        %for b in c.boards[s]:
            <a href="/holySynod/manageBoards/edit/${b.tag}">/${b.tag}/</a>
        %endfor
    </td>
</tr>
%endfor

</table>
