s = document.createElement('script');
s.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js');
document.getElementsByTagName('head')[0].appendChild(s);
var jqueryloadchecker = window.setInterval(checkJquery, 3000);
var functioncallchecker = 0;
var clickfunctionchecker = 0;

function jqueryLoaded() {
	clearInterval(jqueryloadchecker);
	$(window).load(function() {
		$.getScript( "https://raw.githubusercontent.com/KartikTalwar/gmail.js/master/gmail.min.js" )
		  .done(function( script, textStatus ) {
		        if (functioncallchecker == 0) {
	        	        functioncallchecker = 1;
		                gmailEmailRecommender();
		                if (clickfunctionchecker == 0) {
	        	                clickfunctionchecker = 1;
		                        $(window).click(function() {
        		                     gmailEmailRecommender()
	        	                });
					gmail.observe.on("open_email", function(id, url, body) {
  					  console.log("openemail");
					  gmailEmailRecommender()
					  console.log(gmail.get.email_data(id));
					})
        		        }
		        }		
		  })
	})
}
 
function checkJquery() {
	clearInterval(jqueryloadchecker);
	if (window.jQuery) {jqueryLoaded();} else { jqueryloadchecker = window.setInterval(checkJquery, 3000);}
}

 
function gmailEmailRecommender() {
	var emailidentifier = getGmailEmailsUniqueIdentifiers();
	var username = 'pratik.phodu@gmail.com';
	var gmail = Gmail();
	console.log(gmail.get.user_email())
	console.log(gmail.get.email_data(email_id=undefined))
	$.ajax({
      	    type: "GET",
	    crossDomain: true,
	    url: "https://46.137.209.142/gmailemailjs",
	    data: { emailidentifier: emailidentifier, username: username },
	    dataType: "jsonp",
	    jsonp: 'jsonp_callback'
	}).done(function(data) {
	    console.log("CRSQ Gmail Email Recommender");
	    console.log(data['output']);
	    showonsidebar(data['output']);
	})
}

function showonsidebar(l) {	
	if ($("#crsqdiv").length == 0) {
		$('.nH .adC').html('')
	        $('.nH .adC').append('<div id="crsqdiv"></div>')
	}
	else {
        	$("#crsqdiv").html('')
	}

	$("#crsqdiv").append('<style type="text/css"> .crsqtitle { font-size:80%; color: #222;} .crsqlink {font-size:70%;} </style>');
	$("#crsqdiv").append('Antaryaami Suggestions<br/><br/>');
	$('#rapportive-sidebar').hide();

	arrlen=l.length;

	for (var i = 0; i < arrlen; i++) {
        	$('#crsqdiv').append( "<div class='crsqtitle'>" + l[i]['articletitle'] + "</div><div class='crsqlink'><a href='" + l[i]['url'] + "'>" + l[i]['url'] + "</a></div><br/>");
	}
}

function getGmailEmailsUniqueIdentifiers() {
        $('.ajz').click(); openemailelems = $('tr.ajv'); $('.ajz').click();
        openemails = "";
        for (var i=0;i<openemailelems.length;i++)
        {
                if ($(openemailelems[i]).hasClass('UszGxc')) {
                        openemails += ";;||;;||crsq||;;||;;";
                };
		if (($.trim(openemailelems[i].innerText).indexOf("from:")==0) || ($.trim(openemailelems[i].innerText).indexOf("subject:")==0) || ($.trim(openemailelems[i].innerText).indexOf("date:"))==0) {
	                openemails += $.trim(openemailelems[i].innerText) + "--||--||crsq||--||--";
		};
        }
        openemails += ";;||;;||crsq||;;||;;"
        return openemails
}


