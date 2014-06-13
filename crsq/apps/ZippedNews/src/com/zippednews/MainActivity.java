package com.zippednews;

import com.zippednews.R;

import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.Bundle;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.view.KeyEvent;
import android.view.Menu;
import android.view.View;
import android.webkit.CookieManager;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

public class MainActivity extends Activity {

	WebView mainWebView;
	ProgressDialog pd;
		
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		
		super.onCreate(savedInstanceState);
		
		setContentView(R.layout.activity_main);
		
		pd = ProgressDialog.show(this, "", "Loading...",true);
		
		if(isNetworkStatusAvialable (getApplicationContext())) {
		    Toast.makeText(getApplicationContext(), "Loading ZippedNews", Toast.LENGTH_SHORT).show();

		    mainWebView = (WebView) findViewById(R.id.mainWebView);
			
			WebSettings webSettings = mainWebView.getSettings();
			webSettings.setJavaScriptEnabled(true);
			CookieManager.getInstance().setAcceptCookie(true);
			mainWebView.setWebViewClient(new MyCustomWebViewClient());
			mainWebView.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY);
			mainWebView.loadUrl("http://www.zippednews.com");
			
		} else {
			Toast.makeText(getApplicationContext(), "Cannot load ZippedNews. No Internet Connection", Toast.LENGTH_SHORT).show();
		}
	}
	
	public static boolean isNetworkStatusAvialable (Context context) {
	    ConnectivityManager connectivityManager = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
	    if (connectivityManager != null) 
	    {
	        NetworkInfo netInfos = connectivityManager.getActiveNetworkInfo();
	        if(netInfos != null)
	        if(netInfos.isConnected()) 
	            return true;
	    }
	    return false;
	}
	
    private class MyCustomWebViewClient extends WebViewClient {
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
            if ((Uri.parse(url).getHost().contains("zippednews.com")) || true) {
                // This is my web site, so do not override; let my WebView load the page
            	if(isNetworkStatusAvialable (getApplicationContext())) { 
            		view.loadUrl(url);
            	}
            	else {
            		Toast.makeText(getApplicationContext(), "Cannot load ZippedNews. No Internet Connection", Toast.LENGTH_SHORT).show();
            	}
                return false;
            }
            
            else {
            	// Otherwise, the link is not for a page on my site, so launch another Activity that handles URLs
            	Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
            	startActivity(intent);
            	return true;
            }
        }
        
        @Override
        public void onPageFinished(WebView view, String url) {
            if(pd.isShowing()&&pd!=null)
            {
                pd.dismiss();
            }
        }
        
    }
    
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        // Check if the key event was the Back button and if there's history
        if ((keyCode == KeyEvent.KEYCODE_BACK) && mainWebView.canGoBack()) {
            mainWebView.goBack();
            return true;
        }
        // If it wasn't the Back key or there's no web page history, bubble up to the default
        // system behavior (probably exit the activity)
        return super.onKeyDown(keyCode, event);
    }

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

}
