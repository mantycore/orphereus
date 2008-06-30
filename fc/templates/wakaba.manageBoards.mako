# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />

<a href="/holySynod/editBoard">${_('Create new board')}</a>
<hr />
%for s in c.boards:
    %for b in s:
        <a href="/holySynod/editBoard/${b.tag}">/${b.tag}/</a>
    %endfor
    <hr />
%endfor