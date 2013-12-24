s = document.createElement('script');
s.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js');
document.getElementsByTagName('head')[0].appendChild(s);

function jqueryLoaded() {
	clearInterval(checker);
	contentAffiliateAdvertising()
}
 
function checkJquery() {
	if (window.jQuery) {jqueryLoaded();} else { checker = window.setInterval(checkJquery, 2000);}
}
 
checkJquery();

function contentAffiliateAdvertising() {
	var totaltext = $($(".post-body").parent()).children(".post-body").text();
	var options = {'maxaffiliatelinks': 8, 'maxwikilinks': 5}
	var tracker = "1qaz2wsx";
	var result = null;
	$.ajax({
      	    type: "POST",
	    crossDomain: true,
	    url: "http://www.penpatron.com/content-affiliate-advertising/getContentAffiliateAdvertising.php",
	    data: { text: totaltext, tracker: tracker, options: options },
	    dataType: "jsonp",
	    jsonp: 'jsonp_callback'
	}).done(function(data) {
	    result=data.keywords;
	    //result = [{'keyword': 'Columbia Business School', 'link': 'http://www.cseblog.com'} , {'keyword': 'IBM', 'link': 'http://www.pratikpoddar.com'}];
	    $.each(result, function(i,v) {
		$.each($($(".post-body").parent()).children(".post-body"), function(index, value) { $(this).html(function(index,html){return html.replace(v['keyword'], '<a target="_blank" href="'+v['link']+'">'+v['keyword']+'</a>')})})
	    });
	})
}


