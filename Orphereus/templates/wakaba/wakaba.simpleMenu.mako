<%page args="menuId, menuSource, currentItemId = False"/>

%if menuSource:
%for item in menuSource[menuId]:
	%if item[0].route:
		<a href="${item[0].route}" 
		  class="menuItem_${item[1]}"
		  style="
		  %if currentItemId and currentItemId == item[0].id:
		  	color: green;
		  %endif
		  padding-left: ${item[1]*8}px;
		  " 
		> 
		 ${item[0].text}
		</a><br/>
	%else:
		<span 
		  class="menuSpan_${item[1]}"
		  style="
		  %if currentItemId and currentItemId == item[0].id:
		  	color: green;
		  %endif
		  padding-left: ${item[1]*8}px;
		  "  
		> 
		 ${item[0].text}
		</span><br/>
	%endif		
%endfor 
%endif