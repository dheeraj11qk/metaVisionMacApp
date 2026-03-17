import Foundation

class DownloadService: NSObject, URLSessionDownloadDelegate {

    static let shared = DownloadService()

    var progressHandler: ((Double) -> Void)?
    var completionHandler: ((String) -> Void)?

    lazy var session: URLSession = {
        URLSession(configuration: .default,
                   delegate: self,
                   delegateQueue: nil)
    }()

    func download(url: URL) {

        let task = session.downloadTask(with: url)
        task.resume()
    }

    // progress

    func urlSession(_ session: URLSession,
                    downloadTask: URLSessionDownloadTask,
                    didWriteData bytesWritten: Int64,
                    totalBytesWritten: Int64,
                    totalBytesExpectedToWrite: Int64) {

        let progress = Double(totalBytesWritten) /
                       Double(totalBytesExpectedToWrite)

        DispatchQueue.main.async {
            self.progressHandler?(progress)
        }
    }

    // finish

    func urlSession(_ session: URLSession,
                    downloadTask: URLSessionDownloadTask,
                    didFinishDownloadingTo location: URL) {

        guard let url = downloadTask.originalRequest?.url else { return }

        let downloads = FileManager.default.urls(
            for: .downloadsDirectory,
            in: .userDomainMask
        )[0]

        let destination = downloads.appendingPathComponent(
            url.lastPathComponent
        )

        try? FileManager.default.removeItem(at: destination)
        try? FileManager.default.moveItem(at: location, to: destination)

        DispatchQueue.main.async {
            self.completionHandler?(url.lastPathComponent)
        }
    }
}
