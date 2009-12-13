<div id="boardlist_header">
<div id="overlay_menu" style="position: fixed; top: 0px;" class="reply list" onmouseout="javascript:menu_show('');">
<script>var menu_current = '';</script>
[<a href="#" onmouseover="javascript:menu_show('menu_special');">${_('Special pages')}</a>]
%if c.boardlist:
    %for section in c.boardlist:
        %if section[1]:
          [<a href="#" onmouseover="javascript:menu_show('menu_${h.sectionName(section[1])}');">${section[1]}</a>]
        %else:
          [<a href="#" onmouseover="javascript:menu_show('menu-unnamed_${section[2]}');">${_('Unnamed section %d' % section[2])}</a>]
        %endif
    %endfor
[<a href="#" onmouseover="javascript:menu_show('menu_special2');">${_('User pages')}</a>]
%if len(c.menuLinks):
    [<a href="#" onmouseover="javascript:menu_show('menu_links');">${_('Links')}</a>]
%endif
%if not c.userInst.Anonymous and c.userInst.filters:
    [<a href="#" onmouseover="javascript:menu_show('menu_filters');">${_('Filters')}</a>]
%endif

      <div id="menu_special" style="display:none;" onmouseover="javascript:menu_show('menu_special');"  onmouseout="javascript:menu_show('');">
        %if g.OPT.allowOverview:
        <a href="${h.url_for('boardBase', board='~')}" title="/~/">${_('Overview')}</a>
        %endif
        %if not c.userInst.Anonymous:
        <a href="${h.url_for('boardBase', board='@')}" title="/@/">${_('Related threads')}</a>
        %endif
        <a href="${h.url_for('boardBase', board='!')}" title="/!/">${_('Statistics')}</a>
      </div>

    %for section in c.boardlist:
      %if section[1]:
        <div id="menu_${h.sectionName(section[1])}" style="display:none;" onmouseover="javascript:menu_show('menu_${h.sectionName(section[1])}');"  onmouseout="javascript:menu_show('');">
      %else:
        <div id="menu-unnamed_${section[2]}" style="display:none;" onmouseover="javascript:menu_show('menu-unnamed_${section[2]}');"  onmouseout="javascript:menu_show('');">
      %endif
        %for board in section[0]:
        <a href="${h.url_for('boardBase', board=board.tag)}" title="${board.comment}"><b>/${board.tag}/</b>
        %if board.comment:
        &mdash; ${board.comment}
        %endif
        </a>
        %endfor
      </div>
    %endfor
%endif

  <div id="menu_special2" style="display:none;" onmouseover="javascript:menu_show('menu_special2');"  onmouseout="javascript:menu_show('');">
    <div>${_("Preferences")}</div>
    %if not c.userInst.Anonymous:
        <a href="${h.url_for('userProfile')}">${_('Profile')}</a>
    %elif g.OPT.allowAnonProfile:
        <a href="${h.url_for('userProfile')}">${_('Settings')}</a>
    %endif
    <a href="${h.url_for('ajChangeOption', name='useFrame', value=not c.userInst.useFrame, returnTo=c.currentURL)}">
    ${c.userInst.useFrame and _("Turn frame off") or _("Turn frame on")}
    </a>

    <div>${_("Style")}</div>
    %for style in c.styles:
    <a onclick="changeCSS(event, '${style}', '${h.staticFile(style + ".css")}')" \
    href="${h.url_for('ajChangeOption', name='style', value=style, returnTo=c.currentURL)}">
    ${style}
    </a>
    %endfor
    <hr/>
    %if c.userInst.isAdmin():
        <a href="${h.url_for('holySynod')}">${_('Holy Synod')}</a>
    %endif
    %if g.OPT.usersCanViewLogs:
        <a href="${h.url_for('viewLogBase')}">${_('Logs')}</a>
    %endif

    %if not c.userInst.Anonymous:
    <a href="${h.url_for('logout')}" target="_top" onclick="parent.top.list.location.reload(true);">${_('Logout')}</a>
    %else:
        %if g.OPT.allowLogin:
            %if c.currentURL:
                <a href="${h.url_for('authorizeToUrl', url=c.currentURL)}">${_('Login')}</a>
            %else:
                <a href="${h.url_for('authorize')}">${_('Login')}</a>
            %endif
        %endif
        <a href="${h.url_for('logout')}" target="_top" onclick="parent.top.list.location.reload(true);">${_('Kill session')}</a>
    %if g.OPT.allowRegistration:
      <a href="${h.url_for('register', invite='register')}">${_('Register')}</a>
    %endif
    %endif
    </div>

%if c.menuLinks:
  <div id="menu_links" style="display:none;" onmouseover="javascript:menu_show('menu_links');"  onmouseout="javascript:menu_show('');">
    %for link in c.menuLinks:
        % if isinstance(link, list) and len(link) == 2:
        <a href="${link[0]}">${link[1]}</a>
        %endif
    %endfor
    </div>
%endif

%if not c.userInst.Anonymous and c.userInst.filters:
  <div id="menu_filters" style="display:none;" onmouseover="javascript:menu_show('menu_filters');"  onmouseout="javascript:menu_show('');">
    %for f in c.userInst.filters:
        <a href="${h.url_for('boardBase', board=f.filter)}">/${f.filter}/</a>
    %endfor
    </div>
%endif
</div></div>
<br />
