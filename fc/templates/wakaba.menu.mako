%if c.boardlist:
<div class="adminbar">
        [<a href="/~/">~</a>]
    %for section in c.boardlist:
        [
        %for board in section:
            <a href="/${board}/">/${board}/</a>
        %endfor
        ]
    %endfor
	[<a href="/@/">@</a>]
	[<a href="/userProfile/">Profile</a>]
</div>
%endif
