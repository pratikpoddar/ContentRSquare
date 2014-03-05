s = document.createElement('script');
s.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js');
document.getElementsByTagName('head')[0].appendChild(s);
var jqueryloadchecker = window.setInterval(checkJquery, 3000);
var functioncallchecker = 0;

function jqueryLoaded() {
	clearInterval(jqueryloadchecker);
	if (functioncallchecker == 0) {
		functioncallchecker = 1;
		contentAffiliateAdvertising()
	}
}
 
function checkJquery() {
	clearInterval(jqueryloadchecker);
	if (window.jQuery) {jqueryLoaded();} else { jqueryloadchecker = window.setInterval(checkJquery, 3000);}
}
 
function contentAffiliateAdvertising() {
	var totaltext = $($(".post-body").parent()).children(".post-body").text().replace(/[\r\n]/g,' ');
	var options = {'maxaffiliatelinks': 8, 'maxwikilinks': 5};
	var index = "Books";
	var result = null;
	$.ajax({
      	    type: "GET",
	    crossDomain: true,
	    url: "http://46.137.209.142/content-affiliate-advertising",
	    data: { text: totaltext, options: options, index: index },
	    dataType: "jsonp",
	    jsonp: 'jsonp_callback'
	}).done(function(data) {
	    result=data.keywords;
	    console.log("Content-Affiliate-Advertising");
	    console.log(result);
	    //result = [{'keyword': 'Columbia Business School', 'link': 'http://www.cseblog.com'} , {'keyword': 'IBM', 'link': 'http://www.pratikpoddar.com'}];
	    $.each(result, function(i,v) {
		$.each($($(".post-body").parent()).children(".post-body"), function(index, value) { $(this).html(function(index,html){return html.replace(v['keyword'], '<a target="_blank" href="'+v['link']+'">'+v['keyword']+'</a>')})})
	    });
	})
}


