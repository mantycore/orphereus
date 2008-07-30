# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />
${_('Current members of Holy Synod')}
<table class="hlTable">
<tr>
<td>Number</td>
<td colspan=4>UID</td>
</tr>
%for u in c.admins:
    <tr>
        <td>${u.uidNumber}</td>    
        <td><a href='/holySynod/manageUsers/edit/${u.uidNumber}'>${"\r\n".join([u.uid[0:64],u.uid[64:128]])}</a></td>
        <td>${u.options.canDeleteAllPosts and "Mod" or ""}</td>
        <td>${u.options.isAdmin and "Admin" or ""}</td>
        <td>${u.options.canMakeInvite and "Invites" or ""}</td>        
    </tr>
%endfor
</table>
