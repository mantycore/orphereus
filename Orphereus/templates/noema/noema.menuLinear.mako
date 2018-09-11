<%page args="menuId, menuSource, currentItemId = False"/>

%if menuSource:
%for item in menuSource[menuId]:
  %if item[0].route:
    <a href="${item[0].route}"
      class="menuLinearItem menuItem_${item[1]}"
      style="
      %if currentItemId and currentItemId == item[0].id:
        color: green;
      %endif
      padding-left: ${item[1]*8}px;
          display: block;
      "
          id="${item[0].id}"
    >
     ${item[0].text}
    </a>
  %else:
    <span
      class="menuLinearSpan menuSpan_${item[1]}"
      style="
      %if currentItemId and currentItemId == item[0].id:
        color: green;
      %endif
      padding-left: ${item[1]*8}px;
          display: block;
      "
          id="${item[0].id}"
    >
     ${item[0].text}
    </span>
  %endif
%endfor
%endif

