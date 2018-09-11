<%inherit file="noema.main.mako" />

<div class="theader">
%if c.loginSuccessful:
<h1>${_('Successfully logged in')}</h1>
%else:
<h1>${_('Incorrect security code')}</h1>
%endif
<h2><a href="${h.url_for('boardBase', board = c.currentURL)}">Continue</a></h2>
</div>
