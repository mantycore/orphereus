<div class="logo">
    %if g.OPT.devMode:
        [DEV]
    %endif
	%if (g.OPT.useFrameLogo and not(c.boardName)):        
		<div align="center"><a href="${g.OPT.defaultFrame}" target="board"><img src="/logo.png" alt="${c.title}" /></a></div>
	%endif
	%if not(g.OPT.useFrameLogo and not(c.boardName)):        
		${c.title}
		%if c.boardName:
			&mdash; ${c.boardName}
			%if c.page and isinstance(c.page, int):
			  (${c.page})
			%endif
		%endif
	%endif	
</div>
