# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<h2 style="clear: both;">
<span style="float: right;"><a href="/static/rules">Rules</a></span>
<span><a href="/static/markup">Markup and features</a></span>
</h2>

<hr style="clear: both;"/>
<h3>Boards</h3>
<span style="float: right;">
<i>Interesting numbers: ${c.totalPostsCount} [${abs(c.userInst.secid()*c.userInst.secid() - c.totalPostsCount*c.totalPostsCount)}]</i>
</span>
<i>Let my BOARDS go!</i>
<table width="100%" class="hlTable">
    <thead>
        <tr>
            <td style="width: 200px;">${_('Name')}</td>
            <td style="width: 40px;">${_('Threads')}</td>            
            <td style="width: 40px;">${_('Posts')}</td>              
            <td>${_('Description')}</td>
        </tr>
    </thead>
    <tbody>
%for b in c.boards:
        <tr>
            <td><a href="/${b.board.tag}/"><div class="hovblock">${b.board.tag}</div></a></td>
            <td>${b.count}</td>          
            <td>${b.postsCount}</td>               
            <td>
            %if b.board.options and b.board.options.comment:
                ${b.board.options.comment}
            %endif
            </td>  
        </tr>
%endfor 
        <tr>
            <td><div class="hovblock"><b>${_('Total')}</b></div></td>
            <td><div class="hovblock">${c.totalBoardsThreads}</div></td>            
            <td><div class="hovblock">${c.totalBoardsPosts}</div></td>                   
            <td></td>  
        </tr>   
    </tbody>
</table>

<h3>Tags</h3>
<i>Every small TAG has hidden powers. And it has everything to become a BOARD</i>
<table width="100%" class="hlTable">
    <thead>
        <tr>
            <td style="width: 200px;">${_('Name')}</td>
            <td style="width: 40px;">${_('Threads')}</td>
            <td style="width: 40px;">${_('Posts')}</td>                
            <td>${_('Description')}</td>
        </tr>
    </thead>
    <tbody>
%for b in c.tags:
        <tr>
            <td><a href="/${b.board.tag}/"><div class="hovblock">${b.board.tag}</div></a></td>
            <td>${b.count}</td>     
            <td>${b.postsCount}</td>    
            <td>
            %if b.board.options and b.board.options.comment:
                ${b.board.options.comment}
            %endif
            </td>  
        </tr>
%endfor    
        <tr>
            <td><div class="hovblock"><b>${_('Total')}</b></div></td>
            <td><div class="hovblock">${c.totalTagsThreads}</div></td>   
            <td><div class="hovblock">${c.totalTagsPosts}</div></td>                   
            <td></td>  
        </tr>   
    </tbody>
</table>

<hr />
<br clear="all" />
