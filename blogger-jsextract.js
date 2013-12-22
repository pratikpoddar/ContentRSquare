$(window).load(function() {

	s = document.createElement('script'); 
	s.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js'); 
	document.getElementsByTagName('head')[0].appendChild(s); 

	//Add Related Posts
	//$(".post-body").append("<div class='related-posts'>Related Posts</div>")
	//$($(".related-posts").parent().parent()).children(".post-title").text()
	//$($(".related-posts").parent().parent()).children(".post-body").text()
	//$($($(".related-posts").parent().parent()).children(".post-footer")).children().children(".post-labels").children("a")

	$(document).load(function() {
		//Get All Text
		var totaltext = $($(".post-body").parent()).children(".post-body").text()

		$.ajax({
		  type: "POST",
		  url: "http://www.tomonotomo.com/getContentAffiliateAdvertising",
		  data: { text: text, tracker: "1qaz2wsx" }
		})
		  .done(function( res ) {
		    alert( "Data Saved: " + res );
		  });


		result = [{'keyword': 'Columbia Business School', 'link': 'http://www.cseblog.com'} , {'keyword': 'IBM', 'link': 'http://www.pratikpoddar.com'}]
	
		$.each(result, function(i,v) {
			$.each($($(".post-body").parent()).children(".post-body"), function(index, value) { $(this).html(function(index,html){return html.replace(v['keyword'], '<a href="'+v['link']+'">'+v['keyword']+'</a>')})})
		})
	}

}

