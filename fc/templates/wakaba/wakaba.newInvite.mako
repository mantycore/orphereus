# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />

%if c.inviteCode:
<div class="postarea">
<textarea cols="60" rows="5" readonly wrap="virtual">
${'http://%s/register/%s' % (g.OPT.baseDomain, c.inviteCode)}
</textarea>
</div>
%else:
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
%endif