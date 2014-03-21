s = document.createElement('script');
s.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js');
document.getElementsByTagName('head')[0].appendChild(s);
var jqueryloadchecker = window.setInterval(checkJquery, 3000);
var functioncallchecker = 0;

function jqueryLoaded() {
	clearInterval(jqueryloadchecker);
	if (functioncallchecker == 0) {
		functioncallchecker = 1;
		gmailEmailRecommender()
	}
}
 
function checkJquery() {
	clearInterval(jqueryloadchecker);
	if (window.jQuery) {jqueryLoaded();} else { jqueryloadchecker = window.setInterval(checkJquery, 3000);}
}
 
function gmailEmailRecommender() {
	var emailidentifier = getGmailEmailsUniqueIdentifiers();
	var username = "pratik.phodu@gmail.com";
	$.ajax({
      	    type: "GET",
	    crossDomain: true,
	    url: "http://46.137.209.142/gmailemailjs",
	    data: { emailidentifier: emailidentifier, username: username },
	    dataType: "jsonp",
	    jsonp: 'jsonp_callback'
	}).done(function(data) {
	    result={'links': ["http://www.google.com", "http://www.yoyo.com"], 'titles': ["Google", "Yo Yo"]};
	    console.log("CRSQ Gmail Email Recommender");
	    console.log(result);
	    showonsidebar(result);
	)
}

function showonsidebar(d) {
	if ($("#crsqdiv").length == 0) {
	        $('.nH .adC').append('<div id="crsqdiv"></div>')
	}
	else {
        	$("#crsqdiv").html('')
	}

	$("#crsqdiv").append('<style type="text/css"> .crsqtitle { font-size:80%; color: #222;} .crsqlink {font-size:70%;} </style>');
	$("#crsqdiv").append('Antaryaami Suggestions<br/><br/>');

	$('#rapportive-sidebar').hide();

	links=d['links'];
	titles=d['titles'];
	arrlen=titles.length;

	for (var i = 0; i < arrlen; i++) {
        	$('#crsqdiv').append( "<div class='crsqtitle'>" + titles[i] + "</div><div class='crsqlink'><a href='" + links[i] + "'>" + links[i] + "</a></div><br/>");
	}
}

function getGmailEmailsUniqueIdentifiers() {
        $('.ajz').click(); openemailelems = $('tr.ajv'); $('.ajz').click();
        openemails = "";
        for (var i=0;i<openemailelems.length;i++)
        {
                if ($(openemailelems[i]).hasClass('UszGxc')) {
                        openemails += ";;||;;||crsq||;;||;;";
                }
                openemails += $.trim(openemailelems[i].innerText) + "--||--||crsq||--||--";
        }
        openemails += ";;||;;||crsq||;;||;;"
        return openemails
}


