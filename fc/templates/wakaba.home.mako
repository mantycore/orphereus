# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<h2 style="text-align: center;"><a href="/static/rules">Rules</a> <a href="/static/Markup">Markup</a></h2>
<hr />

<h3>Boards</h3>
<i>Let my BOARDS go!</i>
<table width="100%" class="hlTable">
    <thead>
        <tr>
            <td style="width: 200px;">${_('Name')}</td>
            <td>${_('Description')}</td>
        </tr>
    </thead>
    <tbody>
%for b in c.boards:
        <tr>
            <td><a href="/${b.tag}/"><div class="hovblock">${b.tag}</div></a></td>
            <td>
            %if b.options and b.options.comment:
                ${b.options.comment}
            %endif
            </td>  
        </tr>
%endfor    
    </tbody>
</table>

<h3>Tags</h3>
<i>Every small TAG has hidden powers. And it have all abilities to became a BOARD.</i>
<table width="100%" class="hlTable">
    <thead>
        <tr>
            <td style="width: 200px;">${_('Name')}</td>
            <td>${_('Description')}</td>
        </tr>
    </thead>
    <tbody>
%for b in c.tags:
        <tr>
            <td><a href="/${b.tag}/"><div class="hovblock">${b.tag}</div></a></td>
            <td>
            %if b.options and b.options.comment:
                ${b.options.comment}
            %endif
            </td>   
        </tr>
%endfor    
    </tbody>
</table>

<hr />
<br clear="all" />
