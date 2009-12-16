# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

%if c.compressingResult:
<pre>
%for line in c.compressingResult:
${line}
%endfor
</pre>
%else:
<form action="${h.url_for('hsRebuildJs')}" method="post">
<label><input type="checkbox" name="joinOnly" />Merge files only. Don't compress.</label><br/>

<label><input type="checkbox" name="useGClosure" />Use Google Closure</label><br/>

<label><input type="checkbox" name="advancedOpt" disabled="disabled" />
Use Closure Advanced Optimizations (<span style="color: red;">dangerous</span>)</label><br/>

<input type="submit" name="rebuildjs" value="Rebuild" />
</form>
%endif
