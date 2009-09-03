# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<div class="errorMessage">
<h1>${_('You are doing it wrong!')}</h1>
${c.errorText}
</div>

%if c.postTitle or c.postMessage or c.postTagLine:
<hr/>
<div class="postblock">
${_('Here is content of your post:')}<br/>
</div>

<div class="reply">
<blockquote class="postbody">

%if c.postTitle:
<b>${_('Title:')}</b> ${c.postTitle}<br/><br/>
%endif

%if c.postMessage:
<b>${_('Message:')}</b><br/>
${c.postMessage}<br/><br/>
%endif

%if c.postTagLine:
<b>${_('Tags:')}</b> ${c.postTagLine}
%endif

</blockquote>
</div>
<hr/>
%endif
