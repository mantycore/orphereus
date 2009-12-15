<%inherit file="std.main.mako" />
<div align="center">
<h2>${_('Invitation request')}</h2>
%if c.message:
    ${c.message}
%endif
</div>
<br /><br />
%if not(c.hideform) :
    <div class="postarea">
    <form id="postform" action="${h.url_for('invRequest')}" method="post">
    <span class="postblock">${_('Enter your e-mail/jabber address')}</span><br/>
    <input type="text" name="mail" value="${c.mail}" /><br /><br/>
    <span class="postblock">${_('Enter request details')}</span><br/>
    <textarea name="text" cols="45" rows="6" >${c.text}</textarea>
    %if c.captcha:
        <br/>
        <span class="postblock">${_('Enter captcha')}</span>
        <div><img src="${h.url_for('captcha', cid=c.captcha.id)}" alt="Captcha" /></div>
        <p><input name="captcha" type="text" size="60" /></p>
    %endif
    <p><input type="submit" value="${_('OK')}" /></p>
    </form>
    </div>
%endif
