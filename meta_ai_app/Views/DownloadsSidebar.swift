//
//  WebView.swift
//  meta_ai_app
//
//  Created by Dheeraj Gautam on 16/03/26.
//


import SwiftUI

struct DownloadsSidebar: View {

    var downloads: [DownloadItem]

    var body: some View {

        VStack(alignment: .leading) {

            Text("Downloads")
                .font(.headline)

            Divider()

            List(downloads) { item in

                VStack(alignment: .leading) {

                    Text(item.filename)

                    ProgressView(value: item.progress)

                    Text(item.status)
                        .font(.caption)
                        .foregroundColor(.gray)
                }
            }

            Spacer()

            Button("Open Downloads Folder") {

                let downloads = FileManager.default.urls(
                    for: .downloadsDirectory,
                    in: .userDomainMask
                )[0]

                NSWorkspace.shared.open(downloads)
            }
        }
        .frame(width: 300)
        .padding()
    }
}
