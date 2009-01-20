<div class="logo">
    %if g.OPT.devMode:
        [DEV]
    %endif
	${c.title}
	%if c.boardName:
		&#151; ${c.boardName}
		%if c.page and isinstance(c.page, int):
		  (${c.page})
		%endif
	%endif
</div>
