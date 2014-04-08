var articleGenerator = {
  
  searchOnCRSQ_: 'http://46.137.209.142:9200/article-index/article/_search?q=Delhi%20AAP%20Video%20India%20Today%20Group',

  requestArticles: function() {
    alert("History Search Start");
    chrome.history.search({text:''}, function(historyItems){
            //for (var i=0; i<historyItems.length;i++) {
                //    alert(JSON.stringify(historyItems[i]));
           // }
    });
    alert("History Search Done");
    var req = new XMLHttpRequest();
    req.open("GET", this.searchOnCRSQ_, true);
    alert("Article Search Done");
    req.onload = this.showArticles_.bind(this);
    req.send(null);
    alert("Showed Articles");
  },

  showArticles_: function (e) {
    var jsonObj = JSON.parse(e.target.response);
    var articlelist = jsonObj['hits']['hits'];
    alert("Got " + jsonObj['hits']['total'] + " Results");
    //var articles = [{'title': "Didn't elope with anyone's daughter: Arvind Kejriwal", 'url': 'http://www.ndtv.com/elections/article/election-2014/didn-t-elope-with-anyone-s-daughter-arvind-kejriwal-on-runaway-charge-505259', 'image': 'http://www.ndtv.com/news/images/story_page/Arvind-Kejriwal-presser-360x270_32.jpg'}, {'title': "Daily roadshows taking a toll on Arvind Kejriwal's health", 'url': 'http://economictimes.indiatimes.com/news/politics-and-nation/daily-roadshows-taking-a-toll-on-arvind-kejriwals-health/articleshow/33400944.cms', 'image': 'http://economictimes.indiatimes.com/thumb/msid-33400950,width-310,resizemode-4/daily-roadshows-taking-a-toll-on-arvind-kejriwals-health.jpg'}];
    var articles = [];
    for (var i=0; i<articlelist.length; i++) {
	articles.push({'title': articlelist[i]['_source']['title'], 'url': articlelist[i]['_source']['url'], 'image': 'http://economictimes.indiatimes.com/thumb/msid-33400950,width-310,resizemode-4/daily-roadshows-taking-a-toll-on-arvind-kejriwals-health.jpg'})
    }

    if (articles.length>0) {
	document.body.innerHTML = "<div class='attribution'>Powered by ZopEye</div>";
    };

    for (var i = 0; i < articles.length; i++) {
      var d = document.createElement('div');
      var a = document.createElement('a');
      a.href = articles[i].url;
      a.target= "_blank";
      a.innerHTML = '<img src="'+ articles[i].image+'"><br/>' + articles[i].title
      d.appendChild(a);
      document.body.appendChild(d);
    }
  }
};

document.addEventListener('DOMContentLoaded', function () {
  articleGenerator.requestArticles();
});


