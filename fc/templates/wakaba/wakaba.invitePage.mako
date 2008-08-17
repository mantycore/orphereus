# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />

<div class="postarea">
    <form id="inviteForm" method="post" action="makeInvite">
<table>    
    <tr>
        <td>Reason:</td>
        <td><input type='text' name='inviteReason'></td>
    </tr>
    <tr>        
        <td>&nbsp;</td>
        <td><input type='submit' name='generateInvite' value='${_('Generate invite')}'></td>
    </tr>
</table>        
    </form>                 
</div>
