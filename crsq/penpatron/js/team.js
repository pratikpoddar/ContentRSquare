//portfolio close button 
$('.team-close').click(function () {
    $('.teamajax').slideUp();
    return false;
});

//portfolio setting
$('#team-carousel').carousel({
	interval: 6000
	});
	
// portfolio Video responsive
        $(".teamajax .video").fitVids();
	
// script prettyphoto 
$(document).ready(function () {
    $("a[data-rel^='prettyPhoto']").prettyPhoto({
        social_tools: false,
        deeplinking: false
    });
});

//easing portfolio scrolling
$(function () {
    $('.team-close').bind('click', function (event) {
        var $anchor = $('#team');

        $('html, body').stop().animate({
            scrollTop: $($anchor).offset().top - 89
        }, 1000, 'linear');
        event.preventDefault();
    });
});


// Video responsive
$(".white-bg").fitVids();