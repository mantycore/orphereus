# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />
${_('Current members of Holy Synod')}
<table>
%for u in c.admins:
    <tr>
        <td colspan=4><a href='/holySynod/manageUsers/edit/${u.uid_number}'>${u.uid}</a></td>
    </tr>
    <tr>
        <td>${u.uid_number}</td>
        <td>${u.options.canDeleteAllPosts and "Mod" or ""}</td>
        <td>${u.options.isAdmin and "Admin" or ""}</td>
        <td>${u.options.canMakeInvites and "Invites" or ""}</td>
    </tr>
%endfor
</table>