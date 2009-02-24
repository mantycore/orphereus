# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />
${_('Current members of Holy Synod')}
<table class="hlTable">
<tr>
<td>Number</td>
<td><b>Rights</b></td>
<td>Mod</td>
<td>Invites</td>
<td>Opt</td>
<td>Boards</td>
<td>Users</td>
<td>Ext</td>
<td>Mapping</td>
<td>Maint</td>
</tr>
%for u in c.admins:
    <tr>
        <td
            %if u.uidNumber == c.userInst.uidNumber:
            class="highlight"
            %endif
        ><div class="hovblock"><a style="display: block;" href='/holySynod/manageUsers/edit/${u.uidNumber}'>${u.uidNumber}</a></div></td>
        <td>${u.canChangeRights() and "&#8226;" or ""}</td>
        <td>${u.canDeleteAllPosts() and "&#8226;" or ""}</td>
        <td>${u.canMakeInvite() and "&#8226;" or ""}</td>
        <td>${u.canChangeSettings() and "&#8226;" or ""}</td>
        <td>${u.canManageBoards() and "&#8226;" or ""}</td>
        <td>${u.canManageUsers() and "&#8226;" or ""}</td>
        <td>${u.canManageExtensions() and "&#8226;" or ""}</td>
        <td>${u.canManageMappings() and "&#8226;" or ""}</td>
        <td>${u.canRunMaintenance() and "&#8226;" or ""}</td>
    </tr>
%endfor
</table>
