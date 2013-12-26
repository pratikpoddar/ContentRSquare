s = document.createElement('script');
s.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js');
document.getElementsByTagName('head')[0].appendChild(s);

function jqueryLoaded() {
	clearInterval(checker);
	relatedVideosAdvertising()
}
 
function checkJquery() {
	if (window.jQuery) {jqueryLoaded();} else { checker = window.setInterval(checkJquery, 2000);}
}
 
checkJquery();

function relatedVideosAdvertising() {
                var tag = document.createElement("script");
                tag.src = "https://www.youtube.com/iframe_api";
                var firstScriptTag = document.getElementsByTagName("script")[0];
                firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
                onYouTubeIframeAPIReady();

}

function getCRSQSuggestions() {
        var videoid = 123;
	var userid = 123;
	var result = null;
        $.ajax({
            type: "GET",
            crossDomain: true,
            url: "http://www.penpatron.com/related-videos-advertising/getRelatedVideos.php",
            data: { 'videoid': videoid, 'userid': userid },
            dataType: "jsonp",
            jsonp: 'jsonp_callback'
        }).done(function(data) {
            result=data.keywords;
            console.log("Related-Videos-Advertising");
            console.log(result);
            //result = [{'keyword': 'Columbia Business School', 'link': 'http://www.cseblog.com'} , {'keyword': 'IBM', 'link': 'http://www.pratikpoddar.com'}];
	    return result;
        })
	return null;
}

function onYouTubeIframeAPIReady() {
        var ytIframes = getEmbeddedVideos();
              for(var videoCount = 0;videoCount  < ytIframes.length; videoCount ++){
                   player[videoCount] = new YT.Player("ytplayer"+videoCount, {
                                               events: {
                                                    "onReady": onPlayerReady,
                                                    "onStateChange": onPlayerStateChange
                                                    },
                                               playerVars: {rel: 0, enablejsapi: 1}
                          });
                }
}

function crsq_suggestion_row(w,img_h)
{
    var img_w = img_h*4/3;
      var l = w/img_w ;
	var rowArray = [l,w%img_w];
      return rowArray;
}
function crsq_suggestion_column(h,img_h)
{
  var b = (h-61)/img_h ;
  return b;
}

function getPostTags(){
        var keywords;
        var metas = document.getElementsByTagName('meta');
        for(var i =0; i< metas.length;i++){
                if(metas[i].name == 'keywords'){
                        keywords = metas[i].content;
                }
        }
        return keywords;
}
function getPostTitle(){
        var title = document.getElementsByTagName('title');
                var post_title = title[0].innerHTML;
        return post_title;
}

