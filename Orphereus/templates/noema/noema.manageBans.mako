# -*- coding: utf-8 -*-
<%inherit file="noema.management.mako" />

%if c.message:
<span class="theader">${c.message}</span>
<br /><br />
%endif
                
<a href="${h.url_for('hsBanEdit')}">${_('Add new ban')}</a>

<h2>IP bans</h2>
%if (c.bans):
<table class="hlTable">
    <thead>
        <tr>
            <td class="postblock">${_('ID')}</td>
            <td class="postblock">${_('Active')}</td>
            <td class="postblock">${_('IP')}</td>
            <td class="postblock">${_('Network mask')}</td>
            <td class="postblock">${_('Full ban')}</td>
            <td class="postblock">${_('Reason')}</td>
            <td class="postblock">${_('Date given')}</td>
            <td class="postblock">${_('Period')}</td>
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
%else:
<i>${_('No IP ban records.')}</i>
%endif
<h2>User bans</h2>
%if c.userBans:
<table class="hlTable">
    <thead>
        <tr>
            <td class="postblock">${_('UID')}</td>
            <td class="postblock">${_('Reason')}</td>
            <td class="postblock">${_('Date given')}</td>
            <td class="postblock">${_('Period')}</td>
        </tr>
    </thead>
    <tbody>
    %for e in c.userBans:
        <tr>
            <td><a href="${h.url_for('hsUserEdit', uid=e.uid)}">${e.uid}</a></td>
            <td>${e.reason}</td>
            <td>${e.date}</td>
            <td>${e.time}</td>
        </tr>
    %endfor
    </tbody>
</table>
%else:
<i>${_('No users were banned.')}</i>
%endif
