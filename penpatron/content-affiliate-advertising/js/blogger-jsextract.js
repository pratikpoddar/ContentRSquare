s = document.createElement('script');
s.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js');
document.getElementsByTagName('head')[0].appendChild(s);

function jqueryLoaded() {
	clearInterval(checker);
	contentAffiliateAdvertising()
}
 
function checkJquery() {
	if (window.jQuery) {
       		jqueryLoaded();
	} 
    	else {
       		checker = window.setInterval(checkJquery, 1000);
    	}
}	
 
checkJquery();

function contentAffiliateAdvertising() {

	//Add Related Posts
	//$(".post-body").append("<div class='related-posts'>Related Posts</div>")
	//$($(".related-posts").parent().parent()).children(".post-title").text()
	//$($(".related-posts").parent().parent()).children(".post-body").text()
	//$($($(".related-posts").parent().parent()).children(".post-footer")).children().children(".post-labels").children("a")

	//Get All Text
	var totaltext = $($(".post-body").parent()).children(".post-body").text();
	var options = {'maxaffiliatelinks': 8, 'maxwikilinks': 5}
	console.log("sdsd");

	result = []
	$.ajax({
	  type: "POST",
	  crossDomain: true,
	  url: "http://www.penpatron.com/content-affiliate-advertising/getContentAffiliateAdvertising.php",
	  data: { text: totaltext, tracker: "1qaz2wsx", options: options },
	  dataType: "json"
	}).done(function() {
	    console.log("Done");
	  });


	result = [{'keyword': 'Columbia Business School', 'link': 'http://www.cseblog.com'} , {'keyword': 'IBM', 'link': 'http://www.pratikpoddar.com'}];
	
	$.each(result, function(i,v) {
		$.each($($(".post-body").parent()).children(".post-body"), function(index, value) { $(this).html(function(index,html){return html.replace(v['keyword'], '<a target="_blank" href="'+v['link']+'">'+v['keyword']+'</a>')})})
	});
}


