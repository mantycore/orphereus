# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<div class="postarea">
%if c.message:
<h3 class="errorMessage">
  ${c.message}
</h3>
%endif

%if c.invites:
  <table class="hlTable" >
  <thead>
  <tr>
  <td>${_('Id')}</td>
  <td>${_('Date')}</td>
  <td>${_('Reason')}</td>
  <td>${_('Link')}</td>
  </tr>
  </thead>
  <tbody>
  %for invite in c.invites:
  <tr>
  <td>${invite.id}</td>
  <td>${h.tsFormat(invite.date)}</td>
  <td>${invite.reason}</td>
  <td><input type="text" value="${'http://%s/register/%s' % (g.OPT.baseDomain, invite.invite)}" readonly="readonly" /></td>
  </tr>
  %endfor
  </tbody>
  </table>
%else:
<div class="theader">${_("You haven't created any invites.")}</div>
%endif

</div>
<form id="inviteform" action="${h.url_for('userInvitesManager', act='create')}" method="post">
<hr/>
<table align="center">
    <tr>
        <td>${_('Reason:')}</td>
        <td><input type='text' name='invitereason' /></td>
    </tr>
    <tr>
        <td>&nbsp;</td>
        <td><input name="create" type="submit" value="${_('Make an invitation (%d left)') % c.invitesCount}" \
        %if not c.invitesCount:
        disabled="disabled" \
        %endif
        /></td>
    </tr>
</table>

</form>
<hr/>
<br clear="all" />
