%if c.boardlist:
<div class="adminbar">
        [<a href="/~/">~</a>]
    %for section in c.boardlist:
        [
        %for board in section:
            <a href="/${board}/">/${board}/</a>
        %endfor
        ]
    %endfor
	[<a href="/@/">@</a>]
	[<a href="/userProfile/">${_('Profile')}</a>]
    %if c.userInst.isAdmin():
        [<a href="/holySynod/">${_('Holy Synod')}</a>]
    %endif 
    %if c.settingsMap['usersCanViewLogs'].value == 'true':
        [<a href="/viewLog/">${_('Logs')}</a>]
    %endif     
    [<a href="/logout/">${_('Logout')}</a>]
    %if c.userInst.filters():
        <br />
        [
        %for f in c.userInst.filters():
            <a href="/${f.filter}/">/${f.filter}/</a>
        %endfor
        ]
    %endif
</div>
%endif
