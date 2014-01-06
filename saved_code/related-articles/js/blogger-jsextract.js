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
       		checker = window.setInterval(checkJquery, 2000);
    	}
}	
 
checkJquery();

//Add Related Posts
//$(".post-body").append("<div class='related-posts'>Related Posts</div>")
//$($(".related-posts").parent().parent()).children(".post-title").text()
//$($(".related-posts").parent().parent()).children(".post-body").text()
//$($($(".related-posts").parent().parent()).children(".post-footer")).children().children(".post-labels").children("a")