function onPlayerReady(event){
        //alert(event.target.a.id+"ready");
        var intubeCss = document.createElement('link');
        intubeCss.href = 'http://ec2-54-213-118-208.us-west-2.compute.amazonaws.com/css/intube.css';
        intubeCss.rel = "stylesheet";
        var firstScriptTag = document.getElementsByTagName("script")[0];
        firstScriptTag.parentNode.insertBefore(intubeCss, firstScriptTag);
        var suggestionContainer = document.createElement('div');
		jQuery(suggestionContainer).addClass('suggestions');
        suggestionContainer.id = 'suggestionsContainer'+event.target.a.id.substring(8);
        jQuery(suggestionContainer).insertAfter(event.target.a);
        var tags = getPostTags();
        var link = window.location.href;
        if(event.target.a.id == 'ytplayer0'){
                var videoId = event.target.getVideoData();
                videoId = videoId.video_id;
                getCRSQSuggestions(authKey,videoId);
        }
}
function onPlayerStateChange(event){
        var id  = event.target.a.id.substring(8);
                       if (event.data == 0) {
                              var width = event.target.a.clientWidth;
                              var videoHeight = event.target.a.clientHeight;
                              var height = videoHeight;
                                jQuery('#suggestionsContainer'+id).children().remove();
var videoNegHeight = -1 * videoHeight;
                              jQuery("#suggestionsContainer"+id).css({"position":"relative","background":"black","opacity":"1","margin-top":videoNegHeight +"px","height":videoHeight+"px"});
                              jQuery("#suggestionsContainer"+id).width(width);
                              jQuery("#suggestionsContainer"+id).height(height-38);

                                var position=jQuery('#'+event.target.a.id).offset();
                                var imageHeight = getImgH(videoHeight);
			      var rowArray = crsq_suggestion_row(width,imageHeight);
                              var k =Math.floor(rowArray[0]);
                              var l =Math.floor(crsq_suggestion_column(height,imageHeight));
                              var i = 12/k ;
                              var align_height = (height - (l*106))/2;
                              var align_width = (width- (k*155))/2;
                              var suggestiontop = position.top + align_height - 10;
                              var suggestionIndex = 0;
                              for(var counter1=0;counter1<l;counter1++){
                                    var divtest = document.createElement("div");
                                     jQuery(divtest).addClass("row-fluid");
                                    jQuery(divtest).css("margin-bottom","4px");
                                    jQuery(divtest).appendTo("#suggestionsContainer"+id);
                                    for(counter2=0;counter2<k;counter2++){
                                            var span = document.createElement("div");
                                           jQuery(span).addClass("span"+ i);
                                           jQuery(span).addClass("suggestion");
                                           jQuery(span).attr('id','suggestion'+suggestionIndex);
                                           jQuery(span).appendTo(divtest);
                                           // var link = document.createElement("a");
                                        if(suggestionIndex < vozealSuggestions.length){
                                        //      link.href = vozealSuggestions[suggestionIndex]["link"];

                                           var image = document.createElement("img");
                                           image.src = vozealSuggestions[suggestionIndex]["thumbnail"];
                                           image.id = suggestionIndex;
                                           suggestionIndex++;
                                            jQuery(image).appendTo(span);
                                         //    jQuery(link).appendTo(span);
                                        }
                              }
                                jQuery('.suggestion').unbind('click');
                                jQuery('.suggestion').click(function(){
                                                                                jQuery(this.parentNode.parentNode).hide();
                                        if(vozealSuggestions[this.id.substring(10)]['isChannel'] == '0'){
                                                var suggestionLink = vozealSuggestions[this.id.substring(10)]['link'];
                                                jQuery.ajax({
                                                    url:VozealConfig.serverURL+"/redirector.php",
                                                    type:"GET",
                                                    async: false,
                                                    data: {
                                                              url:vozealSuggestions[this.id.substring(10)]['id'],
                                                              isChannel:vozealSuggestions[this.id.substring(10)]['isChannel'],
                                                              authkey: authKey,
                                                              sugId : this.id.substring(10)
                                                    },
                                                    success:function(msg){
                                                      window.location = suggestionLink+"?ref=vozeal";
                                                        },
                                                    error: function(er){
                                                    },
                                                            dataType: "jsonp"
                                                  });
                                        } else if( vozealSuggestions[this.id.substring(10)]['isChannel'] == '1'){
                                                event.target.loadVideoById(vozealSuggestions[this.id.substring(10)]['id']);
                                                jQuery.ajax({
                                                    url:VozealConfig.serverURL+"/redirector.php",
                                                    type:"GET",
                                                    async: true,
                                                    data: {
                                                              url:vozealSuggestions[this.id.substring(10)]['id'],
                                                              isChannel:vozealSuggestions[this.id.substring(10)]['isChannel'],
                                                              authkey: authKey,
                                                              sugId: this.id.substring(10)
                                                    },
                                                    success:function(msg){
                                                        },
                                                    error: function(er){
                                                    },
                                                            dataType: "jsonp"
                                                  });

                                        }
                              });
                              jQuery('.suggestion').hover(function(){
                                                      if(jQuery('#suggestionText').length < 1){
                                                          var suggestionIndex = this.children[0].id;
                                                          var suggestionTitle = vozealSuggestions[suggestionIndex]['title'];
                                                          var suggestionText = document.createElement('div');
                                                          suggestionText.id = "suggestionText";
                                                          jQuery(suggestionText).text(suggestionTitle);
                                                          this.appendChild(suggestionText);
							  jQuery(suggestionText).css('top',imageHeight/2 -30);
                                                      }
                                                     },function(){
                                                       jQuery('#suggestionText').remove();
                                                     });
                       }

                        var powered = document.createElement('div');
                                powered.id = "powered";
                                powered.innerHTML = "Powered by: <a id='vozealLink' href='http://www.vozeal.com'><img  src='http://www.vozeal.com/images/vozeal-logo-new-200X49.png'></img></a>";
                                jQuery(powered).appendTo("#suggestionsContainer"+id);
			//	jQuery('#suggestionsContainer'+id).css('left',adjustment);
                                jQuery('.suggestion img').css('height',imageHeight);
				if(vozealSuggestions.length > 0){
					jQuery('.row-fluid').offset({left:rowArray[1]/2});
      			        	jQuery('#suggestionsContainer'+id).show();
				}
				var suggestionsContainerPos = jQuery('#suggestionsContainer'+id).offset();
                                var suggestionsContainerLeft = suggestionsContainerPos.left;
				var suggestionContainerTop = suggestionsContainerPos.top;
				jQuery('#suggestionsContainer'+id).offset({top:position.top});
                                var adjustment = position.left - suggestionsContainerLeft;
                                console.log(adjustment);
                                console.log(suggestionsContainerLeft);
                                console.log(position.left);
				if(adjustment != 0){
					jQuery('#suggestionsContainer'+id).css('left',adjustment);
				}        
                                   if(id ==0){
                            var videoId = event.target.getVideoData();
                                        videoId = videoId.video_id;
                                                        registerImpressions(l*k,videoId);
                                           }
                           }
                       else if(event.data == 1){
                              jQuery('#suggestionsContainer'+id).hide();
                           }
}
function getImgH(h){
	h = h-62;
	var h_min = 100;
	var h_max = 150;
	var remainder  = h%100;
	var h_opt = h_min;
	for(var i =h_min;i<=h_max;i++){
		if(h%i < remainder){
			remainder = h/i;
			h_opt = i;
		}
	}
		
	return(h_opt);
}

function getEmbeddedVideos(){
        var iframes = document.getElementsByTagName('iframe');
        var ytIframes = filterYoutubeIframes(iframes);
        setIds(ytIframes);
        return ytIframes;
}
function filterYoutubeIframes(iframes){
        var ytIframes = new Array();
        for(var i =0;i<iframes.length;i++){
                var matches = iframes[i].src.match(/youtube.com\/embed/g);
                if(matches != null){
                        ytIframes.push(iframes[i]);
                }
        }
        return ytIframes;
}
function setIds(ytIframes){
        for(var i = 0; i<ytIframes.length;i++){
                ytIframes[i].id = "ytplayer"+i;
        }
}


