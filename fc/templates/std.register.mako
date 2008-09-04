# -*- coding: utf-8 -*-
<%inherit file="std.main.mako" />

<div class="postarea">
	<form id="postform" action="/register/doesntmatteranymore" method="post">
        <h2>${_('New UID')}</h2>
         
         <p><i> 
            ${_('Now you can enter your personal security code.')}
            <br/>
            ${_("Warning: you can't use this link twice.")} 
            <br/>
            ${_("If you close browser now you'll loss your ability to join us.")}
            <br/>
         </i></p>
        
		<span class="postblock">${_('Enter your security code')}</span>
        <p><input name="key" type="password" size=60></p> 
        <span class="postblock">${_('Re-enter security code')}</span>
        <p><input name="key2" type="password" size=60></p>                
        <i>${_('Security code should be at least 12 symbols')}</i>
        <p><input type="submit" value="${_('OK')}"></p>                
	</form>
    
</div>
