<div class="adminbar">
    [
    <a href="${h.url_for('board', board='~')}" title="${_('Overview')}">/~/</a>
    %if not c.userInst.Anonymous:
    <a href="${h.url_for('board', board='@')}" title="${_('Related threads')}">/@/</a>
    %endif
    <a href="${h.url_for('board', board='!')}" title="${_('Home')}">/!/</a>
    ]

%if c.boardlist:
%if g.OPT.spiderTrap:
<span style="display: none"><a href="${h.url_for('botTrap1', confirm=c.userInst.secid())}">...</a><a href="${h.url_for('botTrap1')}">.</a></span>
%endif
    %for section in c.boardlist:
        [
        %for board in section:
            <a href="${h.url_for('board', board=board.tag)}" title="${board.comment}"><b>/${board.tag}/</b></a>
        %endfor
        ]
    %endfor
    %if not c.userInst.Anonymous:
        [<a href="${h.url_for('userProfile')}">${_('Profile')}</a>]
    %elif g.OPT.allowAnonProfile:
        [<a href="${h.url_for('userProfile')}">${_('Settings')}</a>]
    %endif
    %if c.userInst.isAdmin():
        [<a href="${h.url_for('holySynod')}">${_('Holy Synod')}</a>]
    %endif
    %if g.settingsMap['usersCanViewLogs'].value == 'true':
        [<a href="${h.url_for('viewLog')}">${_('Logs')}</a>]
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
    [<a href="${h.url_for('logout')}">${_('Logout')}</a>]
    %else:
        %if g.OPT.allowLogin:
            %if c.currentURL:
                [<a href="${h.url_for('authorizeToUrl', url=c.currentURL)}">${_('Login')}</a>]
            %else:
                [<a href="${h.url_for('authorize')}">${_('Login')}</a>]
            %endif
        %endif
        [<a href="${h.url_for('logout')}">${_('Kill session')}</a>]
    %if g.OPT.allowRegistration:
    [<a href="/register/register">${_('Register')}</a>]
    %endif
    %endif
    %if not c.userInst.Anonymous and c.userInst.filters:
        <br />
        [
        %for f in c.userInst.filters:
            <a href="/${f.filter}/">/${f.filter}/</a>
        %endfor
        ]
    %endif
</div>
