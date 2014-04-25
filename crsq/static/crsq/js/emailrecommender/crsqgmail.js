s = document.createElement('script');
s.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js');
document.getElementsByTagName('head')[0].appendChild(s);
var jqueryloadchecker = window.setInterval(checkJquery, 3000);
 
function jqueryLoaded() {
	clearInterval(jqueryloadchecker);
	gmailEmailRecommender();
}
 
function checkJquery() {
       clearInterval(jqueryloadchecker);
       if (window.jQuery)  {jqueryLoaded();} else { jqueryloadchecker = window.setInterval(checkJquery, 3000);}
}

function onlyUnique(value, index, self) {
	return self.indexOf(value) === index;
}

function gmailEmailRecommender() {
	$.when(getGmailEmailsContent()).done(function(x)  {
		console.log(x);
		$.ajax({
      		    type: "GET",
		    crossDomain: true,
		    url: "https://46.137.209.142/gmailemailjs",
		    data: { emailcontent: x },
		    dataType: "jsonp",
		    jsonp: 'jsonp_callback'
		}).done(function(data) {
		    console.log("CRSQ Gmail Email Recommender");
		    console.log(data['output']);
		    showonsidebar(data['output']);
		})
	})
}

function showonsidebar(l) {	
	if ($("#crsqdiv").length == 0) {
		$('.nH .adC').html('')
	        $('.nH .adC').append('<div id="crsqdiv"></div>')
	}
	else {
        	$("#crsqdiv").html('')
	}

	$("#crsqdiv").append('<style type="text/css"> .crsqtitle { font-size:80%; color: #222;word-wrap: break-word;} .crsqlink {font-size:70%;word-wrap:break-word;} </style>');
	$("#crsqdiv").append('Antaryaami Suggestions<br/><br/>');
	$('#rapportive-sidebar').hide();

	arrlen=l.length;

	if (arrlen == 0) {
		$('#crsqdiv').append("No Suggestions as of now");
	}

	for (var i = 0; i < arrlen; i++) {
        	$('#crsqdiv').append( "<div class='crsqtitle'>" + l[i]['articletitle'] + "</div><div class='crsqlink'><a href='" + l[i]['url'] + "'>" + l[i]['url'] + "</a></div><br/>");
	}
}

function getGmailEmailsContent() {

	openemails=[]; 
	$.each($('.adP'), function(index, value) { openemails.push($($(value).html().replace('<wbr>','').replace(/>/gi,'> ')).text().replace(/  /gi, ' ').replace(/\n/g, ' ').replace(/<[^>]*>/g, " ").replace(/[-_][-_][-_]*/gi,' ').replace(/http[^\s]*/gi, ' ').replace(/@\s*[^\s]*/gi, ' ')) });
	emailcontent = openemails.join(' ').replace(/\W/g, ' ').trim().toLowerCase();
	if (emailcontent=="") {
		return emailcontent;
	}
	else {
		emailcontent = emailcontent.removeStopWords();
	}

	emailcontent = emailcontent.split(' ').filter(function(x) { return !(x=="") }).filter(function(x) { return !($.isNumeric(x))}).filter(onlyUnique).join(' ')

	return emailcontent;
	
}

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
	'am',
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
	'fri',
        'from',
        'full',
        'fully',
        'further',
        'furthered',
        'furthering',
        'furthers',
	'fwiw',
	'fyi',
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
	'lol',
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
	'mon',
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
        'newer',
        'newest',
	'news',
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
	'omg',
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
	'pm',
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
	'related',
	'remove',
        'right',
        'right',
        'room',
        'rooms',
        's',
        'said',
        'same',
	'sat',
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
	'sun',
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
	'thur',
	'thurs',
        'thus',
        'to',
        'today',
        'together',
        'too',
        'took',
        'toward',
	'tue',
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
	'wed',
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
