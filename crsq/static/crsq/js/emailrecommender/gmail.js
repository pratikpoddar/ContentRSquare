if ($("#crsqdiv").length == 0) {
	$('.nH .adC').append('<div id="crsqdiv"></div>')
}
else {
	$("#crsqdiv").html('') 
}
$("#crsqdiv").append('<style type="text/css"> .crsqtitle { font-size:80%; color: #222;} .crsqlink {font-size:70%;} </style>')
$("#crsqdiv").append('Antaryaami Suggestions<br/><br/>')

$('#rapportive-sidebar').hide()

links=["http://www.google.com", "http://www.yoyo.com"]
titles=["Google", "Yo Yo"]
arrlen=titles.length

for (var i = 0; i < arrlen; i++) {
	$('#crsqdiv').append( "<div class='crsqtitle'>" + titles[i] + "</div><div class='crsqlink'><a href='" + links[i] + "'>" + links[i] + "</a></div><br/>");
}

$('.ajz').click()
$('tr.ajv')


