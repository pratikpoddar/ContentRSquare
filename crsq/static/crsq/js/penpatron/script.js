//slideshow background setting
jQuery(function ($) {

    $.supersized({

        // Functionality
        slide_interval: 7000, // Length between transitions
        transition: 1, // 0-None, 1-Fade, 2-Slide Top, 3-Slide Right, 4-Slide Bottom, 5-Slide Left, 6-Carousel Right, 7-Carousel Left
        transition_speed: 600, // Speed of transition

        // Components							
        slide_links: 'false', // Individual links for each slide (Options: false, 'num', 'name', 'blank')
        slides: [ // Slideshow Images
            {
                //image: 'images/cococoslider2.jpg',
                //title: '<div class="col-md-6" style="padding:15px;"><h2 style="line-height:38px;background-color: rgba(0,0,0,0.65);"><span style="font-size:40%">Student Writers:<br/> Get recognition, exposure, internship and money from Patrons by doing what you do best</span></h2></div><div class="col-md-6" style="padding:15px"><h2 style="line-height:38px;background-color: rgba(0,0,0,0.65);"><span style="font-size:40%">Company:<br/> Get Original Content<br/> and Patronage Targeted, Passionate and Opinionated Writers</span></h2></div>'
		//title: '<h2 style="line-height:38px;background-color: rgba(0,0,0,0.65);max-width:500px;padding:10px;"><i class="fa fa-pencil"></i><br/><span style="font-size:40%">Student Writers:<br/> Get recognition, exposure, internship and money from Patrons by doing what you do best</span></h2>'
            //}, {
                image: 'static/crsq/img/penpatron/cococoslider1.jpg',
                title: '<h2 style="line-height:38px;background-color: rgba(0,0,0,0.65);max-width:500px;padding:10px;"><i class="fa fa-pencil"></i><br/><span style="font-size:40%">Student Writers:<br/> Get <u>recognition</u>, <u>exposure</u>, <br/><u>internship</u> and <u>money</u> from Patrons by doing what you do best</span></h2>'
            }, {
                image: 'static/crsq/img/penpatron/cococoslider3.jpg',
                title: '<h2 style="line-height:38px;background-color: rgba(0,0,0,0.65);max-width:500px;padding:10px;"><i class="fa fa-suitcase"></i><br/><span style="font-size:40%">Company:<br/> Get <u>Original Content</u><br/> and <u>Targeted, Passionate and Opinionated Writers</u> by being Patrons</span></h2>'
            },
        ]

    });
});

//toggle menu
$('.menu-btn').on('click',function(){
    $('.navigation').collapse({
toggle: false
});
})
$('body').on('click',function(){
    $('.navigation').collapse('hide');
})


//Page scrolling
$(document).ready(function () {
    $('.navigation').onePageNav({
        filter: ':not(.external)',
        scrollThreshold: 0.25,
        scrollOffset: 90
    });

});


// script prettyphoto
$(document).ready(function () {
    $("a[data-rel^='prettyPhoto']").prettyPhoto({
        social_tools: false,
        deeplinking: false
    });
});


$(window).load(function () {
    $('.bwWrapper').BlackAndWhite({
        hoverEffect: true, // default true
        // set the path to BnWWorker.js for a superfast implementation
        webworkerPath: false,
        // for the images with a fluid width and height 
        responsive: true,
        // to invert the hover effect
        invertHoverEffect: false,
        // this option works only on the modern browsers ( on IE lower than 9 it remains always 1)
        intensity: 1,
        speed: { //this property could also be just speed: value for both fadeIn and fadeOut
            fadeIn: 200, // 200ms for fadeIn animations
            fadeOut: 800 // 800ms for fadeOut animations
        },
        onImageReady: function (img) {
            // this callback gets executed anytime an image is converted
        }
    });
});


//portfolio setting
$('#about-carousel').carousel({
    interval: 6000
});


//team ajax setting
$(document).ready(function () {
    $('.team-ajax,.team-icon').click(function () {

        var toLoad = $(this).attr('data-link') + ' .worksajax > *';
        $('.teamajax').slideUp('slow', loadContent);

        function loadContent() {
            $('.teamajax').load(toLoad, '', showNewContent)
        }

        function showNewContent() {

        }

        return false;


    });

});


//team scrolling
$(function () {
    $('.team-ajax,.team-icon').bind('click', function (event) {
        var $anchor = $('#teamlist');

        $('html, body').stop().animate({
            scrollTop: $($anchor).offset().top - 89
        }, 1000, 'linear');
        event.preventDefault();
    });
});



