# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

<a href="${h.url_for('hsBoardEdit')}">${_('Create new board')}</a>
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
            <a href="${h.url_for('hsBoardEdit', tag=b.tag)}" \
            %if b.adminOnly:
            style="color: red; font-weight: bold;" \
            %endif
            >/${b.tag}/</a>
        %endfor
    </td>
</tr>
%endfor

</table>
