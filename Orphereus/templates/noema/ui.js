//# -*- coding: utf-8 -*-

(function() {
    var postsCache = {};
    
    function addFileRow() {
        var currentCount = parseInt($('#createdRows').attr('value')),
            additionalFilesCount = parseInt(
                $('#additionalFilesCount').attr('value'));
        if (currentCount >= additionalFilesCount - 1) {
            $('#addFileButton').attr('disabled', 'disabled');
        }
        $('#createdRows').attr('value', currentCount + 1);

        var currentId = parseInt($('#nextRowId').attr('value'));
        $('#nextRowId').attr('value', currentId + 1);

        var newRow = $('#fileRow0').clone();
        newRow.attr('id', 'fileRow' +  currentId);
        
        $('input[type=file]', newRow).attr('name', 'file_' + (currentId + 1));
        var spoilerField = $('input.spoiler-toggle', newRow);
        if (spoilerField) {
            spoilerField.attr('name', 'spoiler_' + (currentId + 1));
        }
        $('button.add-file', newRow).after(
            $('<button class="remove-file">убрать</button>').
                click(removeFileRow)
        ).remove();
        $('#newPost table.attaches').append(newRow);
    }
    
    function removeFileRow() {
        $(this).closest('tr').remove();
        var currentCount = parseInt($('#createdRows').attr('value'));
        $('#createdRows').attr('value', currentCount - 1);
        $('#addFileBtn').attr('disabled', '');
        return false;
    }
    
    function checkForTagNames(){
        var checkedField = $('#newPost input[name=tagsChecked]');
        if (!checkedField.val() && $('#newPost input[name=newThread]').val()) {
            var tags = $('#newPost input[name=tags]').val();
            // FIXME: URL
            $.post('/ajax/checkTags', {tags: tags}, tagCheckComplete);
            $('#newPost form').hide();
            $("#additionalPostParameters").show();
            $("#paramPlaceholder").html($("#paramPlaceholderContent").html());
            $("#additionalPostParameters button").attr('disabled', 'disabled');
            checkedField.val('yes');
            return false;
        }
        else
        {
            checkedField.val('');
            return true;
        }
    }
    
    function restoreForm() {
        $('#additionalPostParameters').hide();
        $('#newPost form').show();
        $('#newPost input[name=tagsChecked]').val('');
        $("#paramPlaceholder").html('&nbsp;');
    }
    
    function tagCheckComplete(data) {
        if (data) {
            $('#paramPlaceholder').html(data);
            $('#additionalPostParameters button').attr('disabled', '');
            $('#submitAgainButton').click(function() {
                $('#newPost form.post-content').append(
                    $('#additionalPostParameters')
                ).submit();
            });
            $('#cancelPostingButton').click(restorePostForm);
        }
        else {
            $('#newPost form.post-content').submit();
        }
    }
    
    function quickReply() {
        var threadId = $(this).closest('.thread').attr('data-id'),
            targetId = $(this).closest('.post').attr('data-id');
        $(this).closest('.post-wrapper').after($('#replyWrapper').show());
        $('#reply').attr(
            'action',
            $('#reply').attr('action').replace(/\d+/, threadId)
        );
        $('#reply input[name=tagLine]').attr(
            'value',
            $('#newPost input[name=tagLine]').attr('value')
        );
        $('#reply input[name=curPage]').attr(
            'value',
            $('#newPost input[name=curPage]').attr('value')
        );
        var textarea = $('#reply textarea').get(0);
        textarea.value += '>>' + targetId + '\n';
        if (textarea.setSelectionRange) {
            textarea.setSelectionRange(
                textarea.value.length, textarea.value.length
            );
        }
        textarea.focus();
        return false;
    }
    
    function loadSkippedReplies() {
        var threadId = $(this).attr('data-id');
        $(this).closest('div').html('Загружаем, подождите...');
        $('#tail' + threadId).load(
            '/ajax/getRenderedReplies/' + threadId,
            function() {
                initPostControls('#tail' + threadId);
            }
        );
    }
    
    function showTarget(href) {
        var me = this;
        
        function realShowTarget(targetId) {
            if (postsCache[targetId] !== null) {
                var wrapper = $('#hoverWrapper');
                wrapper.html(postsCache[targetId]);
                var left = $(me).offset().left + $(me).width(),
                    top = $(me).offset().top - wrapper.height() - 2;
                wrapper.css('left', left).css('top', top).show();
            }
        }
        
        var targetId = href.match(/\/(\d+)\#i(\d+)$/)[2];
        if (postsCache.hasOwnProperty(targetId)) {
            realShowTarget(targetId);
        } else if ($('#postWrapper' + targetId).length > 0) {
            postsCache[targetId] = $('#postWrapper' + targetId).html();
            realShowTarget(targetId);
        } else {
            $.ajax({
                url: '/ajax/getRenderedPost/' + targetId,
                success: function(html) {
                    postsCache[targetId] = html;
                    realShowTarget(targetId);
                },
                failure: function() {
                    postsCache[targetId] = null;
                }
            });
            return;
        }
    }
    
    function hideTarget() {
        $('#hoverWrapper').hide().empty();
    }
    
    function expandCut() {
        var postId = $(this).attr('data-id');
        $.ajax({
            url: '/ajax/getPost/' + postId,
            success: function(html) {
                initTextControls(
                    $('#i' + postId + ' .real-post-text').html(html)
                );
            }
        });
        return false;
    }
    
    function initTextControls(where) {
        $('a', where).each(function() {
            var me = this;
            if (!$(me).hasClass('post-cut')) {
                $(me).hover(
                    function() {
                        showTarget.call(me, $(me).attr('href'));
                    },
                    hideTarget
                );
            }
        });
    }
    
    function initPostControls(where) {
        $('.post-control a').click(function() {
            $('.post-head input.delete').show();
        });
        $('a.post-id', where).click(quickReply);
        $('a.file-tile', where).click(function() {
            var img = $('img', this);
            if (img) {
                var width = $(this).attr('data-width'),
                    height = $(this).attr('data-width');
                if ((width <= 1000) && (height <= 700)) {   // FIXME
                    if (img.hasClass('thumb')) {
                        img.attr('data-thumb-src', img.attr('src'));
                        img.attr('src', $(this).attr('href'));
                        img.removeClass('thumb');
                    } else {
                        img.attr('src', img.attr('data-thumb-src'));
                        img.addClass('thumb');
                    }
                } else {
                    return true;
                }
            }
            return false;
        });
        initTextControls($('.post-text', where));
        $('.post-cut', where).click(expandCut);
    }
    
    function highlightPost() {
        $('.post.highlighted').removeClass('highlighted');
        if (window.location.hash && /^#i[0-9]+$/.test(window.location.hash)) {
            $(window.location.hash).addClass('highlighted');
        }
    }
    
    $(document).ready(function() {
        $('#newPostToggle').click(function() {
            $('#newPost form').toggle();
        });
        
        $('#newPost form').submit(function() {
            return checkForTagNames();
        });
        
        $('#newPost .add-file').click(function() {
            addFileRow();
            return false;
        });
        
        initPostControls();
        
        $('#replyCancel').click(function() {
            $('#replyWrapper').hide();
            return false;
        });
        
        $('.skipped a').click(loadSkippedReplies);
        
        window.onhashchange = highlightPost;
        highlightPost();
    });
})();


