# -*- coding: utf-8 -*-
<%inherit file="noema.main.mako" />

<div class="errorMessage">
<h1>${_('Final Anonymization')}</h1>

%if not c.FAResult:
<form action="${h.url_for('anonymize', post=c.postId)}" method="post">
    <p>${_("You are trying to anonymize post #%s.") % c.postId}</p>
    <h3><input type="checkbox" name="batchFA">${_('Anonymize ALL posts older than this one')}</h3>
    <p>${_("This action will remove mapping to your UID. You will loss abilities to:")}</p>
    <ol>
    <li>${_("delete this post")}</li>
    <li>${_('view this post in <a href="%s">/@/</a>') % h.url_for('boardBase', board='@')} </li>
    <li>${_("use ID of this post in prooflabels")}</li>
    </ol>
    <h3>${_("Do you want to continue?")}</h3>

    <input type="hidden" name="postId" value="${c.postId}">
    <p><input type="submit" value="${_('Yes, I want!')}"></p>
</form>

%else:
<h3>${_("Result")}</h3>
%for res in c.FAResult:
${res}<br/>
%endfor
%endif

</div>
