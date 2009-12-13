<%page args="menuId, menuSource, currentItemId = False"/>

<hr/>
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
<hr/>
