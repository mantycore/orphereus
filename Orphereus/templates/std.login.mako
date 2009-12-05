# -*- coding: utf-8 -*-
<%inherit file="std.main.mako" />

%if not h.templateExists(c.actuatorTest+'std.login.mako'):
<div class="postarea">
  <form id="postform" action="${h.url_for('authorizeToUrl', url=c.currentURL)}" method="post">
    <span class="postblock">${_('Enter your security code')}</span>
    <p style="display: none;"><input name="login" type="text" size="60" value="dummy" /></p>
    <p><input name="password" type="password" size="60" style="text-align: center" /></p>
        %if c.showCaptcha:
            <p class="postblock">${_('Too many login attempts. Enter CAPTCHA please')}</p>
            <div><img src="${h.url_for('captcha', cid=c.captcha.id)}" alt="Captcha" style="border: #964600 2px solid;"/></div>
            <p><input name="captcha" size="32" style="text-align: center"/></p>
            <p><input name="captid" type="hidden" value="${c.captcha.id}"/></p>
        %endif
    <p><input type="submit" value="${_('OK')}"/></p>
  </form>
</div>
%else:
    <%include file="${c.actuator+'std.login.mako'}" />
%endif

<div style="text-align: center;">
%if g.OPT.allowRegistration:
  <a href="${h.url_for('register', invite='register')}"><strong>${_('Register')}</strong></a><br /><br />
%endif

%if h.templateExists(c.actuatorTest+'std.login_bottom.mako'):
   <%include file="${c.actuator+'std.login_bottom.mako'}" />
%endif
</div>

