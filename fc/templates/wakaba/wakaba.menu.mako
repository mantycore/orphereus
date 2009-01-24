<div class="adminbar">
    [
    <a href="/~/" title="${_('Overview')}">/~/</a>
    %if not c.userInst.Anonymous:
    <a href="/@/" title="${_('Related threads')}">/@/</a>
    %endif
    <a href="/!/" title="${_('Home')}">/!/</a>    
    ]    
    
%if c.boardlist:
%if g.OPT.spiderTrap:    
<div style="display: none"><a href="/ajax/stat/${c.userInst.secid()}">...</a><a href="/ajax/stat">.</a></div>
%endif        
    %for section in c.boardlist:
        [
        %for board in section:
            <a href="/${board.tag}/" title="${board.comment}"><b>/${board.tag}/</b></a>
        %endfor
        ]
    %endfor
    %if not c.userInst.Anonymous:
	[<a href="/userProfile/">${_('Profile')}</a>]
    %endif
    %if c.userInst.isAdmin():
        [<a href="/holySynod/">${_('Holy Synod')}</a>]
    %endif 
    %if g.settingsMap['usersCanViewLogs'].value == 'true':
        [<a href="/viewLog/">${_('Logs')}</a>]
    %endif     
    %if c.menuLinks:
        %for link in c.menuLinks:
            % if isinstance(link, list) and len(link) == 2:
            [<a href="${link[0]}">${link[1]}</a>]
            %endif
        %endfor
    %endif
%endif

    [<a target="_blank" href="/static/donate">Donate</a>]
    %if not c.userInst.Anonymous:
    [<a href="/logout/">${_('Logout')}</a>]
    %else:
    [<a href="/authorize">${_('Login')}</a>]
    %if g.OPT.allowRegistration:
    [<a href="/register/register">${_('Register')}</a>]
    %endif 
    %endif
    %if not c.userInst.Anonymous and c.userInst.filters():
        <br />
        [
        %for f in c.userInst.filters():
            <a href="/${f.filter}/">/${f.filter}/</a>
        %endfor
        ]
    %endif
</div>
