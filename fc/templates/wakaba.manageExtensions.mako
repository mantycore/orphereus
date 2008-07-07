# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />

<a href="/holySynod/manageExtensions/edit">${_('Add new extension')}</a>
<hr />
<table>
    <thead>
        <tr>
            <td>${_('Extension')}</td>
            <td>${_('Thumb Path')}</td>
            <td>${_('Thumb Resolution')}</td>
            <td>${_('Type')}</td>
        </tr>
    </thead>
    <tbody>
    %for e in c.extensions:
        <tr>
            <td><a href="/holySynod/manageExtensions/edit/${e.ext}">${e.ext}</a></td>
            <td>${e.path}</td>
            <td>${e.thwidth}&#215;${e.thheight}</td>
            <td>${e.type}</td>
        </tr>
    %endfor
    </tbody>
</table>