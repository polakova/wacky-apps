package com.wackyapps.app;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

/**
 * Minimal WebView host. Loads the bundled offline app from assets/www/index.html.
 * The same wrapper powers every Wacky App; only the assets + label + package differ.
 */
public class MainActivity extends Activity {
    private WebView web;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);

        // Ask for mic up front (only the Yelling Meter uses it; others ignore it).
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            try { requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO}, 1); } catch (Exception ignored) {}
        }

        web = new WebView(this);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);                       // localStorage (high scores, counters)
        s.setMediaPlaybackRequiresUserGesture(false);       // WebAudio toys
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        WebView.setWebContentsDebuggingEnabled(false);

        // Grant in-page permission requests (mic) so getUserMedia works once the OS allows it.
        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(final PermissionRequest request) {
                runOnUiThread(() -> request.grant(request.getResources()));
            }
        });

        // Keep local (file://) navigation inside the WebView so the all-in-one
        // collection's offline hub works. Any http(s) link — e.g. the "← all 111"
        // link back to the live site — opens in the phone's real browser, which
        // does the networking (this app itself has no INTERNET permission).
        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest req) {
                return openExternally(req.getUrl().toString());
            }
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return openExternally(url);
            }
        });

        setContentView(web);
        web.loadUrl("file:///android_asset/www/index.html");
    }

    /** http/https → open in external browser (return true = WebView won't load it). file:// → false. */
    private boolean openExternally(String url) {
        if (url != null && (url.startsWith("http://") || url.startsWith("https://"))) {
            try { startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url))); } catch (Exception ignored) {}
            return true;
        }
        return false;
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) web.goBack();   // navigate the all-in-one collection
        else super.onBackPressed();
    }
}
