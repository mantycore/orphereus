<br/>
<p class="footer"> 
    - <a target="_top" href="http://orphereus.anoma.ch/">Orphereus 0.9</a> -<br/>
    [<a target="_top" href="/static/donate">Donate</a>]
</p>

%if g.OPT.devMode and c.log:
	%for l in c.log:
		${l}<br/>
	%endfor
%endif