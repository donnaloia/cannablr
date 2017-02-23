$(function () {
    $('.dropdown .title').on('click',function(){
        $(this).parent().toggleClass('select').find('.drop').toggle();
    });
    $('.dropdown .drop li').on('click',function(){
        var $this = $(this), input = $this.text();
        $('.dropdown .title').text(input);
    });
});