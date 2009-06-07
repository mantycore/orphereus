# -*- coding: utf-8 -*-
<%page args="boards, totalThreads, totalPosts"/>

<table width="100%" class="hlTable">
<thead>
    <tr>
        <td style="width: 200px;">${_('Name')}</td>
        <td style="width: 40px;">${_('Threads')}</td>
        <td style="width: 40px;">${_('Posts')}</td>
        <td>${_('Description')}</td>
    </tr>
</thead>
<tbody>
%for b in boards:
    <tr>
        <td><div class="hovblock"><a style="display: block;" href="${h.url_for('boardBase', board=b.board.tag)}">${b.board.tag}</a></div></td>
        <td>${b.count}</td>
        <td>${b.postsCount}</td>
        <td>
        %if b.board.options and b.board.options.comment:
            ${b.board.options.comment}
        %endif
        %if b.board.options and b.board.options.specialRules:
            <div class="smallFont">
            Rules:
            <ul class="nomargin">
            %for rule in b.board.options.specialRules.split(';'):
                <li>${rule}</li>
            %endfor
            </ul>
            </div>
        %endif
        </td>
    </tr>
%endfor
    <tr>
        <td><div class="hovblock"><b>${_('Total')}</b></div></td>
        <td><div class="hovblock">${totalThreads}</div></td>
        <td><div class="hovblock">${totalPosts}</div></td>
        <td></td>
    </tr>
</tbody>
</table>

