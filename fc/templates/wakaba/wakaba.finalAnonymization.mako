# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<div class="errorMessage"> 
<h1>${_('Final Anonymization')}</h1>

%if not c.FAResult:
<p>You are trying to anonymize post #${c.postId}.</p>
<p>This action will remove mapping to your UID. You will loss abilities to:</p>
<ol>
<li>delete this post</li>
<li>view this post in <a href="/@">/@/</a></li>
<li>use ID of this posts in prooflabels</li>
</ol>
<h3>Do you want to continue?</h3>

<form action="/${c.postId}/anonymize" method="post">
    <input type="hidden" name="postId" value="${c.postId}">
    <input type="submit" value="${_('Yes, I want!')}">
</form>
%else:
<h3>Result</h3>
${c.FAResult}
%endif

</div>