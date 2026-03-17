//
//   DownloadItem.swift.swift
//  meta_ai_app
//
//  Created by Dheeraj Gautam on 16/03/26.
//

import Foundation

struct DownloadItem: Identifiable {

    let id = UUID()
    let filename: String
    var progress: Double
    var status: String
}
