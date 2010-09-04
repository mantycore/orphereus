# -*- coding: utf-8 -*-
          <input type="hidden" name="task" value="delete" />
          %if c.isAdmin:
            ${_('Reason')}: <input type="text" name="reason" size="35" />
           %endif

            %if c.userInst.Anonymous:
                ${_('Password')}: <input type="password" name="remPass" size="10" value="${c.remPass}" title="${_("Correct password only required if session in which post was made already expired/deleted")}" />
            %endif
            [<label><input type="checkbox" name="fileonly" value="on" />${_('Only file')}</label>]
            <input name="task_delete" value="${_('Delete post(s)')}" type="submit" />