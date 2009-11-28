# -*- coding: utf-8 -*-

%if c.graphsToShow:
<h3 class="theader"><a style="cursor:pointer; display: block;" onclick="toggle_div('statgraphs');">${_('Traces')}</a></h3>
<div id="statgraphs" style="text-align: center;">
%for graph in c.graphsToShow:
<a href="${h.staticFile(graph[1])}"><img src="${h.staticFile(graph[0])}" alt="${graph}" /></a>
%endfor
</div>
%endif
