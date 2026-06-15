package com.wackyapps.app;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;

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

        setContentView(web);
        web.loadUrl("file:///android_asset/www/index.html");
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) web.goBack();   // navigate the all-in-one collection
        else super.onBackPressed();
    }
}
