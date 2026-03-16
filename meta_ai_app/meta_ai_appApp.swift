//
//  meta_ai_appApp.swift
//  meta_ai_app
//
//  Created by Dheeraj Gautam on 16/03/26.
//

import SwiftUI
import CoreData

@main
struct meta_ai_appApp: App {
    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}
