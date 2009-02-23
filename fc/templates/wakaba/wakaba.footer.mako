<br/>
<p class="footer">
    - <a target="_top" href="http://orphereus.anoma.ch/">Orphereus 1.0 alpha</a> -
</p>

%if g.OPT.devMode and c.sum:
<br/>	Total time: ${c.sum} <br/><br/>
%endif

%if g.OPT.devMode and c.log:
<font size="-2">
  %for l in c.log:
    ${l}<br/><br/>
  %endfor
  <div style="display: none"><a href="/holySynod/stat">.</a></div>
</font>
%endif

