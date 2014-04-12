s = document.createElement('script');
s.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js');
document.getElementsByTagName('head')[0].appendChild(s);
var jqueryloadchecker = window.setInterval(checkJqueryAndGlobals, 3000);
var functioncallchecker = 0;
var gmailidentifierextractor = 0;
 
function jqueryLoaded() {
	clearInterval(jqueryloadchecker);
	$.getScript( "https://46.137.209.142/static/crsq/js/emailrecommender/gmail.min.js" )
		  .done(function( script, textStatus ) {
		        if (functioncallchecker == 0) {
	        	        functioncallchecker = 1;
				var gmail = Gmail();
		                gmailEmailRecommender();
				gmail.observe.on("open_email", function(id, url, body) {
  				  console.log("crsq email opened");
				  gmailEmailRecommender();
				})
        		 }
		})
}
 
function checkJqueryAndGlobals() {
       clearInterval(jqueryloadchecker);
       if ((window.jQuery) && (typeof GLOBALS == "object")) {jqueryLoaded();} else { jqueryloadchecker = window.setInterval(checkJqueryAndGlobals, 3000);}
}

function gmailEmailRecommender() {
	var gmail = Gmail();
	var username = gmail.get.user_email();
	var emailidentifier = getGmailEmailsUniqueIdentifiers();
	console.log("username: " + username)
	console.log(emailidentifier)
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

	if (arrlen == 0) {
		$('#crsqdiv').append("No Suggestions as of now");
	}

	for (var i = 0; i < arrlen; i++) {
        	$('#crsqdiv').append( "<div class='crsqtitle'>" + l[i]['articletitle'] + "</div><div class='crsqlink'><a href='" + l[i]['url'] + "'>" + l[i]['url'] + "</a></div><br/>");
	}
}

function getGmailEmailsUniqueIdentifiers() {

	/*
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
	*/

	var gmail = Gmail();
	t = gmail.get.email_data(email_id=undefined).threads;
	
	function checkingifreturned() {
 	   if(typeof t == 'undefined') {
		clearInterval(checkingifreturned);
	        setTimeout(checkingifreturned, 2000);
	        return;
	    }

	    else {
	  
		output = [];
		for (key in t) {
			outputtemp = {};
			outputtemp['from_email'] = t[key]['from_email'];
			outputtemp['to'] = t[key]['to'];
			outputtemp['cc'] = t[key]['cc'];
			outputtemp['bcc'] = t[key]['bcc'];
			outputtemp['datetime'] = t[key]['datetime'];
			outputtemp['subject'] = t[key]['subject'];
			output.push(outputtemp);
		}	
        	return JSON.stringify(output)
            }
	}
	checkingifreturned();
}


