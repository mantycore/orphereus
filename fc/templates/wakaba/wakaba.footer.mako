<br/>
<p class="footer">
    - <a target="_top" href="http://orphereus.anoma.ch/">${g.OPT.version}</a> -
</p>

%if g.OPT.devMode and c.sum:
<br/>	Total time: ${c.sum} <br/><br/>
%endif

%if g.OPT.devMode and c.log:
<font size="-2">
  %for l in c.log:
    ${l}<br/><br/>
  %endfor
  <span style="display: none"><a href="${h.url_for('botTrap2')}">.</a></span>
</font>
%endif

