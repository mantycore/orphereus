
%if c.userInst.canChangeSettings():
<a href="${h.url_for('hsSettings')}">${_('Manage settings')}</a><br />
%endif

%if c.userInst.canManageBoards():
<a href="${h.url_for('hsBoards')}">${_('Manage boards')}</a><br />
%endif

%if c.userInst.canManageUsers():
<a href="${h.url_for('hsUsers')}">${_('Manage users')}</a><br />
%endif

%if c.userInst.canManageUsers():
<a href="${h.url_for('hsBans')}">${_('Manage bans')}</a><br />
%endif

%if c.userInst.canManageExtensions():
<a href="${h.url_for('hsExtensions')}">${_('Manage extensions')}</a><br />
%endif

%if c.userInst.canManageMappings():
<a href="${h.url_for('hsMappings')}">${_('Manage mappings')}</a><br />
%endif

<a href="${h.url_for('hsViewLogBase')}">${_('View logs')}</a><br />

%if c.userInst.canMakeInvite():
<a href="${h.url_for('hsInvite')}">${_('Generate invite')}</a><br />
%endif

%if c.userInst.canRunMaintenance():
<a href="${h.url_for('hsMaintenance')}">${_('Maintenance')}</a><br />
%endif
