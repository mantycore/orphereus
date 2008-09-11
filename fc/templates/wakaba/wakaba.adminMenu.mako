
<a href="/holySynod/manageSettings">${_('Manage settings')}</a><br />
<a href="/holySynod/manageBoards">${_('Manage boards')}</a><br />
<a href="/holySynod/manageUsers">${_('Manage users')}</a><br />
<a href="/holySynod/manageExtensions">${_('Manage extensions')}</a><br />
<a href="/holySynod/manageMappings">${_('Manage mappings')}</a><br />
<!--
<a href="/holySynod/manageQuestions">${_('Manage questions')}</a><br />
<a href="/holySynod/manageApplications">${_('Manage applications')}</a><br />
-->
<a href="/holySynod/viewLog">${_('View logs')}</a><br />
%if c.userInst.canMakeInvite():
<a href="/holySynod/invitePage">${_('Generate invite')}</a><br />
%endif
<a href="/holySynod/service">${_('Maintenance')}</a><br />
