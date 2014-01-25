//portfolio close button 
$('.close').click(function () {
    $('.worksajax').slideUp();
    return false;
});

//portfolio setting
$('#work-carousel').carousel({
	interval: 6000
	});
	
// portfolio Video responsive
        $(".worksajax .video").fitVids();
	
// script prettyphoto 
$(document).ready(function () {
    $("a[data-rel^='prettyPhoto']").prettyPhoto({
        social_tools: false,
        deeplinking: false
    });
});

//easing portfolio scrolling
$(function () {
    $('.close').bind('click', function (event) {
        var $anchor = $('#portfolio');

        $('html, body').stop().animate({
            scrollTop: $($anchor).offset().top - 89
        }, 1000, 'linear');
        event.preventDefault();
    });
});


// Video responsive
$(".white-bg").fitVids();