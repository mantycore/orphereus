# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />

<div class="postarea">
    <form id="userEditReasonForm" method="post" action="/holySynod/manageUsers/editUserByPost/${c.pid}">
<table>    
    <tr>
        <td>Reason:</td>
        <td><input type='text' name='UIDViewReason'></td>
    </tr>
    <tr>        
        <td>&nbsp;</td>
        <td><input type='submit' name='editUser' value='${_('Show user info')}'></td>
    </tr>
</table>        
    </form>                 
</div>
