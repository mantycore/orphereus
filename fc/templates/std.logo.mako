<div class="logo">
    %if c.devmode:
        [DEV]
    %endif
	${c.title}
	%if c.boardName:
		&#151; ${c.boardName}
	%endif
</div>
