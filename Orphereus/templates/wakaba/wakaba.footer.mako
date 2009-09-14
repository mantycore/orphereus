<br/>
<p class="footer">
- <a target="_top" href="http://orphereus.anoma.ch/">${g.version}</a> -
%if g.OPT.recoveryMode:
<br/><i>recovery mode</i><br/><br/>
%endif
</p>

%if g.OPT.devMode and c.sum:
<br/>  Total time: ${c.sum} <br/><br/>
%endif


%if g.OPT.devMode and c.log:
<font size="-2">
%for l in c.log:
${l}<br/><br/>
%endfor
${"rendering: %s" % str(h.currentTime() - c.renderStartTime)}
%if g.OPT.memcachedPosts:
  memcached
%endif
<br />
${"total: %s" % str(h.currentTime() - c.processStartTime)} (${"render %s%% time" % str((h.currentTime() - c.renderStartTime)*100/(h.currentTime() - c.processStartTime))})
<br />request profiling: ${g.OPT.requestProfiling}
<span style="display: none"><a href="${h.url_for('botTrap2', confirm=c.userInst.secid())}">.</a></span>
</font>
%endif

