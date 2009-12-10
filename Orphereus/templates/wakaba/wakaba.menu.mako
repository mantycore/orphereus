<div class="adminbar">
<span class="boardlist">
${h.boardMenu([h.itemsToSection(
  [
    (_('Overview'), '~', g.OPT.allowOverview, h.url_for('boardBase', board='~')),
    (_('Related threads'), '@', not c.userInst.Anonymous, h.url_for('boardBase', board='@')),
    (_('My threads'), '*', not c.userInst.Anonymous, h.url_for('boardBase', board='*')),
    (_('Home'), '!', True, h.url_for('boardBase', board='!')),
  ]
  )], False
)}

%if c.boardlist:
%if g.OPT.spiderTrap:
<span style="display: none"><a href="${h.url_for('botTrap1', confirm=c.userInst.secid())}">...</a><a href="${h.url_for('botTrap2', confirm=c.userInst.secid())}">.</a></span>
%endif
  ${h.boardMenu(c.boardlist)}
%endif
</span>

<div class="CSSMenu">
<ul>
  <li>
%if not c.userInst.Anonymous:
    [<a href="${h.url_for('userProfile')}">${_('Profile')}</a>]
%elif g.OPT.allowAnonProfile:
    [<a href="${h.url_for('userProfile')}">${_('Settings')}</a>]
%endif
    <ul class="CSSMenuBase">
      <li>
      %if not c.userInst.Anonymous:
          <a href="${h.url_for('userProfile')}">${_('Profile')}</a>
      %elif g.OPT.allowAnonProfile:
          <a href="${h.url_for('userProfile')}">${_('Settings')}</a>
      %endif
      </li>
      <li><span class="CSSMenuHeader">${_("Quick switch")}</a></li>
      <li><a href="${h.url_for('ajChangeOption', name='useFrame', value=not c.userInst.useFrame, returnTo=c.currentURL)}">
      ${c.userInst.useFrame and _("Turn frame off") or _("Turn frame on")}
      </a></li>
      <li><span class="CSSMenuHeader">${_("Style")}</a></li>
      %for style in c.styles:
      <li><a onclick="changeCSS(event, '${style}', '${h.staticFile(style + ".css")}')" \
      href="${h.url_for('ajChangeOption', name='style', value=style, returnTo=c.currentURL)}">
      ${style}
      </a></li>
      %endfor
    </ul>
  </li>

  <li>
    [<a href="#">${_('Links')}</a>]
    <ul class="CSSMenuBase">
          <li><span class="CSSMenuHeader">${_("Special")}</a></li>
      %if c.userInst.isAdmin():
          <li><a href="${h.url_for('holySynod')}">${_('Holy Synod')}</a></li>
      %endif
      %if g.OPT.usersCanViewLogs:
          <li><a href="${h.url_for('viewLogBase')}">${_('Logs')}</a></li>
      %endif
          <li><span class="CSSMenuHeader">${_("Other")}</a></li>
      %if c.menuLinks:
          %for link in c.menuLinks:
              %if isinstance(link, list) and len(link) == 2:
              <li><a href="${link[0]}">${link[1]}</a></li>
              %endif
          %endfor
      %endif
    </ul>
  </li>
</ul>
</div>

<!--
%if c.userInst.isAdmin():
    [<a href="${h.url_for('holySynod')}">${_('Holy Synod')}</a>]
%endif
%if g.OPT.usersCanViewLogs:
    [<a href="${h.url_for('viewLogBase')}">${_('Logs')}</a>]
%endif
%if c.menuLinks:
    %for link in c.menuLinks:
        %if isinstance(link, list) and len(link) == 2:
        [<a href="${link[0]}">${link[1]}</a>]
        %endif
    %endfor
%endif
-->
%if not c.userInst.Anonymous:
[<a href="${h.url_for('logout')}" target="_top" onclick="parent.top.list.location.reload(true);">${_('Logout')}</a>]
%else:
    %if g.OPT.allowLogin:
        %if c.currentURL:
            [<a href="${h.url_for('authorizeToUrl', url=c.currentURL)}">${_('Login')}</a>]
        %else:
            [<a href="${h.url_for('authorize')}">${_('Login')}</a>]
        %endif
    %endif
    [<a href="${h.url_for('logout')}" target="_top" onclick="parent.top.list.location.reload(true);">${_('Kill session')}</a>]
%if g.OPT.allowRegistration:
[<a href="${h.url_for('register', invite='register')}">${_('Register')}</a>]
%endif
%endif
%if not c.userInst.Anonymous and c.userInst.filters:
    <br />
    [ \
    %for f in c.userInst.filters:
        <a href="${h.url_for('boardBase', board=f.filter)}">/${f.filter}/</a> \
    %endfor
    ]
%endif
</div>


