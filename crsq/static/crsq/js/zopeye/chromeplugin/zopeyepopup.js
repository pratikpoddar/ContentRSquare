var articleGenerator = {
  
  searchlink: "",
  zopeyeArticles: function() {
    console.log("History Search Start");
    chrome.history.search({text:''}, function(historyItems){

        function onlyUnique(value, index, self) {
            return self.indexOf(value) === index;
        }
	
	function checkDomainBlocked(url) {
		
		if (url.indexOf("mail.google.com") > -1) {
			return 1;
		}
		
		if (url.indexOf("facebook.com") > -1) {
			return 1;
		}

		if (url.indexOf("twitter.com") > -1) {
			return 1;
		}

		if (url.indexOf("linkedin.com") > -1) {
			return 1;
		}
		
		if (url.indexOf("google.com/adsense") > -1) {
			return 1;
		}
	
		if (url.indexOf("quora.com") > -1) {
			return 1;
		}
		
		return 0;
	}

	function cleanTitle(str) {

		str = str.trim().toLowerCase();

		last = Math.max(str.lastIndexOf("-"), str.lastIndexOf("|"));

		if (str== "") { return "" }

                if (last==-1) { last = str.length; }

		str = str.substring(0,last).removeStopWords().trim();
		if (str== "") { return "" }

		str = str.replace(/[^a-z\s]+/g, " ").removeStopWords().replace(/\s{2,}/g, ' ').trim();
		if (str== "") { return "" }

		return str;
	}

        chrome.storage.local.get(null, function (data) { if (("articles" in data) && ("searchlink" in data)) { articleGenerator.showArticles_(data['articles'], data['searchlink']);}; });

	searchitem = []	
        for (var i=0; i<Math.min(historyItems.length,70);i++) {
		if (checkDomainBlocked(historyItems[i]['url'])==0) {
			historytitle = cleanTitle(historyItems[i]['title']);
			if (historytitle.length>0) {
				if (searchitem.length<50) {
			                searchitem.push(historytitle);
				}
			}
		}
        }

	searchitem = searchitem.filter(onlyUnique);
	searchitem = searchitem.slice(0,20);
	searchitem = searchitem.join(' ');
	console.log(searchitem);
	articleGenerator.searchlink =  'http://46.137.209.142/zopeyesearch/'+encodeURIComponent(searchitem);

	console.log("History Search Done");
	var req = new XMLHttpRequest();
	req.open("GET", articleGenerator.searchlink, true);
	console.log("Article Search Done");
	req.onload = function(e) { articleGenerator.showArticles_(JSON.parse(e.target.response), articleGenerator.searchlink); chrome.storage.local.set({'articles': JSON.parse(e.target.response), 'searchlink': articleGenerator.searchlink}, function() {}); };
	req.send(null);
	console.log("Showed Articles");
    })
  },

  showArticles_: function (articles, searchlink) {
    console.log(articles);
    if (articles.length>0) {
	document.body.innerHTML = "<div class='jumbotron'><div class='crsqsuggestions row'></div></div>";
	document.body.innerHTML += "<div class='crsqattribution row'><a href='"+searchlink+"' target='_blank'>Powered by ZopEye</a></div>"
    };

    for (var i = 0; i < Math.min(articles.length,4); i++) {
      var d = document.createElement('div');
      d.className="col-sm-3 col-lg-3 col-md-3 crsqarticle";
      var a = document.createElement('a');
      a.href = articles[i].url;
      a.target= "_blank";
      a.innerHTML = '<br/><img class="crsqimage" src="'+ articles[i].image+'"/><br/><div class="crsqtitle">' + articles[i].title + '</div>' + '<div class="crsqdomain">' + articles[i].domain + '</div>' +' <div class="crsqhighlight">' + articles[i].highlight + '</div>'
      d.appendChild(a);
      document.body.children[0].children[0].appendChild(d);
    }

    if (articles.length>0) {
        document.body.innerHTML += "<br/>";
    };

  }
};

