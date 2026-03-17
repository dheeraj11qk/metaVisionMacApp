//
//  WebView.swift
//  meta_ai_app
//
//  Created by Dheeraj Gautam on 16/03/26.
//



import SwiftUI
import WebKit

struct WebView: NSViewRepresentable {

    @ObservedObject var model: BrowserViewModel

    func makeNSView(context: Context) -> WKWebView {
        return model.webView
    }

    func updateNSView(_ nsView: WKWebView, context: Context) { }
}
