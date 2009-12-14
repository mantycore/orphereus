<%page args="menuId, menuSource, bottomMenu = False"/>

<div class="adminbar">
<div class="boardlist">

%if g.OPT.spiderTrap:
<span style="display: none"><a href="${h.url_for('botTrap1', confirm=c.userInst.secid())}">...</a><a href="${h.url_for('botTrap2', confirm=c.userInst.secid())}">.</a></span>
%endif

%if menuSource:
%for item in menuSource[menuId][False]: # sections
%if menuSource[menuId].get(item.id, None):
  <!-- ${item.text} -->
  %if not item.collapse:
   [${h.renderNCTop(menuSource[menuId][item.id], menuSource[menuId])}]
  %else:
    <div class="${bottomMenu and 'CSSMenu CSSMenuBottom' or 'CSSMenu'}">
    <ul>
      %for subitem in menuSource[menuId][item.id]: # links in sections
      <li>
        [<b><a href="${subitem.route or '#'}">${subitem.text}</a></b>]
        <ul class="CSSMenuBase">
          %for subitem in menuSource[menuId][item.id]: # links in sections
            %if menuSource[menuId].get(subitem.id, None):
                <li>
                %for subsubitem in menuSource[menuId].get(subitem.id, None):
                  %if subsubitem.route:
                  ${h.renderCollapsedLink(subsubitem)}
                  %else:
                  <span class="CSSMenuHeader"><b>${subsubitem.text}</b></span>
                  %endif
                %endfor
                 </li>
            %endif
          %endfor
        </ul>
      </li>
      %endfor
    </ul>
    </div>
  %endif

%endif
%endfor
%endif

</div>
%if not c.userInst.Anonymous and c.userInst.filters:
    <br />
    [ \
    %for f in c.userInst.filters:
        <a href="${h.url_for('boardBase', board=f.filter)}">/${f.filter}/</a> \
    %endfor
    ]
%endif
</div>
