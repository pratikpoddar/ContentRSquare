var s = document.createElement('script');
s.setAttribute('src', 'https://46.137.209.142/static/crsq/js/emailrecommender/crsqgmail.js?v=4.01212');
(document.head||document.documentElement).appendChild(s);
console.log('CRSQ Gmail Extractor Running')
s.onload = function() {
    console.log('CRSQ Gmail Extractor JS Running')
    s.parentNode.removeChild(s);
};
