# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<div style="text-align: center;">    
<h2 style="margin: 0;">Orphie-Mark</h2>
<i>(Разметка)</i>
</div>
<table width="80%" class="hlTable" align="center">
    <thead>
        <tr>
            <td style="width:50%;"><b>Входит</b></td>
            <td style="width:50%;"><b>Выходит</b></td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left">*курсивная надпись* или _курсивная надпись_</td>
            <td align="left"><em>курсивная надпись</em></td>
        </tr>
        <tr>
            <td align="left">**полужирный текст** или __полужирный текст__</td>
            <td align="left"><strong>полужирный текст</strong></td>
        </tr>
        <tr>
            <td align="left">`код`</td>
            <td align="left"><tt>код</tt></td>
        </tr>
        <tr>
            <td align="left">``код` с `бэктиками``</td>
            <td align="left"><tt>код` с `бэктиками</tt></td>
        </tr>
        <tr>
            <td align="left">>>номер</td>
            <td align="left">ссылка на пост</td>
        </tr>
        <tr>
            <td align="left">##номер1 или ##номер1,номер2,...</td>
            <td align="left">Подпись, она же пруфметка.<br/><br/>
            <font style="font-size: 90%">
            <b>Пример использования:</b> <br/>
            Допустим, вы написали посты с номерами 10 и 20, а посты с номерами 40 и 50 написаны другим человеком.<br/>
            В таком случае написав <br/>
            <code>##10,20,40,50</code> <br/>
            вы получите на выходе<br/>
            
            <p>
            <span class="badsignature">##<a href=".">40</a>,<a href=".">50</a></span>,<span class="signature"><a href=".">10</a>,<a href=".">20</a></span>
            </p>            
          
            </font>
            </td>
        </tr>
        <tr>
            <td align="left">%%спойлер%%</td>
            <td align="left"><span class="spoiler">спойлер</span></td>
        </tr>
        <tr>
            <td align="left">%%<br/>блок спойлера<br/>%%</td>
            <td align="left">
                <div class="spoiler">
                <p> спойлер </p>
                </div>
            </td>
        </tr>
        <tr>
            <td align="left">зачеркивание^H^H^H^H^H или зачеркивание^W</td>
            <td align="left"><del>зачеркивание</del></td>
        </tr>
            <tr>
            <td align="left">* текст<br/>* текст</td>
            <td align="left"><ul><li>текст</li><li>текст</li></ul></td>
        </tr>
    <tr>
            <td align="left">1. текст<br/>2. текст</td>
            <td align="left"><ol><li>текст</li><li>текст</li></ol></td>
        </tr>
        <tr>
            <td align="left">> > текст<br/>или<br/>> текст</td>
            <td align="left"><font color=#406010>> > текст</font><br/>или<br/><font color=#789922>> текст</font></td>
        </tr>
        <tr>
            <td align="left">&nbsp;текст<br/>&nbsp;текст</td>
            <td align="left"><tt>блок<br/>кода</tt></td>
        </tr>
        <tr>
            <td align="left">-</td>
            <td align="left">-</td>
        </tr>
        <tr>
            <td align="left">--</td>
            <td align="left">–</td>
        </tr>
        <tr>
            <td align="left">---</td>
            <td align="left">—</td>
        </tr>
        <tr>
            <td align="left">(c)</td>
            <td align="left">&copy;</td>
        </tr>
        <tr>
            <td align="left">(tm)</td>
            <td align="left">&#153;</td>
        </tr>
        <tr>
            <td align="left">...</td>
            <td align="left">&#133;</td>
        </tr>
    </tbody>
</table>

<h2 style="margin: 0; text-align: center;">Особенности Orphereus</h2>

<h3 style="text-align: center;">О досках и плотницком деле.</h3>
На Аноме нет жестко закрепленной системы досок.
Каждому треду может соответствовать несколько <i>тэгов</i>, которые перечисляются в поле boards при создании треда.
Те тэги, список которых вы видите наверху каждой страницы - это и есть доски в обычном значении этого слова. 
Любой популярный тэг может стать доской.
<i>Доска — это тэг, который понравился бородатым админам и был закреплен в верхнем меню.</i> Поэтому <b>обязательно пользуйтесь тэгами</b>!

<h3 style="text-align: center;">Фильтры</h3>
На Аноме можно не только постить в несколько досок. Можно еще и просматривать посты из разных досок. Чтобы этого добиться, 
введите в адресной строке браузера адрес вида <a href="http://anoma.ch/b+d+a">http://anoma.ch/b+d+a</a>. Вам будут показаны все треды из 
досок /b/, /d/ и /a/. Если вы введете адрес вида <a href="http://anoma.ch/b+d+a-drugs">http://anoma.ch/b+d+a-drugs</a>, то вы увидите все треды
из /b/, /d/ и /a/ кроме тех, которые размещены еще и на доске /drugs/. Несколько досок, таким образом соединенных в одну, называются <i>фильтрами</i>.
<br/>
Также на Аноме есть два специальных фильтра:
<ol>
<li><b>/~/</b> — все треды изо всех досок. В своем <a href="/userProfile/">профиле</a> вы можете перечислить через запятую те тэги, которые вы не хотите видеть в /~/ (пункт Home filter exclusions)</li>
<li><b>/@/</b> — все треды, в которых есть ваши сообщения</li>
</ol>
Вы можете добавить часто используемые фильтры в свой профиль (пункт User Filters) - тогда под списком досок появится еще одна строка с вашими личными фильтрами.<br />
Особая страница <b>/!/</b> — это список досок и тэгов, статистическая информация и прочее.

<hr />