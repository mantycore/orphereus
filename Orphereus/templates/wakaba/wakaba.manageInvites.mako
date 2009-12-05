# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

%if c.inviteCode:
<div class="postarea">
<textarea cols="60" rows="5" readonly="readonly" >
${'http://%s/register/%s' % (g.OPT.baseDomain, c.inviteCode)}
</textarea>
</div>
%else:
<form id="inviteForm" method="post" action="${h.url_for('hsInvite')}">
<table>
    <tr>
        <td>${_('Reason:')}</td>
        <td><input type='text' name='inviteReason' /></td>
    </tr>
    <tr>
        <td>${_('Make user read-only:')}</td>
        <td><input type='checkbox' name='readonly' /></td>
    </tr>
    <tr>
        <td>&nbsp;</td>
        <td><input type='submit' name='generateInvite' value='${_('Generate invite')}' /></td>
    </tr>
</table>
</form>
%if c.inviteList:
  <hr/>
  <table class="hlTable" >
  <thead>
  <tr>
  <td>${_('Id')}</td>
  <td>${_('Issuer')}</td>
  <td>${_('Date')}</td>
  <td>${_('Reason')}</td>
  <td>${_('RO')}</td>
  <td>${_('Code')}</td>
  <td>${_('Management')}</td>
  </tr>
  </thead>
  <tbody>
  %for invite in c.inviteList:
  <tr>
  <td>${invite.id}</td>
  <td>${invite.issuer}</td>
  <td>${h.tsFormat(invite.date)}</td>
  <td>${invite.reason}</td>
  <td>${invite.readonly}</td>
  <td><input type="text" value="${invite.invite}" readonly="readonly" /></td>
  <td><a href="${h.url_for('hsCancelInvite', id=invite.id)}">${_('Cancel')}</a></td>
  </tr>
  %endfor
  </tbody>
  </table>
%endif
%endif
