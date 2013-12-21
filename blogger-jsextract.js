s = document.createElement('script'); 
s.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js'); 
document.getElementsByTagName('head')[0].appendChild(s); 

//Add Related Posts
//$(".post-body").append("<div class='related-posts'>Related Posts</div>")
//$($(".related-posts").parent().parent()).children(".post-title").text()
//$($(".related-posts").parent().parent()).children(".post-body").text()
//$($($(".related-posts").parent().parent()).children(".post-footer")).children().children(".post-labels").children("a")

//Get All Text
$($(".post-body").parent()).children(".post-body").text()

