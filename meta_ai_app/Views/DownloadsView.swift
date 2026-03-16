//
//  DownloadsView.swift
//  meta_ai_app
//
//  Created by Dheeraj Gautam on 16/03/26.
//



import SwiftUI

struct DownloadsView: View {

    var downloads: [DownloadItem]

    var body: some View {

        VStack(alignment: .leading) {

            Text("Downloads")
                .font(.headline)

            List(downloads) { item in
                Text(item.filename)
            }
            .frame(height: 150)
        }
        .padding()
    }
}
