# -*- coding: utf-8 -*-

%if c.graphsToShow:
<h3 class="theader"><a style="cursor:pointer; display: block;" onclick="toggle_div('statgraphs');">${_('Traces')}</a></h3>
<div id="statgraphs" style="display: none; text-align: center;">
%for graph in c.graphsToShow:
<img src="${h.staticFile(graph)}" alt="${graph}" /> <br/>
%endfor
</div>
%endif
