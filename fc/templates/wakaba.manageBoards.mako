# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />

<a href="/holySynod/manageBoards/edit">${_('Create new board')}</a>
<hr />
%for s in c.boards:
    %for b in c.boards[s]:
        <a href="/holySynod/manageBoards/edit/${b.tag}">/${b.tag}/</a>
    %endfor
    <hr />
%endfor
