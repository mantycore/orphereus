# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />
${_('Current members of Holy Synod')}
<table>
%for u in c.admins:
    <tr>
        <td colspan=5><a href='/holySynod/manageUsers/edit/${u.uidNumber}'>${"\r\n".join([u.uid[0:64],u.uid[64:128]])}</a></td>
    </tr>
    <tr>
        <td>${u.uidNumber}</td>
        <td>${u.options.canDeleteAllPosts and "Mod" or ""}</td>
        <td>${u.options.isAdmin and "Admin" or ""}</td>
        <td>${u.options.canMakeInvite and "Invites" or ""}</td>
        <td></td>
    </tr>
%endfor
</table>
