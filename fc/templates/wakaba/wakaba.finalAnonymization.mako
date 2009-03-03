# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<div class="errorMessage">
<h1>${_('Final Anonymization')}</h1>

%if not c.FAResult:
<form action="/${c.postId}/anonymize" method="post">
    <p>You are trying to anonymize post #${c.postId}.</p>
    <h3><input type="checkbox" name="batchFA">${_('Anonymize ALL posts older than this one')}</h3>
    <p>This action will remove mapping to your UID. You will loss abilities to:</p>
    <ol>
    <li>delete this post</li>
    <li>view this post in <a href="/@">/@/</a></li>
    <li>use ID of this posts in prooflabels</li>
    </ol>
    <h3>Do you want to continue?</h3>

    <input type="hidden" name="postId" value="${c.postId}">
    <p><input type="submit" value="${_('Yes, I want!')}"></p>
</form>

%else:
<h3>Result</h3>
%for res in c.FAResult:
${res}<br/>
%endfor
%endif

</div>
