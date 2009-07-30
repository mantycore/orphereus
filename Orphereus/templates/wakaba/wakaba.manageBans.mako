# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

%if c.message:
<span class="theader">${c.message}</span>
<br /><br />
%endif
                
<a href="${h.url_for('hsBanEdit')}">${_('Add new ban')}</a>

<table class="hlTable">
    <thead>
        <tr>
            <td>${_('ID')}</td>
            <td>${_('Active')}</td>
            <td>${_('IP')}</td>
            <td>${_('Network mask')}</td>
            <td>${_('Full ban')}</td>
            <td>${_('Reason')}</td>
            <td>${_('Date given')}</td>
            <td>${_('Period')}</td>
        </tr>
    </thead>
    <tbody>
    %for e in c.bans:
        <tr>
            <td><a href="${h.url_for('hsBanEdit', id=e.id)}">${e.id}</a></td>
            <td align="center">${e.enabled and "&#8226;" or ""}</td>
            <td>${h.intToIp(e.ip)}</td>
            <td>${h.intToIp(e.mask)}</td>
            <td>${e.type and _("yes") or _("no")}</td>
            <td>${e.reason}</td>
            <td>${e.date}</td>
            <td>${e.period}</td>
        </tr>
    %endfor
    </tbody>
</table>