document.addEventListener('DOMContentLoaded', function () {
	var i = new Image();
	i.onload = articleGenerator.zopeyeArticles;
	i.onerror = function () { document.body.children[0].children[0].innerHTML = "No Internet Connection Found. ZopEye eyes are closed!" ;}
	i.src = 'http://www.google.com/images/logo.png?d=' + escape(Date());
});


String.prototype.removeStopWords = function() {
    var x;
    var y;
    var word;
    var stop_word;
    var regex_str;
    var regex;
    var cleansed_string = this.valueOf();
    var stop_words = new Array(
        'a',
        'about',
        'above',
        'across',
        'after',
        'again',
        'against',
        'all',
        'almost',
        'alone',
        'along',
        'already',
        'also',
        'although',
        'always',
        'among',
        'an',
        'and',
        'another',
        'any',
        'anybody',
        'anyone',
        'anything',
        'anywhere',
        'are',
        'area',
        'areas',
        'around',
        'as',
        'ask',
        'asked',
        'asking',
        'asks',
        'at',
        'away',
        'b',
        'back',
        'backed',
        'backing',
        'backs',
        'be',
        'became',
        'because',
        'become',
        'becomes',
        'been',
        'before',
        'began',
        'behind',
        'being',
        'beings',
        'best',
        'better',
        'between',
        'big',
        'both',
        'but',
        'by',
        'c',
        'came',
        'can',
        'cannot',
        'case',
        'cases',
        'certain',
        'certainly',
        'clear',
        'clearly',
	'com',
        'come',
        'could',
        'd',
        'did',
        'differ',
        'different',
        'differently',
        'do',
        'does',
        'done',
        'down',
        'down',
        'downed',
        'downing',
        'downs',
        'during',
        'e',
        'each',
        'early',
        'either',
        'end',
        'ended',
        'ending',
        'ends',
        'enough',
	'error',
        'even',
        'evenly',
        'ever',
        'every',
        'everybody',
        'everyone',
        'everything',
        'everywhere',
        'f',
        'face',
        'faces',
        'fact',
        'facts',
        'far',
        'felt',
        'few',
        'find',
        'finds',
        'first',
        'for',
        'four',
        'from',
        'full',
        'fully',
        'further',
        'furthered',
        'furthering',
        'furthers',
        'g',
        'gave',
        'general',
        'generally',
        'get',
        'gets',
        'give',
        'given',
        'gives',
        'go',
        'going',
        'good',
        'goods',
        'got',
        'great',
        'greater',
        'greatest',
        'group',
        'grouped',
        'grouping',
        'groups',
        'h',
        'had',
        'has',
        'have',
        'having',
        'he',
        'her',
        'here',
        'herself',
        'high',
        'high',
        'high',
        'higher',
        'highest',
        'him',
        'himself',
        'his',
        'how',
        'however',
        'i',
        'if',
        'important',
        'in',
        'interest',
        'interested',
        'interesting',
        'interests',
        'into',
        'is',
        'it',
        'its',
        'itself',
        'j',
        'just',
        'k',
        'keep',
        'keeps',
        'kind',
        'knew',
        'know',
        'known',
        'knows',
        'l',
        'large',
        'largely',
        'last',
        'later',
        'latest',
        'least',
        'less',
        'let',
        'lets',
        'like',
        'likely',
        'long',
        'longer',
        'longest',
        'm',
        'made',
        'make',
        'making',
        'man',
        'many',
        'may',
        'me',
        'member',
        'members',
        'men',
        'might',
        'more',
        'most',
        'mostly',
        'mr',
        'mrs',
        'much',
        'must',
        'my',
        'myself',
        'n',
        'necessary',
        'need',
        'needed',
        'needing',
        'needs',
        'never',
        'new',
        'new',
        'newer',
        'newest',
        'next',
        'no',
        'nobody',
        'non',
        'noone',
        'not',
        'nothing',
        'now',
        'nowhere',
        'number',
        'numbers',
        'o',
        'of',
        'off',
        'often',
        'old',
        'older',
        'oldest',
        'on',
        'once',
        'one',
        'only',
        'open',
        'opened',
        'opening',
        'opens',
        'or',
        'order',
        'ordered',
        'ordering',
        'orders',
	'org',
        'other',
        'others',
        'our',
        'out',
        'over',
        'p',
        'part',
        'parted',
        'parting',
        'parts',
        'per',
        'perhaps',
        'place',
        'places',
        'point',
        'pointed',
        'pointing',
        'points',
        'possible',
        'present',
        'presented',
        'presenting',
        'presents',
        'problem',
        'problems',
        'put',
        'puts',
        'q',
        'quite',
        'r',
        'rather',
        'really',
	'remove',
        'right',
        'right',
        'room',
        'rooms',
        's',
        'said',
        'same',
        'saw',
        'say',
        'says',
        'second',
        'seconds',
        'see',
        'seem',
        'seemed',
        'seeming',
        'seems',
        'sees',
        'several',
        'shall',
        'she',
        'should',
        'show',
        'showed',
        'showing',
        'shows',
        'side',
        'sides',
        'since',
        'small',
        'smaller',
        'smallest',
        'so',
        'some',
        'somebody',
        'someone',
        'something',
        'somewhere',
        'state',
        'states',
        'still',
        'still',
        'such',
        'sure',
        't',
        'take',
        'taken',
        'than',
        'that',
        'the',
        'their',
        'them',
        'then',
        'there',
        'therefore',
        'these',
        'they',
        'thing',
        'things',
        'think',
        'thinks',
        'this',
        'those',
        'though',
        'thought',
        'thoughts',
        'three',
        'through',
        'thus',
        'to',
        'today',
        'together',
        'too',
        'took',
        'toward',
        'turn',
        'turned',
        'turning',
        'turns',
        'two',
        'u',
        'under',
        'until',
        'up',
        'upon',
        'us',
        'use',
        'used',
        'uses',
        'v',
	'visit',
        'very',
        'w',
        'want',
        'wanted',
        'wanting',
        'wants',
        'was',
        'way',
        'ways',
        'we',
        'well',
        'wells',
        'went',
        'were',
        'what',
        'when',
        'where',
        'whether',
        'which',
        'while',
        'who',
        'whole',
        'whose',
        'why',
        'will',
        'with',
        'within',
        'without',
        'work',
        'worked',
        'working',
        'works',
        'would',
	'www',
        'x',
        'y',
        'year',
        'years',
        'yet',
        'you',
        'young',
        'younger',
        'youngest',
        'your',
        'yours',
        'z'
    )
         
    // Split out all the individual words in the phrase
    words = cleansed_string.match(/[^\s]+|\s+[^\s+]$/g)
 
    // Review all the words
    for(x=0; x < words.length; x++) {
        // For each word, check all the stop words
        for(y=0; y < stop_words.length; y++) {
            // Get the current word
            word = words[x].replace(/\s+|[^a-z]+/ig, "");   // Trim the word and remove non-alpha
             
            // Get the stop word
            stop_word = stop_words[y];
             
            // If the word matches the stop word, remove it from the keywords
            if(word.toLowerCase() == stop_word) {
                // Build the regex
                regex_str = "^\\s*"+stop_word+"\\s*$";      // Only word
                regex_str += "|^\\s*"+stop_word+"\\s+";     // First word
                regex_str += "|\\s+"+stop_word+"\\s*$";     // Last word
                regex_str += "|\\s+"+stop_word+"\\s+";      // Word somewhere in the middle
                regex = new RegExp(regex_str, "ig");
             
                // Remove the word from the keywords
                cleansed_string = cleansed_string.replace(regex, " ");
            }
        }
    }
    return cleansed_string.replace(/^\s+|\s+$/g, "");
}
