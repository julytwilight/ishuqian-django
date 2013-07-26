$(function(){
    //显示添加书签url表单
    $('.add-bookmark').click(function(){
        $('.addlink').toggle();
    });
    //隐藏添加书签url表单
    $('.url-cancel').click(function(){
        $('.add-bookmark').click();
    });

    //提交添加url表单表单验证
    $('.add-url').submit(function(){
        if ( !$('.bookmark-url').val() ) {
            return false;
        }
    });
});