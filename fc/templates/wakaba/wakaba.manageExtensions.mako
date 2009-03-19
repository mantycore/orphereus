# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

<form id="postform" method="post" action="">
%if not c.showCount:
<input type="submit" value="${_('Show statistics')}" name="showCount"/>
%endif
<a href="${h.url_for('hsExtensionEdit')}">${_('Add new extension')}</a>
</form>

<hr />

<table class="hlTable">
    <thead>
        <tr>
            <td>${_('Extension')}</td>
            <td>${_('Type')}</td>
            <td>${_('Thumb Resolution')}</td>
            <td>${_('Thumb Path')}</td>
            <td>${_('Enabled')}</td>
            <td>${_('New window')}</td>
            %if c.showCount:
            <td>${_('Files posted')}</td>
            %endif
        </tr>
    </thead>
    <tbody>
    %for e in c.extensions:
        <tr>
            <td><a href="${h.url_for('hsExtensionEdit', name=e.ext)}">${e.ext}</a></td>
            <td>${e.type}</td>
            <td>${e.thwidth}&#215;${e.thheight}</td>
            <td>${e.path}</td>
            <td>${e.enabled and _("yes") or _("no")}</td>
            <td>${e.newWindow and _("yes") or _("no")}</td>
            %if c.showCount:
            <td>${e.count()}</td>
            %endif
        </tr>
    %endfor
    </tbody>
</table>
