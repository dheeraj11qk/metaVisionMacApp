import SwiftUI

struct BrowserToolbar: View {

    @ObservedObject var model: BrowserViewModel
    @Binding var url: String

    var body: some View {

        HStack {

            Button {
                model.goBack()
            } label: {
                Image(systemName: "chevron.left")
            }

            Button {
                model.goForward()
            } label: {
                Image(systemName: "chevron.right")
            }

            Button {
                model.reload()
            } label: {
                Image(systemName: "arrow.clockwise")
            }

            TextField("Search or URL", text: $url)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .onSubmit {
                    model.load(urlString: url)
                }

            Button("Go") {
                model.load(urlString: url)
            }

            // Download Button
            Button {
                model.showDownloads.toggle()
            } label: {
                Image(systemName: "arrow.down.circle")
                    .font(.title3)
            }

        }
        .padding()
    }
}
