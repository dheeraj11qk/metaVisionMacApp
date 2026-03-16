import SwiftUI

struct ContentView: View {

    @StateObject var model = BrowserViewModel()
    @State private var url = "https://www.meta.ai/"

    var body: some View {

        HStack(spacing:0){

            VStack{

                BrowserToolbar(
                    model: model,
                    url: $url
                )

                WebView(model: model)

            }

            if model.showDownloads {

                DownloadsSidebar(
                    downloads: model.downloads
                )
            }
        }
        .onAppear {
            model.load(urlString: url)
        }
    }
}
