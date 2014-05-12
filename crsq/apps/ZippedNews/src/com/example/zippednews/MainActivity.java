package com.example.zippednews;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		setContentView(R.layout.activity_main);

        WebView mainWebView = (WebView) findViewById(R.id.mainWebView);
        WebSettings webSettings = mainWebView.getSettings();
		webSettings.setJavaScriptEnabled(true);
		mainWebView.setWebViewClient(new MyCustomWebViewClient());
		mainWebView.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY);
		
        mainWebView.loadUrl("http://www.zippednews.com");
	}
	
    private class MyCustomWebViewClient extends WebViewClient {
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
            view.loadUrl(url);
            return true;
        }
    }

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

}
