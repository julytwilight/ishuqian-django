$(function(){
    // 显示添加书签url表单
    $('.add-bookmark').click(function(){
        $('.addlink').toggle();
    });
    // 隐藏添加书签url表单
    $('.url-cancel').click(function(){
        $('.add-bookmark').click();
    });

    // 提交添加url表单表单验证
    $('.add-url').submit(function(){
        if ( !$('.bookmark-url').val() ) {
            return false;
        }
    });

    // 全选 和 全不选
    $('.checkall').click(function(){
        // $('.bm-box').each(function(){
        //     //$(this).prop('checked', true);
        //     $(this).checked=true;
        // });
        var names=document.getElementsByName('bm_box');
        var len=names.length;
        if(len>0)
        {
            var i=0;
            for(i=0;i<len;i++)
                names[i].checked=true;
        }
    });
    $('.delcheck').click(function(){
        // $('.bm-box').each(function(){
        //     //$(this).prop('checked', false);
        //     $(this).checked=false;
        // });
        var names=document.getElementsByName('bm_box');
        var len=names.length;
        if(len>0)
        {
            var i=0;
            for(i=0;i<len;i++)
                names[i].checked=false;
        }
    });

    // 选择收藏书签的用户时
    $('.favorite-person').hover(function(){
        $(this).addClass('favorite-person-hover');
    }, function(){
        $(this).removeClass('favorite-person-hover');
    });
});