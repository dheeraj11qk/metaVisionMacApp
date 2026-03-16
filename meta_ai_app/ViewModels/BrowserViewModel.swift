


import SwiftUI
import WebKit
import Combine

class BrowserViewModel: NSObject, ObservableObject, WKNavigationDelegate, WKScriptMessageHandler {

    @Published var webView = WKWebView()
    @Published var progress: Double = 0
    @Published var downloads: [DownloadItem] = []
    @Published var showDownloads = false
    @Published var isDownloading = false

    override init() {

        let config = WKWebViewConfiguration()
        config.websiteDataStore = WKWebsiteDataStore.default()

        // JavaScript listener for blob downloads
        let script = """
        document.addEventListener('click', function(e){

            const a = e.target.closest('a');
            if(!a) return;

            const href = a.href || "";

            if(href.startsWith("blob:")){

                fetch(href)
                .then(r => r.blob())
                .then(blob => {

                    const reader = new FileReader();

                    reader.onloadend = function(){
                        window.webkit.messageHandlers.download.postMessage(reader.result);
                    };

                    reader.readAsDataURL(blob);

                });

                e.preventDefault();
                return;
            }

        });
        """

        let contentController = WKUserContentController()

        contentController.addUserScript(
            WKUserScript(
                source: script,
                injectionTime: .atDocumentEnd,
                forMainFrameOnly: false
            )
        )

        config.userContentController = contentController

        webView = WKWebView(frame: .zero, configuration: config)

        super.init()

        contentController.add(self, name: "download")

        webView.navigationDelegate = self

        webView.addObserver(
            self,
            forKeyPath: "estimatedProgress",
            options: .new,
            context: nil
        )
    }

    // MARK: Progress

    override func observeValue(
        forKeyPath keyPath: String?,
        of object: Any?,
        change: [NSKeyValueChangeKey : Any]?,
        context: UnsafeMutableRawPointer?
    ) {

        if keyPath == "estimatedProgress" {
            progress = webView.estimatedProgress
        }
    }

    // MARK: Navigation

    func load(urlString: String) {

        var text = urlString

        if !text.contains("http") {
            text = "https://www.google.com/search?q=\(text)"
        }

        if let url = URL(string: text) {
            webView.load(URLRequest(url: url))
        }
    }

    func goBack() {
        if webView.canGoBack { webView.goBack() }
    }

    func goForward() {
        if webView.canGoForward { webView.goForward() }
    }

    func reload() {
        webView.reload()
    }

    // MARK: Navigation policy

    func webView(_ webView: WKWebView,
                 decidePolicyFor navigationAction: WKNavigationAction,
                 decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {

        decisionHandler(.allow)
    }

    // MARK: JS message handler

    func userContentController(
        _ userContentController: WKUserContentController,
        didReceive message: WKScriptMessage
    ) {

        guard message.name == "download" else { return }

        // blob base64 download
        if let base64 = message.body as? String,
           base64.starts(with: "data:") {

            saveBase64File(base64)
        }
    }

    // MARK: Save blob file

    func saveBase64File(_ base64: String) {

        guard let comma = base64.firstIndex(of: ",") else { return }

        let meta = base64[..<comma]
        let dataString = base64[base64.index(after: comma)...]

        guard let data = Data(base64Encoded: String(dataString)) else { return }

        var ext = "file"

        if meta.contains("video/mp4") { ext = "mp4" }
        if meta.contains("image/png") { ext = "png" }
        if meta.contains("image/jpeg") { ext = "jpg" }
        if meta.contains("image/webp") { ext = "webp" }

        let filename = "download_\(UUID().uuidString).\(ext)"

        let downloadsFolder = FileManager.default.urls(
            for: .downloadsDirectory,
            in: .userDomainMask
        ).first!

        let fileURL = downloadsFolder.appendingPathComponent(filename)

        do {

            try data.write(to: fileURL)

            DispatchQueue.main.async {

                self.downloads.append(
                    DownloadItem(
                        filename: filename,
                        progress: 1,
                        status: "Completed"
                    )
                )

                self.isDownloading = false
            }

            print("Saved file:", fileURL)

        } catch {

            print("Save failed:", error)
        }
    }
}
